# Potential path: pf-reasoning-tool-proj/pf_reasoning_tool/tools/vision_llm_tool.py

import base64
import traceback
from typing import Union, List, Dict, Optional

# PromptFlow specific imports
from promptflow.core import tool
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from promptflow.contracts.multimedia import Image # Crucial for input type

# OpenAI specific imports
from openai import AzureOpenAI, OpenAI, APIError # Import APIError for better handling

# --- Helper Function: Get OpenAI Client (Copied/Adapted from reasoning_tool_call.py) ---
# NOTE: Ensure the API version used here is compatible with the vision model deployment!
# (Helper function code remains the same as before - no changes needed here)
def get_client(connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]):
    """
    Creates an OpenAI or AzureOpenAI client from a PromptFlow connection.
    IMPORTANT: Ensure the connection's API version OR the forced version below
               is compatible with the target Azure OpenAI Vision model.
    """
    if not connection:
         raise ValueError("Connection object is required.")

    # Try to get connection details robustly
    try:
        connection_dict = dict(connection)
        conn_api_version = connection_dict.get("api_version") # Get version from connection if possible
        print(f"DEBUG: API Version from Connection: {conn_api_version}")
    except (TypeError, ValueError):
         # Fallback for non-dict-like connections
         connection_dict = {
             "api_key": getattr(connection, 'api_key', None),
             "api_base": getattr(connection, 'api_base', None), # Used for Azure endpoint if azure_endpoint missing
             "azure_endpoint": getattr(connection, 'azure_endpoint', None),
             "api_version": getattr(connection, 'api_version', None),
         }
         conn_api_version = connection_dict.get("api_version")
         print(f"DEBUG: API Version from Connection (fallback): {conn_api_version}")

    api_key = connection_dict.get("api_key")
    if not api_key:
        raise ValueError("API key is missing in the connection.")

    # Determine if it's standard OpenAI or Azure OpenAI based on key/endpoint
    is_azure = bool(connection_dict.get("azure_endpoint") or connection_dict.get("api_base")) and not api_key.startswith("sk-")

    if not is_azure:
        # Standard OpenAI Connection
        print("DEBUG: Creating standard OpenAI client.")
        conn_params = {
            "api_key": api_key,
            # Allow overriding base_url for OpenAI compatible endpoints
            "base_url": connection_dict.get("api_base") or connection_dict.get("azure_endpoint")
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return OpenAI(**client_args)
    else:
        # Azure OpenAI Connection
        print("DEBUG: Creating Azure OpenAI client.")
        azure_endpoint = connection_dict.get("azure_endpoint") or connection_dict.get("api_base")
        if not azure_endpoint:
             raise ValueError("Azure endpoint ('azure_endpoint' or 'api_base') is missing in the Azure connection.")

        # --- API Version Handling for Azure ---
        # Prioritize version from connection, fall back to a known compatible one if needed.
        # Check Azure docs for the specific version required by your *vision model deployment*.
        # Example compatible versions: "2024-02-01", "2024-03-01-preview", "2024-02-15-preview"
        api_version_to_use = conn_api_version or "2024-02-15-preview" # <<< ADJUST AS NEEDED
        print(f"INFO: Using Azure OpenAI API Version for Vision Tool: {api_version_to_use}")
        # --------------------------------------

        conn_params = {
            "api_key": api_key,
            "azure_endpoint": azure_endpoint,
            "api_version": api_version_to_use,
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return AzureOpenAI(**client_args)


# === Main PromptFlow Tool Function for Vision ===
@tool
def vision_llm(
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection],
    deployment_name: str, # e.g., "gpt-4-vision-preview", "your-gpt4v-deployment"
    prompt: str,
    images: List[Image], # Accepts the list of Image objects directly
    max_tokens: int = 1000, # Note: OpenAI uses max_tokens for vision models
    temperature: float = 0.7, # <<< Added temperature parameter
    # Optional: Add other parameters like top_p if needed
) -> str:
    """
    Calls an Azure OpenAI vision-capable model (like GPT-4 Turbo with Vision).

    Takes a text prompt and a list of PromptFlow Image objects as input.
    Formats the request using Base64 encoding for the images.

    Args:
        connection: The AzureOpenAI or OpenAI connection object.
        deployment_name: The specific deployment name of the vision model.
        prompt: The text prompt to send along with the images.
        images: A list of promptflow.contracts.multimedia.Image objects.
                Typically the output of a previous tool like 'prepare_pf_image_input'.
        max_tokens: The maximum number of tokens to generate in the response.
        temperature (float): Controls randomness. Lower values make the output more deterministic.
                             Value between 0.0 and 2.0. Defaults to 0.7.

    Returns:
        The text response generated by the vision model.
    """
    if not images:
        print("Warning: No images provided to vision_llm tool. Proceeding with text prompt only.")
        # Decide if you want to error out or proceed without images
        # raise ValueError("At least one image is required for the vision_llm tool.")

    client = get_client(connection)

    # --- Construct the messages payload for the Vision API ---
    content_list = []

    # 1. Add the text prompt
    content_list.append({"type": "text", "text": prompt})
    print(f"DEBUG: Added text prompt to content list.")

    # 2. Add each image using Base64 encoding
    for i, img_obj in enumerate(images):
        try:
            if not isinstance(img_obj, Image):
                 print(f"Warning: Item {i} in the 'images' list is not a PromptFlow Image object. Skipping.")
                 continue # Skip this item

            img_bytes = img_obj.value
            mime_type = img_obj.mime_type

            if not img_bytes:
                print(f"Warning: Image object {i} has empty bytes. Skipping.")
                continue

            if not mime_type or not mime_type.startswith("image/"):
                mime_type = "image/jpeg" # Default if needed
                print(f"Warning: Image object {i} lacked a valid image MIME type. Defaulting to '{mime_type}'.")

            base64_image = base64.b64encode(img_bytes).decode('utf-8')
            image_url_payload = f"data:{mime_type};base64,{base64_image}"

            content_list.append({
                "type": "image_url",
                "image_url": {"url": image_url_payload}
            })
            print(f"DEBUG: Added image {i} (MIME: {mime_type}, Size: {len(img_bytes)} bytes) to content list.")

        except Exception as e:
            print(f"Error processing image {i}: {e}")
            traceback.print_exc()
            print(f"Skipping image {i} due to processing error.")
            continue

    if len(content_list) <= 1 and images:
         raise ValueError("Failed to process any of the provided images for the API call.")

    messages = [{"role": "user", "content": content_list}]
    print(f"--- DEBUG: Final 'messages' payload structure for API call (Image data omitted for brevity): ---")
    # (Debug printing for messages remains the same)
    print(f"[{{'role': 'user', 'content': [")
    for item in content_list:
        if item['type'] == 'text':
            print(f"  {item},")
        else:
            # Get mime type and length again for logging clarity if needed
            b64_len = len(item['image_url']['url'].split(',')[-1])
            mime = item['image_url']['url'].split(';')[0].split(':')[-1]
            print(f"  {{'type': 'image_url', 'image_url': {{'url': 'data:{mime};base64,...len={b64_len}...'}}}} ,")
    print(f"]}}]")
    print(f"--- DEBUG: End Payload Structure ---")


    # --- LLM Call ---
    try:
        api_params = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature, # <<< Added temperature to API parameters
            "model": deployment_name,
            # Add other parameters like 'top_p' here if needed
        }
        # Print params excluding messages for cleaner logs
        print(f"API Call Parameters (excluding key/image data): { {k:v for k,v in api_params.items() if k != 'messages'} }")

        response = client.chat.completions.create(**api_params)

        if response.choices and response.choices[0].message:
            result_text = response.choices[0].message.content
            print(f"DEBUG: LLM Response received.")
            return result_text
        else:
            raise ValueError("Received an empty or invalid response from the API.")

    except APIError as e:
        print(f"OpenAI API Error calling LLM: {e}")
        raise RuntimeError(f"Azure OpenAI API error: {e.status_code} - {e.message}") from e
    except Exception as e:
        print(f"Generic Error calling LLM: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise e