import os
from dotenv import load_dotenv

load_dotenv()
import jwt


def create_token(user):
    "Return signed JWT from user data."

    token = jwt.encode({"username": user}, os.environ['SECRET_KEY'], algorithm="HS256")

    return token

def verify_token(token):
    """authenticate user token"""

    payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms="HS256")

    return payload

