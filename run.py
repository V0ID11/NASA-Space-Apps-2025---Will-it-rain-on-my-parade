from app import create_app
import DataUnderstanding
from DataUnderstanding import GetData


app = create_app()


if __name__ == '__main__':
    # default to localhost:8000 for local development
    global USERNAME 
    global PASSWORD
    global TOKEN
    USERNAME = "lockie_sam"
    PASSWORD = "1fy6pJqE401w2OoAK1WR"
    TOKEN = GetData.get_token(username=USERNAME, password=PASSWORD)


    app.run()
