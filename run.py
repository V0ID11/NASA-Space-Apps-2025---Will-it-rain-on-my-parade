from app import create_app
from ftplib import FTP 



app = create_app()


if __name__ == '__main__':
    # default to localhost:8000 for local development

    ftp = FTP('194.76.27.28')
    ftp.login(user='climate-coders_webdev',passwd='jOjI8f!98a*Atugu4X9dR#1nLk')
    app.run()
