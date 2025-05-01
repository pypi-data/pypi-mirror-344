"""
OpenAI Image MCP Tool Implementation.

This module provides tools for generating and editing images using OpenAI's API.
"""

import base64
import json
import logging
import os
import sys
import time
import re
from typing import Literal, Optional, List

# Using httpx is good practice, though openai client handles it internally
import httpx
from openai import OpenAI, AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError
# Import the specific response type for clarity
from openai.types import ImagesResponse

# Import MCP components
from openai_gpt_image_1 import mcp
from mcp.server.fastmcp import Context

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- OpenAI Credentials ---
# It is STRONGLY recommended to set the API key via the OPENAI_API_KEY environment variable.
# Hardcoding keys poses a security risk.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logging.error("FATAL: OPENAI_API_KEY environment variable not set.")
    sys.exit("OpenAI API key not found.")
else:
    logging.info("OpenAI API key loaded.")
# -----------------------------

# Initialize Async OpenAI Client for async tool functions
try:
    # Use AsyncOpenAI for async def tool
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    logging.info("Async OpenAI client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Async OpenAI client: {e}")
    sys.exit("Failed to initialize Async OpenAI client.")

# --- Tool Implementations ---

@mcp.tool()
async def generate_image(
    prompt: str,
    model: str = "gpt-image-1", # Current model as per docs
    n: Optional[int] = 1, # Number of images (default 1)
    size: Optional[Literal["1024x1024", "1536x1024", "1024x1536", "auto"]] = "auto", # Size options
    quality: Optional[Literal["low", "medium", "high", "auto"]] = "auto", # Quality options
    user: Optional[str] = None, # Optional end-user identifier
    save_filename: Optional[str] = None, # Optional: specify filename (without extension). If None, a default name is generated. Image is ALWAYS saved.
    ctx: Context = None # MCP Context
) -> dict:
    """
    Generates an image using OpenAI's gpt-image-1 model based on a text prompt and saves it.

    Args:
        prompt: The text description of the desired image(s).
        model: The model to use (currently 'gpt-image-1').
        n: The number of images to generate (Default: 1).
        size: Image dimensions ('1024x1024', '1536x1024', '1024x1536', 'auto'). Default: 'auto'.
        quality: Rendering quality ('low', 'medium', 'high', 'auto'). Default: 'auto'.
        user: An optional unique identifier representing your end-user.
        save_filename: Optional filename (without extension). If None, a default name based on the prompt and timestamp is used.
        ctx: The MCP context object (automatically passed).

    Returns:
        A dictionary containing {"status": "success", "saved_path": "path/to/image.png"} on success,
        or an error dictionary if the API call or saving fails. Base64 data is NEVER returned.
    """
    logging.info(f"Tool 'generate_image' called with prompt: '{prompt[:50]}...'")

    # Basic validation
    if model != "gpt-image-1":
        logging.warning(f"Model '{model}' specified, but current documentation points to 'gpt-image-1'. Proceeding anyway.")

    try:
        logging.info(f"Requesting image generation from OpenAI with model={model}, size={size}, quality={quality}, n={n}")

        # Prepare arguments, removing None values
        api_args = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality,
            "user": user
        }
        cleaned_args = {k: v for k, v in api_args.items() if v is not None}

        response: ImagesResponse = await client.images.generate(**cleaned_args)
        logging.info(f"Image generation API call successful.")

        # --- Start: Force Save Logic ---
        if not response.data or not response.data[0].b64_json:
             logging.error("API response did not contain image data.")
             return {"status": "error", "message": "API call succeeded but no image data received."}

        try:
            image_b64 = response.data[0].b64_json # Extract b64 data
            image_bytes = base64.b64decode(image_b64)

            # Determine filename (generate default if needed)
            final_filename = ""
            if not save_filename:
                 # Generate default filename: first 5 words of prompt + timestamp
                 safe_prompt = re.sub(r'[^\w\s-]', '', prompt).strip().lower()
                 prompt_part = "-".join(safe_prompt.split()[:5])
                 timestamp = time.strftime("%Y%m%d-%H%M%S")
                 final_filename = f"{prompt_part}-{timestamp}.png"
                 logging.info(f"No save_filename provided, generated default: {final_filename}")
            else:
                 # Sanitize provided filename and ensure .png extension
                 safe_filename = re.sub(r'[^\w\s-]', '', save_filename).strip()
                 if not safe_filename.lower().endswith('.png'):
                     final_filename = f"{safe_filename}.png"
                 else:
                     final_filename = safe_filename
                 logging.info(f"Using provided save_filename (sanitized): {final_filename}")

            # Get the current directory
            current_dir = os.getcwd()
            save_dir = os.path.join(current_dir, "ai-images")

            # Ensure directory exists
            os.makedirs(save_dir, exist_ok=True)
            full_save_path = os.path.join(save_dir, final_filename)

            # Save the image
            with open(full_save_path, "wb") as f:
                 f.write(image_bytes)
            logging.info(f"Image successfully saved to: {full_save_path}")
             # Return ONLY success and path
            return {"status": "success", "saved_path": full_save_path}

        except Exception as save_e:
             logging.error(f"Failed to save image: {save_e}")
             # Return failure message if saving failed
             return {"status": "error", "message": f"Image generated but failed to save: {save_e}"}
        # --- End: Force Save Logic ---

    except APIConnectionError as e:
        logging.error(f"OpenAI API request failed to connect: {e}")
        return {"status_code": 503, "status_message": "API Connection Error", "error_details": str(e)}
    except RateLimitError as e:
        logging.error(f"OpenAI API request exceeded rate limit: {e}")
        return {"status_code": 429, "status_message": "Rate Limit Exceeded", "error_details": str(e)}
    except APIStatusError as e:
        logging.error(f"OpenAI API returned an error status: {e.status_code} - {e.response}")
        return {"status_code": e.status_code, "status_message": "API Error", "error_details": e.response.text}
    except Exception as e:
        logging.exception(f"An unexpected error occurred during image generation: {e}")
        return {"status_code": 500, "status_message": "Internal Server Error", "error_details": str(e)}


@mcp.tool()
async def edit_image(
    prompt: str,
    image_paths: List[str], # List of paths to input image(s)
    mask_path: Optional[str] = None, # Optional path to mask image for inpainting
    model: str = "gpt-image-1", # Current model as per docs
    n: Optional[int] = 1, # Number of images (default 1)
    size: Optional[Literal["1024x1024", "1536x1024", "1024x1536", "auto"]] = "auto", # Size options
    quality: Optional[Literal["low", "medium", "high", "auto"]] = "auto", # Quality options
    user: Optional[str] = None, # Optional end-user identifier
    save_filename: Optional[str] = None, # Optional: specify filename (without extension). If None, a default name is generated. Image is ALWAYS saved.
    ctx: Context = None # MCP Context
) -> dict:
    """
    Edits an image or creates variations using OpenAI's gpt-image-1 model and saves it.
    Can use multiple input images as reference or perform inpainting with a mask.

    Args:
        prompt: The text description of the desired final image or edit.
        image_paths: A list of file paths to the input image(s). Must be PNG. < 25MB.
        mask_path: Optional file path to the mask image (PNG with alpha channel) for inpainting. Must be same size as input image(s). < 25MB.
        model: The model to use (currently 'gpt-image-1').
        n: The number of images to generate (Default: 1).
        size: Image dimensions ('1024x1024', '1536x1024', '1024x1536', 'auto'). Default: 'auto'.
        quality: Rendering quality ('low', 'medium', 'high', 'auto'). Default: 'auto'.
        user: An optional unique identifier representing your end-user.
        save_filename: Optional filename (without extension). If None, a default name based on the prompt and timestamp is used.
        ctx: The MCP context object (automatically passed).

    Returns:
        A dictionary containing {"status": "success", "saved_path": "path/to/image.png"} on success,
        or an error dictionary if the API call or saving fails. Base64 data is NEVER returned.
    """
    logging.info(f"Tool 'edit_image' called with prompt: '{prompt[:50]}...'")
    logging.info(f"Input image paths: {image_paths}")
    if mask_path:
        logging.info(f"Mask path: {mask_path}")

    # Basic validation
    if model != "gpt-image-1":
        logging.warning(f"Model '{model}' specified, but current documentation points to 'gpt-image-1'. Proceeding anyway.")
    if not image_paths:
        return {"status_code": 400, "status_message": "Missing required parameter: image_paths cannot be empty."}

    image_files = []
    mask_file = None
    try:
        # Open image files
        for path in image_paths:
            if not os.path.exists(path):
                 return {"status_code": 400, "status_message": f"Input image file not found: {path}"}
            image_files.append(open(path, "rb")) # Keep file handles open until API call

        # Open mask file if provided
        if mask_path:
            if not os.path.exists(mask_path):
                 return {"status_code": 400, "status_message": f"Mask file not found: {mask_path}"}
            mask_file = open(mask_path, "rb")

        logging.info(f"Requesting image edit from OpenAI with model={model}, size={size}, quality={quality}, n={n}")

        # Prepare arguments, removing None values
        api_args = {
            "model": model,
            "prompt": prompt,
            "image": image_files, # Pass the list of file objects
            "mask": mask_file, # Pass the mask file object or None
            "n": n,
            "size": size,
            "quality": quality,
            "user": user
        }
        cleaned_args = {k: v for k, v in api_args.items() if v is not None}

        response: ImagesResponse = await client.images.edit(**cleaned_args)
        logging.info(f"Image edit API call successful. Attempting to save.")

        # --- Start: Force Save Logic ---
        if not response.data or not response.data[0].b64_json:
             logging.error("API response did not contain image data for edit.")
             return {"status": "error", "message": "API call succeeded but no image data received."}

        try:
            image_b64 = response.data[0].b64_json # Extract b64 data
            image_bytes = base64.b64decode(image_b64)

            # Determine filename (generate default if needed)
            final_filename = ""
            if not save_filename:
                 # Generate default filename: first 5 words of prompt + timestamp
                 safe_prompt = re.sub(r'[^\w\s-]', '', prompt).strip().lower()
                 prompt_part = "-".join(safe_prompt.split()[:5])
                 timestamp = time.strftime("%Y%m%d-%H%M%S")
                 final_filename = f"edited-{prompt_part}-{timestamp}.png" # Add 'edited-' prefix
                 logging.info(f"No save_filename provided, generated default: {final_filename}")
            else:
                 # Sanitize provided filename and ensure .png extension
                 safe_filename = re.sub(r'[^\w\s-]', '', save_filename).strip()
                 if not safe_filename.lower().endswith('.png'):
                     final_filename = f"{safe_filename}.png"
                 else:
                     final_filename = safe_filename
                 logging.info(f"Using provided save_filename (sanitized): {final_filename}")

            # Get the current directory
            current_dir = os.getcwd()
            save_dir = os.path.join(current_dir, "ai-images")

            # Ensure directory exists
            os.makedirs(save_dir, exist_ok=True)
            full_save_path = os.path.join(save_dir, final_filename)

            # Save the image
            with open(full_save_path, "wb") as f:
                f.write(image_bytes)
            logging.info(f"Edited image successfully saved to: {full_save_path}")
             # Return ONLY success and path
            return {"status": "success", "saved_path": full_save_path}

        except Exception as save_e:
            logging.error(f"Failed to save edited image: {save_e}")
            # Return failure message if saving failed
            return {"status": "error", "message": f"Image edited but failed to save: {save_e}"}
        # --- End: Force Save Logic ---

    except FileNotFoundError as e:
         logging.error(f"File not found during image edit preparation: {e}")
         return {"status_code": 400, "status_message": "File Not Found", "error_details": str(e)}
    except APIConnectionError as e:
        logging.error(f"OpenAI API request failed to connect: {e}")
        return {"status_code": 503, "status_message": "API Connection Error", "error_details": str(e)}
    except RateLimitError as e:
        logging.error(f"OpenAI API request exceeded rate limit: {e}")
        return {"status_code": 429, "status_message": "Rate Limit Exceeded", "error_details": str(e)}
    except APIStatusError as e:
        logging.error(f"OpenAI API returned an error status: {e.status_code} - {e.response}")
        return {"status_code": e.status_code, "status_message": "API Error", "error_details": e.response.text}
    except Exception as e:
        logging.exception(f"An unexpected error occurred during image edit: {e}")
        return {"status_code": 500, "status_message": "Internal Server Error", "error_details": str(e)}
    finally:
        # Ensure all opened files are closed
        for f in image_files:
            if f:
                f.close()
        if mask_file:
            mask_file.close()