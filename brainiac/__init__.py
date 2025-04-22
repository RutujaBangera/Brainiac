from flask import Flask
import boto3
import json
import os

def get_secret():

    secret_name = "brainiac"
    region_name = "ap-south-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


def create_app():
    secrets = get_secret()
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    print(GROQ_API_KEY)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SonalSolaskar"
    secrets = get_secret()
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    print(GROQ_API_KEY)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
