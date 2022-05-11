import os
from dotenv import load_dotenv

load_dotenv()
import jwt


def create_token(user):
    "Return signed JWT from user data."
    print("**************", user)
    token = jwt.encode({"username": user}, os.environ['SECRET_KEY'], algorithm="HS256")

    return token