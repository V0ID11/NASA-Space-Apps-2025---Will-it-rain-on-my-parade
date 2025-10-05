from app import create_app
from DataUnderstanding import GetData


app = create_app()


if __name__ == '__main__':
    # default to localhost:8000 for local development
    GetData.load_token()
    app.run()
