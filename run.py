from app import create_app


app = create_app()


if __name__ == '__main__':
    # default to localhost:8000 for local development
    app.run(host='127.0.0.1', port=8000, debug=True)
