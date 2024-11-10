from flask import Flask, request, send_file, render_template, jsonify
import os
from src.process_green_areas import process_green_areas

app = Flask(__name__, static_folder='static', template_folder='static')

# Paths for temporary files
INPUT_PATH = 'input_image.jpg'

@app.route('/')
def index():
    """Render the main page for image upload and processing."""
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    """Handle image upload, process the image, and return the result as JSON."""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    # Save uploaded file
    file = request.files['image']
    file.save(INPUT_PATH)

    try:
        # Process the image and get the output path
        processed_image_path = process_green_areas(INPUT_PATH)
        
        # Send JSON response with processed image URL
        # The URL should be relative to the static folder
        return jsonify({"success": True, "processedImageUrl": f"/{processed_image_path}"})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        # Clean up temporary files
        if os.path.exists(INPUT_PATH):
            os.remove(INPUT_PATH)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, ssl_context=('ssl/fullchain.pem', 'ssl/privkey.pem'))
