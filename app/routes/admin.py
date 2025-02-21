import os
from werkzeug.utils import secure_filename
from flask import Blueprint, flash, redirect, render_template, url_for, request, jsonify, current_app
from flask_login import login_required
from app.models import Content, db
from app.forms import ContentForm
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'location': url_for('static', filename=f'uploads/{filename}', _external=True)
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploads_dir = os.path.join(current_app.static_folder, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, filename)
        file.save(file_path)
        return f'/static/uploads/{filename}'
    return None

@admin.route('/dashboard')
@login_required
def dashboard():
    contents = Content.query.order_by(Content.updated_at.desc()).all()
    return render_template('admin/dashboard.html', contents=contents)

@admin.route('/content/<int:id>', methods=['GET'])
@login_required
def get_content(id):
    content = Content.query.get_or_404(id)
    return jsonify({
        'id': content.id,
        'title': content.title,
        'content': content.body,
        'status': content.status or 'published',
        'external_link': content.external_link,
        'image_url': content.image_url,
        'updated_at': content.updated_at.strftime('%Y-%m-%d %H:%M:%S') if content.updated_at else None
    })

@admin.route('/content', methods=['POST'])
@admin.route('/content/<int:id>', methods=['POST'])
@login_required
def manage_content(id=None):
    try:
        # Validate required fields
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not title.strip():
            return jsonify({'error': 'Title is required'}), 400
        if not content or not content.strip():
            return jsonify({'error': 'Content is required'}), 400
            
        if id:
            content_obj = Content.query.get_or_404(id)
        else:
            content_obj = Content()
            db.session.add(content_obj)
        
        content_obj.title = title
        content_obj.body = content
        content_obj.status = request.form.get('status', 'published')
        content_obj.external_link = request.form.get('external_link')
        content_obj.page = request.form.get('page', 'home')
        content_obj.updated_at = datetime.utcnow()
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url = save_image(file)
                if image_url:
                    content_obj.image_url = image_url
        
        db.session.commit()
        
        return jsonify({
            'id': content_obj.id,
            'message': 'Content saved successfully',
            'title': content_obj.title,
            'status': content_obj.status
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error saving content: {str(e)}")  # Log the error
        return jsonify({'error': 'Failed to save content. Please try again.'}), 500

@admin.route('/content/<int:id>', methods=['DELETE'])
@login_required
def delete_content(id):
    content = Content.query.get_or_404(id)
    try:
        db.session.delete(content)
        db.session.commit()
        return jsonify({'message': 'Content deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin.route('/formatting-help')
@login_required
def formatting_help():
    return render_template('admin/formatting_help.html')