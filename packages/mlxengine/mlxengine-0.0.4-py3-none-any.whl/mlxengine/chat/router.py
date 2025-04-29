import json
from typing import Generator, List, Dict, Any, Union # Added Dict, Any, Union
import collections.abc # To check for Mapping/Sequence types

from starlette.responses import StreamingResponse
from starlette.requests import Request
from turboapi import APIRouter, JSONResponse

from .mlx.models import load_model
# Import the base Model class from satya to check instance types
from satya import Model
# Import necessary schema components
from .schema import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    Role, # Assuming Role is needed by ChatMessage or used elsewhere
    # Import the chunk types if needed for type hints, though Model check is key
    # ChatCompletionChunk,
    # ChatCompletionChunkChoice
    ResponseFormat, # Import ResponseFormat
    JsonSchemaFormat, # Import JsonSchemaFormat for nested deserialization
    Tool,            # Import Tool for tool deserialization
    Function,        # Import Function for nested tool deserialization
    FunctionParameters, # Import FunctionParameters for deeply nested deserialization
)
from .text_models import BaseTextModel
from ..utils.serialization import recursive_to_dict # Import the helper function

router = APIRouter(tags=["chat—completions"])


# --- Helper function for recursive serialization ---
# def recursive_to_dict(item: Any) -> Any:
#     """Recursively converts satya.Model instances to dictionaries."""
#     if isinstance(item, Model):
#         # Call .dict() on the model instance
#         try:
#             d = item.dict()
#         except AttributeError:
#              # Fallback if .dict() doesn't exist - adapt as needed for satya
#              # This example assumes fields are attributes or stored in __fields__
#              try:
#                  d = {f: getattr(item, f) for f in item.__fields__}
#              except AttributeError:
#                  # Last resort: return as is, hoping it's serializable or error later
#                  return item # Or raise an error?
# 
#         # Recursively process the dictionary values
#         return recursive_to_dict(d)
#     elif isinstance(item, collections.abc.Mapping):
#         # If it's a dictionary-like object, process its values
#         return {k: recursive_to_dict(v) for k, v in item.items()}
#     elif isinstance(item, collections.abc.Sequence) and not isinstance(item, (str, bytes)):
#         # If it's a list/tuple-like object (but not string/bytes), process its elements
#         return [recursive_to_dict(elem) for elem in item]
#     else:
#         # Assume it's a primitive type (int, str, float, bool, None)
#         return item
# --- End Helper function ---


@router.post("/chat/completions", response_model=ChatCompletionResponse)
@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: Request):
    """Create a chat completion"""
    try:
        body = await request.json()
        chat_request_initial = ChatCompletionRequest(**body) # Initial parse

        # --- Explicit Deserialization for Nested Models ---
        # Use .dict() or fallback to get a mutable dictionary representation
        try:
             chat_request_data = chat_request_initial.dict()
        except AttributeError:
             # Fallback if .dict() doesn't exist
             # This assumes fields are accessible attributes
             # Adjust if satya.Model stores fields differently (e.g., __fields__)
             fields = getattr(chat_request_initial, '__fields__', None)
             if fields:
                 chat_request_data = {f: getattr(chat_request_initial, f) for f in fields}
             else:
                 # If no obvious way to get fields, try vars() as a last resort
                 # This might include internal attributes, use with caution
                 chat_request_data = vars(chat_request_initial)

        # Deserialize 'messages'
        raw_messages = chat_request_data.get('messages', [])
        if raw_messages:
            typed_messages = []
            for msg in raw_messages:
                if isinstance(msg, dict):
                    typed_messages.append(ChatMessage(**msg))
                elif isinstance(msg, ChatMessage): # Already typed
                    typed_messages.append(msg)
            chat_request_data['messages'] = typed_messages

        # Deserialize 'response_format' and its nested 'json_schema'
        raw_response_format = chat_request_data.get('response_format')
        if isinstance(raw_response_format, dict):
            # First, handle the nested 'json_schema' if it exists and is a dict
            nested_json_schema = raw_response_format.get('json_schema')
            if isinstance(nested_json_schema, dict):
                try:
                    # Convert the nested dict to JsonSchemaFormat model
                    raw_response_format['json_schema'] = JsonSchemaFormat(**nested_json_schema)
                except Exception as e_jsf:
                    print(f"Error deserializing nested json_schema: {e_jsf}")
                    raise ValueError(f"Invalid json_schema structure within response_format: {nested_json_schema}") from e_jsf
            elif isinstance(nested_json_schema, JsonSchemaFormat):
                # Already typed, no action needed
                pass

            # Now, instantiate the outer ResponseFormat model
            try:
                chat_request_data['response_format'] = ResponseFormat(**raw_response_format)
            except Exception as e_rf:
                print(f"Error deserializing response_format: {e_rf}")
                raise ValueError(f"Invalid response_format structure: {raw_response_format}") from e_rf
        elif isinstance(raw_response_format, ResponseFormat):
            # Already typed, check nested just in case (though unlikely if outer is typed)
            if isinstance(raw_response_format.json_schema, dict):
                 try:
                     raw_response_format.json_schema = JsonSchemaFormat(**raw_response_format.json_schema)
                 except Exception as e_jsf:
                     print(f"Error deserializing nested json_schema within existing ResponseFormat: {e_jsf}")
                     raise ValueError(f"Invalid json_schema dict within ResponseFormat object: {raw_response_format.json_schema}") from e_jsf
            # No further action needed if both outer and nested are typed

        # Deserialize 'tools' and their nested 'function' -> 'parameters'
        raw_tools = chat_request_data.get('tools')
        if isinstance(raw_tools, list):
            typed_tools = []
            for tool_dict in raw_tools:
                if isinstance(tool_dict, dict):
                    # Handle nested 'function'
                    function_dict = tool_dict.get('function')
                    if isinstance(function_dict, dict):
                        # Handle deeply nested 'parameters' within 'function'
                        params_dict = function_dict.get('parameters')
                        if isinstance(params_dict, dict):
                            try:
                                function_dict['parameters'] = FunctionParameters(**params_dict)
                            except Exception as e_fp:
                                print(f"Error deserializing function parameters: {e_fp}")
                                raise ValueError(f"Invalid parameters structure in function: {params_dict}") from e_fp
                        elif isinstance(params_dict, FunctionParameters):
                            pass # Already typed

                        # Now instantiate Function with potentially typed parameters
                        try:
                            tool_dict['function'] = Function(**function_dict)
                        except Exception as e_f:
                            print(f"Error deserializing function: {e_f}")
                            raise ValueError(f"Invalid function structure in tool: {function_dict}") from e_f
                    elif isinstance(function_dict, Function):
                        # If function is already typed, still check its parameters
                        if isinstance(function_dict.parameters, dict):
                             try:
                                function_dict.parameters = FunctionParameters(**function_dict.parameters)
                             except Exception as e_fp_nested:
                                 print(f"Error deserializing nested function parameters: {e_fp_nested}")
                                 raise ValueError(f"Invalid parameters dict within Function object: {function_dict.parameters}") from e_fp_nested

                    # Now instantiate Tool with potentially typed function
                    try:
                        typed_tools.append(Tool(**tool_dict))
                    except Exception as e_t:
                        print(f"Error deserializing tool: {e_t}")
                        raise ValueError(f"Invalid tool structure: {tool_dict}") from e_t
                elif isinstance(tool_dict, Tool):
                    # If tool is already typed, perform nested checks just in case
                    if isinstance(tool_dict.function, dict):
                         # This case is less likely if outer is typed, but for robustness:
                         function_dict_inner = tool_dict.function
                         params_dict_inner = function_dict_inner.get('parameters')
                         if isinstance(params_dict_inner, dict):
                             try:
                                 function_dict_inner['parameters'] = FunctionParameters(**params_dict_inner)
                             except Exception as e_fp_deep:
                                 print(f"Error deserializing deeply nested function parameters: {e_fp_deep}")
                                 raise ValueError(f"Invalid parameters structure in function dict within Tool object: {params_dict_inner}") from e_fp_deep
                         try:
                             tool_dict.function = Function(**function_dict_inner)
                         except Exception as e_f_inner:
                             print(f"Error deserializing function dict within Tool object: {e_f_inner}")
                             raise ValueError(f"Invalid function dict within Tool object: {function_dict_inner}") from e_f_inner
                    elif isinstance(tool_dict.function, Function):
                        # Check parameters within the already-typed Function
                        if isinstance(tool_dict.function.parameters, dict):
                             try:
                                tool_dict.function.parameters = FunctionParameters(**tool_dict.function.parameters)
                             except Exception as e_fp_nested_typed:
                                 print(f"Error deserializing parameters dict within typed Function object: {e_fp_nested_typed}")
                                 raise ValueError(f"Invalid parameters dict within Function object: {tool_dict.function.parameters}") from e_fp_nested_typed
                    typed_tools.append(tool_dict) # Append the already typed (and potentially fixed) tool
            chat_request_data['tools'] = typed_tools

        # Re-create the ChatCompletionRequest with fully typed nested models
        chat_request = ChatCompletionRequest(**chat_request_data)
        # --- End Explicit Deserialization ---

        text_model = _create_text_model(
            chat_request.model, chat_request.get_extra_params().get("adapter_path")
        )

        if not chat_request.stream:
            completion = text_model.generate(chat_request)
            # Recursively serialize the entire completion object for the response
            response_content = recursive_to_dict(completion)
            return JSONResponse(content=response_content)

        # Handling streaming response
        async def event_generator() -> Generator[str, None, None]:
            for chunk in text_model.stream_generate(chat_request):
                # Recursively convert the chunk object to a plain dict structure
                serializable_chunk_dict = recursive_to_dict(chunk)
                # Now json.dumps should work
                yield f"data: {json.dumps(serializable_chunk_dict)}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        import traceback # Import traceback for detailed logging
        print(f"Error during chat completion: {e}")
        traceback.print_exc() # Print the full traceback for debugging
        return JSONResponse(status_code=500, content={"error": str(e)})


# --- Model Caching Logic ---
_last_model_id = None
_last_text_model = None

def _create_text_model(model_id: str, adapter_path: str = None) -> BaseTextModel:
    """Loads or retrieves a cached text model."""
    global _last_model_id, _last_text_model
    cache_key = f"{model_id}_{adapter_path}" if adapter_path else model_id
    if cache_key == _last_model_id:
        return _last_text_model

    print(f"Loading model: {model_id}" + (f" with adapter: {adapter_path}" if adapter_path else ""))
    model = load_model(model_id, adapter_path)
    _last_text_model = model
    _last_model_id = cache_key
    print(f"Model {cache_key} loaded and cached.")
    return model