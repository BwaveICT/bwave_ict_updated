from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask import url_for
from app import app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/admin/tinymce_upload', methods=['POST'])
def tinymce_upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Return the URL of the uploaded image
        image_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({'location': image_url}), 200
    else:
        return jsonify({'message': 'Invalid file format'}), 400



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
