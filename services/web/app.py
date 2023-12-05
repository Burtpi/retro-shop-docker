from routes.routes import main_bp
from config import app


app.register_blueprint(main_bp)
if __name__ == '__main__':
    

    app.run(host='0.0.0.0', port=5000)
