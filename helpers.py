import jwt

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
