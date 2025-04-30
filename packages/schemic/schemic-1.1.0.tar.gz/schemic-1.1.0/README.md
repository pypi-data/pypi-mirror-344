# Schemic

[![PyPI version](https://badge.fury.io/py/schemic.svg)](https://badge.fury.io/py/schemic)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

OpenAI's structured output API allows you to specify a JSON schema for the model's response, ensuring predictable output. However, generating a compatible schema from standard Pydantic models presents several challenges:

1.  **Strict Requirements:** OpenAI imposes specific constraints not typical in standard JSON Schema usage:
    *   `additionalProperties` must often be `False`.
    *   `required` fields must be explicitly listed for all properties within an object (with some exceptions for dictionary-like objects).
    *   `default` values are disallowed.
    *   Certain types or keywords like `format: date-time` or `oneOf` are forbidden.
    *   `$ref` objects cannot have sibling keywords.
    *   `anyOf` choices requires unique first keys.
2.  **Manual Conversion:** Developers often resort to manually creating separate, simplified schemas or writing complex conversion logic to bridge the gap between their application's Pydantic models and OpenAI's requirements.
3.  **Workflow Complexity:** This leads to duplicated model definitions, increased maintenance overhead, and potential inconsistencies.

## Schemic's Solution

Schemic simplifies using Pydantic models with OpenAI's structured output by providing a `SchemicModel` base class.

1.  **Inherit:** Define your data structures by inheriting from `SchemicModel` instead of Pydantic's `BaseModel`.
2.  **Generate:** Use the `YourModel.schemic_schema()` class method. This method automatically:
    *   Generates the JSON schema from your Pydantic model.
    *   Recursively modifies the schema to comply with OpenAI's strict requirements (handling `additionalProperties`, `required`, `default`, disallowed keywords, etc.).
    *   Wraps the schema in the necessary format (`{"type": "json_schema", "json_schema": {...}}`) for the OpenAI API.
3.  **Use:** Pass the generated schema directly to the `response_format` parameter in your OpenAI API call.
4.  **Parse:** Instantiate your `SchemicModel` directly from the OpenAI response dictionary (`YourModel(**response_dict)`), leveraging Pydantic's built-in parsing.

No more manual schema adjustments or duplicate models. Define once, generate a compatible schema, and parse the response easily.

## Installation

```bash
pip install schemic
```

## Quick Example

```python
# filepath: example.py
import datetime
import json
from typing import List, Optional
from pydantic import Field
from schemic import SchemicModel # Import SchemicModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables (replace with your API key management)
load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Define your models using SchemicModel
class Task(SchemicModel):
    description: str = Field(..., description="Description of the task")
    due_date: Optional[datetime.date] = Field(None, description="Optional due date")
    completed: bool = Field(False, description="Whether the task is completed")

class TodoList(SchemicModel):
    title: str = Field(..., description="Title of the todo list")
    items: List[Task] = Field(..., description="List of tasks")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Timestamp of creation" # Note: default/default_factory will be handled
    )

# 2. Generate the OpenAI-compatible schema
openai_schema = TodoList.schemic_schema()

# Optional: See the generated schema
# print(json.dumps(openai_schema, indent=2))
# Note how 'default' is removed from 'completed', 'format' might be removed from dates,
# 'additionalProperties' and 'required' are adjusted, and the whole thing is wrapped.

# 3. Use the schema with the OpenAI API
def create_todo_list(prompt: str):
    response = client.chat.completions.create( # Use create for newer versions
        model="gpt-4o", # Or your preferred model supporting structured output
        messages=[
            {"role": "system", "content": "You are an assistant that creates todo lists."},
            {"role": "user", "content": prompt}
        ],
        response_format=openai_schema, # Pass the generated schema
        temperature=0.5,
    )

    # 4. Parse the response directly into your SchemicModel
    response_content = response.choices[0].message.content
    if response_content:
        try:
            content_dict = json.loads(response_content)
            todo_list = TodoList(**content_dict) # Direct parsing!
            return todo_list
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON response")
            print(response_content)
            return None
        except Exception as e: # Catch Pydantic validation errors etc.
             print(f"Error parsing response into model: {e}")
             print(response_content)
             return None
    else:
        print("Error: Empty response content")
        return None


# Example usage
prompt = "Create a todo list for a weekend trip: pack clothes, book hotel, charge phone."
my_list = create_todo_list(prompt)

if my_list:
    print(f"\n--- Todo List: {my_list.title} ---")
    for item in my_list.items:
        print(f"- {item.description} (Completed: {item.completed})")
    # Note: created_at will have the default value assigned by Pydantic during parsing
    print(f"Created At: {my_list.created_at}")

```

## Key Features

-   **`SchemicModel`**: Inherit from this class instead of `pydantic.BaseModel`.
-   **`YourModel.schemic_schema()`**: Class method that generates the OpenAI-compatible JSON schema.
    -   Handles `additionalProperties`, `required`, `default`, `oneOf` -> `anyOf`, `$ref` cleanup, `format` removal, and wrapping automatically.
    -   Accepts an optional `delete_props_with_defaults=True` argument to remove fields with defaults entirely, instead of just removing the `default` keyword.
-   **Standard Pydantic Parsing**: Use `YourModel(**response_dict)` to parse the OpenAI response, benefiting from Pydantic's validation and default value handling on the *receiving* end.

## Why Use Schemic?

-   **Single Source of Truth**: Define your data models once using Pydantic and use them for both your application logic and OpenAI interaction.
-   **Automatic Compliance**: Automatically handles the nuances and strict requirements of OpenAI's JSON schema format.
-   **Simplified Workflow**: Eliminates the need for manual schema conversion, duplicate models, or complex post-processing logic.
-   **Leverage Pydantic**: Continue to benefit from Pydantic's robust validation and data parsing features when receiving responses.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
Test your changes with `python -m unittest discover tests`

## Known Requirements of the OpenAI API:
This is the running list of openais specific requirements I'm aware of:
1. Additional properties must be set on all nested objects, and if not having contents must be set to False
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'AISectionResponse': In context=(), 'additionalProperties' is required to be supplied and to be false.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
2. The “required” keyword must be set on all nested properties (unless they are objects)
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'AISectionResponse': In context=(), 'required' is required to be supplied and to be an array including every key in properties. Missing 'id'.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
3. defaults are not allowed ever
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'AISectionResponse': In context=('properties', 'type'), 'default' is not permitted.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
4. datetimes and variables other than basic data types are never allowed
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'MathProblem': In context=('properties', 'created_at'), 'format' is not permitted.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
5. oneOf is not permitted to be in the schema (handle this by converting it to anyOf)
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'PetOwner': In context=('properties', 'pet'), 'oneOf' is not permitted.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
6. anyOf must not share identical first keys (including in the required keys array, as well as in the properties dictionary)
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema: Objects provided via 'anyOf' must not share identical first keys. Consider adding a discriminator key or rearranging the properties to ensure the first key is unique.", 'type': 'invalid_request_error', 'param': None, 'code': None}}
```
7. REMOVED
8. you have to wrap the schema in a specific format before sending the model to the ai
```json
{
    "type": "json_schema", // must remain the same
    "json_schema": { // must remain the same
        "strict": True, // must remain the same
        "name": "schemic_model", // this is the name of the model
        "schema": {} // this is the actual schema
    }
}
```
9. some models have heightened requirements compared to others... Shouldn't matter however, and schemic should always just produce the highest level of strictness possible. For example, o1 model will throw an error like seen with requirement #6, but 4o will not.
10. required array doesn't seem to support objects with certain properties. For example, if the object doesn't have a "properties" field (or no "required" field) (dictionaries for example only have additionalProperties).
* This makes sense given that you can't require something with an undefined key. So if the object is a dictionary, it doesn't need to be required, but if it is an object, it does need to be required.
For example it will support "nested", but not "determined_dir" in the following example:
```python
schema = {
    "type": "json_schema",
    "json_schema": {
        "strict": True,
        "name": "AISectionResponse",
        "schema": { # Added everything before this line (AKA requirement #8)
            "$defs": {
                "NestedObjectR1": {
                    "properties": {
                        "nested_prop": {
                            "title": "Nested Prop",
                            "type": "string"
                        }
                    },
                    "required": [
                        "nested_prop"
                    ],
                    "additionalProperties": False, # Added this line (AKA requirement #1)
                    "title": "NestedObjectR1",
                    "type": "object"
                },
                "NoteSegmentButton": {
                    "properties": {
                        "type": { # This must also be the first one in the dictionary, as it is unique (AKA requirement #6)
                            "enum": ["button"], # Changed this line (AKA requirement #3) --> Removed SegmentType and replaced with enum values
                            "title": "Type", # Changed this line (AKA requirement #3)
                            "type": "string" # Changed this line (AKA requirement #3)
                        },
                        "id": {
                            "title": "Id",
                            "type": "string"
                        },
                        "isDetermined": {
                            "title": "Isdetermined",
                            "type": "boolean"
                        },
                        "placeholder": {
                            "description": "The placeholder text for the button. This is what will be displayed on the button itself.",
                            "title": "Placeholder",
                            "type": "string"
                        },
                        "action": {
                            "description": "The action to take when the button is clicked. This could be a function name, a URL, etc.",
                            "title": "Action",
                            "type": "string"
                        }
                    },
                    "additionalProperties": False, # Added this line (AKA requirement #1)
                    "required": [
                        "type", # Added this line (AKA requirement #2). This must also be the first one in the list, as it is unique (AKA requirement #6)
                        "id", # Added this line (AKA requirement #2)
                        "isDetermined",
                        "placeholder",
                        "action"
                    ],
                    "title": "NoteSegmentButton",
                    "type": "object"
                },
                "NoteSegmentDropdown": {
                    "properties": {
                        "type": { # This must also be the first one in the dictionary, as it is unique (AKA requirement #6)
                            "enum": ["dropdown"], # Changed this line (AKA requirement #3) --> Removed SegmentType and replaced with enum values
                            "title": "Type", # Changed this line (AKA requirement #3)
                            "type": "string" # Changed this line (AKA requirement #3)
                        },
                        "id": {
                            "title": "Id",
                            "type": "string"
                        },
                        "isDetermined": {
                            "title": "Isdetermined",
                            "type": "boolean"
                        },
                        "options": {
                            "items": {
                                "type": "string"
                            },
                            "title": "Options",
                            "type": "array"
                        },
                        "selected": {
                            "items": {
                                "type": "integer"
                            },
                            "title": "Selected",
                            "type": "array"
                        }
                    },
                    "additionalProperties": False, # Added this line (AKA requirement #1)
                    "required": [
                        "type", # Added this line (AKA requirement #2) This must also be the first one in the list, as it is unique (AKA requirement #6)
                        "id", # Added this line (AKA requirement #2)
                        "isDetermined",
                        "options",
                        "selected"
                    ],
                    "title": "NoteSegmentDropdown",
                    "type": "object"
                },
                "NoteSegmentInput": {
                    "properties": {
                        "type": { # This must also be the first one in the dictionary, as it is unique (AKA requirement #6)
                            "enum": ["input"], # Changed this line (AKA requirement #3) --> Removed SegmentType and replaced with enum values
                            "title": "Type", # Changed this line (AKA requirement #3)
                            "type": "string" # Changed this line (AKA requirement #3)
                        },
                        "id": {
                            "title": "Id",
                            "type": "string"
                        },
                        "isDetermined": {
                            "title": "Isdetermined",
                            "type": "boolean"
                        },
                        "value": {
                            "title": "Value",
                            "type": "string"
                        }
                    },
                    "additionalProperties": False, # Added this line (AKA requirement #1)
                    "required": [
                        "type", # Added this line (AKA requirement #2) This must also be the first one in the list, as it is unique (AKA requirement #6)
                        "id", # Added this line (AKA requirement #2)
                        "isDetermined",
                        "value"
                    ],
                    "title": "NoteSegmentInput",
                    "type": "object"
                },
                # SegmentType removed as no longer needed since defaults are not supported by openai, and and we are instead using enum values in the code
            },
            "properties": {
                "top_level_prop": {
                    "title": "Top Level Prop",
                    "type": "string"
                },
                "nested": {
                    "$ref": "#/$defs/NestedObjectR1"
                }, # normal object
                "determined_dir": {
                    "additionalProperties": { # This doesn't need to be false because it has a value... if there was no value we would have to set additionalProperties to false
                        "anyOf": [
                            {
                                "$ref": "#/$defs/NoteSegmentDropdown"
                            },
                            {
                                "$ref": "#/$defs/NoteSegmentInput"
                            },
                            {
                                "$ref": "#/$defs/NoteSegmentButton"
                            }
                        ]
                    },
                    "description": "A dictionary where keys are the placeholder IDs (e.g., 'SOMEUUID1') from the template's content_str, and values are the determined content for that placeholder.",
                    "title": "Determined Dir",
                    "type": "object"
                }, # not a normal object, but a dictionary with a specific structure, with no properties or required fields
                "determined_str": {
                    "description": "The string representing the text for the note section, with '{SOMEUUID1}' representing data from the determined_dir.",
                    "title": "Determined Str",
                    "type": "string"
                }
            },
            "additionalProperties": False, # Added this line (AKA requirement #1)
            "required": [
                "top_level_prop",
                "nested", # THIS IS SUPPORTED
                "determined_dir", # THIS IS NOT SUPPORTED, AND THE LINE MUST BE COMMENTED OUT, DESPITE "nested" BEING SUPPORTED, AND THEY ARE BOTH OBJECTS
                "determined_str",
            ],
            "title": "AISectionResponse",
            "type": "object"
        }
    }
}
```

Example Error:
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'AISectionResponse': In context=(), 'required' is required to be supplied and to be an array including every key in properties. Extra required key 'determined_dir' supplied.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```
11. $refs do not support additional keys:
```cmd
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'PetOwner': context=('properties', 'pet_color'), $ref cannot have keywords {'description'}.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}

openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid schema for response_format 'PetOwner': context=('properties', 'pet_color'), $ref cannot have keywords {'type'}.", 'type': 'invalid_request_error', 'param': 'response_format', 'code': None}}
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

