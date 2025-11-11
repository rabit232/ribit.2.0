#!/usr/bin/env python3
"""
Set Ribit's Matrix Avatar
Downloads and sets the robot girl GIF as profile picture
"""

import asyncio
import os
import sys
from nio import AsyncClient, UploadResponse
from PIL import Image
import io

async def set_avatar(homeserver, user_id, access_token, avatar_path):
    """
    Set Matrix avatar for Ribit
    
    Args:
        homeserver: Matrix homeserver URL
        user_id: Matrix user ID
        access_token: Matrix access token
        avatar_path: Path to avatar image file
    """
    print(f"🤖 Setting Ribit's Avatar")
    print(f"Homeserver: {homeserver}")
    print(f"User: {user_id}")
    print(f"Avatar: {avatar_path}")
    print()
    
    # Create client
    client = AsyncClient(homeserver, user_id)
    client.access_token = access_token
    
    try:
        # Read avatar file
        with open(avatar_path, 'rb') as f:
            avatar_data = f.read()
        
        print(f"📁 Avatar file size: {len(avatar_data)} bytes")
        
        # Determine content type
        if avatar_path.endswith('.gif'):
            content_type = 'image/gif'
        elif avatar_path.endswith('.png'):
            content_type = 'image/png'
        elif avatar_path.endswith('.jpg') or avatar_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        else:
            content_type = 'image/gif'  # default
        
        print(f"📤 Uploading avatar ({content_type})...")
        
        # Upload avatar
        response, maybe_keys = await client.upload(
            data_provider=lambda: avatar_data,
            content_type=content_type,
            filename=os.path.basename(avatar_path)
        )
        
        if isinstance(response, UploadResponse):
            mxc_url = response.content_uri
            print(f"✅ Avatar uploaded: {mxc_url}")
            
            # Set avatar
            print("🎨 Setting as profile picture...")
            await client.set_avatar(mxc_url)
            
            print("✅ Avatar set successfully!")
            print()
            print("🤖 Ribit now has a robot girl avatar! 🎉")
            
        else:
            print(f"❌ Upload failed: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await client.close()


async def main():
    """Main function"""
    # Get credentials from environment or .env file
    homeserver = os.getenv('MATRIX_HOMESERVER', 'https://matrix.envs.net')
    user_id = os.getenv('MATRIX_USER_ID', '@ribit:envs.net')
    access_token = os.getenv('MATRIX_ACCESS_TOKEN')
    
    if not access_token:
        # Try loading from .env
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            if key == 'MATRIX_ACCESS_TOKEN':
                                access_token = value.strip()
                            elif key == 'MATRIX_HOMESERVER':
                                homeserver = value.strip()
                            elif key == 'MATRIX_USER_ID':
                                user_id = value.strip()
    
    if not access_token:
        print("❌ MATRIX_ACCESS_TOKEN not set!")
        print()
        print("Set it with:")
        print("  export MATRIX_ACCESS_TOKEN='your_token'")
        print()
        print("Or create .env file with:")
        print("  MATRIX_ACCESS_TOKEN=your_token")
        sys.exit(1)
    
    # Avatar path
    avatar_path = os.path.join(os.path.dirname(__file__), 'ribit_avatar.gif')
    
    if not os.path.exists(avatar_path):
        print(f"❌ Avatar file not found: {avatar_path}")
        print()
        print("Download it with:")
        print('  wget "https://media.giphy.com/media/6F4TGyw69QRvVrHgRC/giphy.gif" -O ribit_avatar.gif')
        sys.exit(1)
    
    # Set avatar
    await set_avatar(homeserver, user_id, access_token, avatar_path)


if __name__ == '__main__':
    asyncio.run(main())

