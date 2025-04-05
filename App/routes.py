from flask import render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import sys
from Tests.Leaf_Count import count_and_show_leaves
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

def init_routes(app):
    # Configure upload folder
    UPLOAD_FOLDER = 'Asset/Images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/count_leaves', methods=['POST'])
    def process_image():
        if 'image' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            leaf_count = count_and_show_leaves(filepath)

            return jsonify({
                'leaf_count': leaf_count,
                'message': f'Detected {leaf_count} leaves'
            })

        return jsonify({'error': 'Invalid file type'}), 400