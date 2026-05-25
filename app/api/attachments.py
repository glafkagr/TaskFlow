import os
import uuid
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.attachment import Attachment
from app.models.task import Task
from app.models.project import Project

attachments_blp = Blueprint('attachments', __name__, url_prefix='/tasks/<int:task_id>/attachments')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@attachments_blp.route('/')
class AttachmentList(MethodView):
    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        # Έλεγχος ότι το task ανήκει στον χρήστη
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        attachments = Attachment.query.filter_by(task_id=task_id).all()

        return jsonify([{
            'id': a.id,
            'filename': a.filename,
            'filesize': a.filesize,
            'created_at': a.created_at.isoformat()
        } for a in attachments]), 200

    @jwt_required()
    def post(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        # Έλεγχος ότι το task ανήκει στον χρήστη
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        # Δημιουργία φακέλου uploads αν δεν υπάρχει
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

        # Αποθήκευση αρχείου με μοναδικό όνομα
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)

        filesize = os.path.getsize(filepath)

        attachment = Attachment(
            filename=original_filename,
            filepath=filepath,
            filesize=filesize,
            task_id=task_id,
            uploaded_by=user_id
        )
        db.session.add(attachment)
        db.session.commit()

        return jsonify({
            'id': attachment.id,
            'filename': attachment.filename,
            'filesize': attachment.filesize,
            'created_at': attachment.created_at.isoformat()
        }), 201

@attachments_blp.route('/<int:attachment_id>')
class AttachmentDetail(MethodView):
    @jwt_required()
    def get(self, task_id, attachment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        attachment = Attachment.query.join(Task).join(Project).filter(
            Attachment.id == attachment_id,
            Attachment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        return jsonify({
            'id': attachment.id,
            'filename': attachment.filename,
            'filesize': attachment.filesize,
            'created_at': attachment.created_at.isoformat()
        }), 200

    @jwt_required()
    def delete(self, task_id, attachment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        attachment = Attachment.query.join(Task).join(Project).filter(
            Attachment.id == attachment_id,
            Attachment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        # Διαγραφή αρχείου από το filesystem
        if os.path.exists(attachment.filepath):
            os.remove(attachment.filepath)

        db.session.delete(attachment)
        db.session.commit()

        return jsonify({'message': 'Attachment deleted successfully'}), 200

@attachments_blp.route('/<int:attachment_id>/download')
class AttachmentDownload(MethodView):
    @jwt_required()
    def get(self, task_id, attachment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        attachment = Attachment.query.join(Task).join(Project).filter(
            Attachment.id == attachment_id,
            Attachment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        from flask import send_file
        return send_file(attachment.filepath, as_attachment=True, download_name=attachment.filename)
