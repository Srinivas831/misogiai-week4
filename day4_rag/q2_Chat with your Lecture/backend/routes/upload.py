from flask import Blueprint, request, jsonify              # Flask tools for creating APIs
import os                                                  # Python's file and path tools
from werkzeug.utils import secure_filename                 # Ensures uploaded filenames are safe
       
from services.audio_utils import extract_audio_from_video # TEMP: Extract audio after upload (just to test)
from services.transcribe import transcribe_audio
from services.embed_store import embed_transcript
from services.simple_embed import simple_embed_transcript

UPLOAD_FOLDER = "static/videos"                            # Folder to save uploaded videos
ALLOWED_EXTENSIONS = {"mp4", "mov", "mkv"}                 # Allowed video formats for upload

# Create a Blueprint (modular route group) for the upload feature
upload_bp = Blueprint("upload", __name__)

# Function to check if a file has an allowed extension
def allowed_file(filename):
    print("filename",filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the /upload API route (POST method only)
@upload_bp.route("/upload", methods=["POST"])
def upload_video():
    file = request.files['file']
    print("filename",file.filename)
    if "file" not in request.files:
        return jsonify({"error": "Invalid file type"}), 400
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = (file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
        serve_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(serve_path)

        try:
            audio_output_path = serve_path.replace("videos", "audio").replace(".mp4", ".mp3")
            print(f"[🔄] Extracting audio from video...")
            extract_audio_from_video(serve_path, audio_output_path)

            print(f"[🔄] Transcribing audio...")
            transcript_text = transcribe_audio(audio_output_path)
            
            # The transcribe_audio function already saves the transcript to file
            # So we can directly get the transcript path
            filename_base = os.path.basename(audio_output_path).replace(".mp3", ".txt")
            transcript_path = os.path.join("static/transcripts", filename_base)
            
            print(f"[🔄] Embedding transcript...")
            # Try ChromaDB first, fallback to simple embedding
            try:
                embed_result = embed_transcript(transcript_path, collection_name="lecture_chunks")
                if not embed_result:
                    print("[⚠️] ChromaDB embedding failed, trying simple embedding...")
                    embed_result = simple_embed_transcript(transcript_path, collection_name="lecture_chunks")
            except Exception as embed_error:
                print(f"[⚠️] ChromaDB embedding error: {embed_error}")
                print("[🔄] Falling back to simple embedding...")
                embed_result = simple_embed_transcript(transcript_path, collection_name="lecture_chunks")
            
            print(f"[✅] Processing completed successfully!")
            
            if not embed_result:
                return jsonify({"error": "All embedding methods failed"}), 500
            
        except Exception as processing_error:
            print(f"[❌] Processing error: {processing_error}")
            return jsonify({"error": f"Processing failed: {str(processing_error)}"}), 500

        return jsonify({"message": "File uploaded successfully", 
                        "filename": filename}), 200
    
    return jsonify({"error": "Invalid file type"}), 400
