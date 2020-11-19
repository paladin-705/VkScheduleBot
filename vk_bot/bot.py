from app import app as application

if __name__ == "__main__":
    application.run(
        host=application.config['SERVER_IP'],
        port=application.config['SERVER_PORT']
    )
