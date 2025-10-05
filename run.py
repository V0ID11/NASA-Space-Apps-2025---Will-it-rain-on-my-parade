from app import create_app



app = create_app()


if __name__ == '__main__':
    # default to localhost:8000 for local development
    # global USERNAME 
    # global PASSWORD
    # global TOKEN
    # USERNAME, PASSWORD, TOKEN = GetData.load_token()
    
    app.run()
