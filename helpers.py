import jwt
import os
import uuid
import requests
from app import app

# Generate JWT token
def generate_jwt(user_id):
    payload = {"user_id": user_id}
    jwt_token = jwt.encode(payload, "secret_key", algorithm="HS256")
    return jwt_token


# Verify JWT token
def verify_jwt(jwt_token):
    try:
        payload = jwt.decode(jwt_token, "secret_key", algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None

# Generate a unique filename with actual extension
def generate_unique_filename(filename):
    filename, extension = os.path.splitext(filename)
    return str(uuid.uuid4()) + extension

# Download image from url and save it in /static/media folder
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
            f.write(response.content)
    else:
        raise Exception("Failed to download image")