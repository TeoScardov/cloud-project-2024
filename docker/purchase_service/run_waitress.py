from waitress import serve
from app import create_app  # replace with the actual import path

if __name__ == '__main__':
    app = create_app(config_class="production")
    serve(app, host='0.0.0.0', port=4004)
