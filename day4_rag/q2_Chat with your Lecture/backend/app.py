from flask import Flask
from flask_cors import CORS
from routes.upload import upload_bp

app=Flask(__name__)
CORS(app)

# Increase timeout for long-running operations
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Register Blueprints — this tells Flask to use the upload route from routes/upload.py
app.register_blueprint(upload_bp)


if __name__ == "__main__":
    app.run(debug=True)
