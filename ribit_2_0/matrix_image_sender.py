"""
Matrix Image Sender for Ribit 2.0
Handles uploading and sending images to Matrix rooms
"""

import logging
import mimetypes
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

async def send_image_to_room(client, room_id: str, image_path: str, description: str = "") -> bool:
    """
    Send an image file to a Matrix room
    
    Args:
        client: Matrix AsyncClient instance
        room_id: The room ID to send the image to
        image_path: Path to the image file
        description: Optional description/caption for the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from nio import UploadResponse
        
        # Check if file exists
        file_path = Path(image_path)
        if not file_path.exists():
            logger.error(f"Image file not found: {image_path}")
            return False
        
        # Get file info
        file_size = file_path.stat().st_size
        mime_type = mimetypes.guess_type(image_path)[0] or 'image/png'
        
        logger.info(f"Uploading image: {image_path} ({file_size} bytes, {mime_type})")
        
        # Read file
        with open(image_path, 'rb') as f:
            file_data = f.read()
        
        # Upload to Matrix server
        upload_response, _ = await client.upload(
            file_data,
            content_type=mime_type,
            filename=file_path.name,
            filesize=file_size
        )
        
        if not isinstance(upload_response, UploadResponse):
            logger.error(f"Failed to upload image: {upload_response}")
            return False
        
        logger.info(f"Image uploaded successfully: {upload_response.content_uri}")
        
        # Send image message
        content = {
            "msgtype": "m.image",
            "body": description or file_path.name,
            "url": upload_response.content_uri,
            "info": {
                "size": file_size,
                "mimetype": mime_type,
            }
        }
        
        # Try to get image dimensions if possible
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                width, height = img.size
                content["info"]["w"] = width
                content["info"]["h"] = height
        except Exception as e:
            logger.debug(f"Could not get image dimensions: {e}")
        
        # Send the message
        response = await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content=content
        )
        
        logger.info(f"Image sent to room {room_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending image to Matrix: {e}")
        return False

