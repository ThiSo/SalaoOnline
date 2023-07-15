from app import create_app

app = create_app()

from app_routes import *

if __name__ == '__main__':
    app.run(debug=True)

