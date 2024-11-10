from flask import Flask, request, send_file, render_template, jsonify
import os
import csv
from src.algo import process_algo  # Make sure to import process_algo correctly

app = Flask(__name__, static_folder='static', template_folder='static')

# Paths for temporary files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """Render the main page for task upload and processing."""
    return render_template('index.html')

@app.route('/process-task', methods=['POST'])
def process_task():
    """Handle CSV upload, process the addresses, and return the result as JSON."""
    if 'task' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    # Save uploaded file
    file = request.files['task']
    file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_task.csv')
    file.save(file_path)

    print("Map has been saved to 'optimized_route_map.html'")
    try:
        # Read the CSV file and extract addresses
        addresses = []
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the header row
            for row in reader:
                # Assuming that address is from column index 3 onward
                address_parts = row[3:]
                address = ', '.join(address_parts).strip()
                addresses.append(address)

        if len(addresses) < 2:
            return jsonify({"success": False, "error": "At least two addresses are required"}), 400

        print(addresses)
        # Process the addresses and get the output path
        processed_task_path = process_algo(addresses)

        # Send JSON response with processed task URL
        # The URL should be relative to the static folder
        return jsonify({"success": True, "processedRoute": f"/{processed_task_path}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, ssl_context=('ssl/fullchain.pem', 'ssl/privkey.pem'))
