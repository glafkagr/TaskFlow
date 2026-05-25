from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.web import web_bp
from app.models.user import User
from app.extensions import db
from app.models.project import Project
from app.models.task import Task

@web_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('web.dashboard'))
    return render_template('index.html')

@web_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('web.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('web.register_page'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('web.register_page'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('web.dashboard'))

    return render_template('auth/register.html')

@web_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('web.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('web.dashboard'))

        flash('Invalid email or password', 'error')

    return render_template('auth/login.html')

@web_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, projects=projects)

@web_bp.route('/projects/create', methods=['POST'])
@login_required
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')

    project = Project(
        name=name,
        description=description,
        user_id=current_user.id
    )
    db.session.add(project)
    db.session.commit()

    flash('Project created successfully!', 'success')
    return redirect(url_for('web.dashboard'))

@web_bp.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('web.dashboard'))

    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_detail.html', project=project, tasks=tasks)

@web_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('web.dashboard'))

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully', 'success')
    return redirect(url_for('web.dashboard'))

@web_bp.route('/projects/<int:project_id>/tasks/create', methods=['POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('web.dashboard'))

    title = request.form.get('title')
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')

    task = Task(
        title=title,
        description=description,
        priority=priority,
        status='pending',
        project_id=project_id,
        created_by=current_user.id
    )
    db.session.add(task)
    db.session.commit()

    flash('Task created successfully!', 'success')
    return redirect(url_for('web.project_detail', project_id=project_id))



@web_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get_or_404(task.project_id)

    if project.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('web.dashboard'))

    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()

    flash('Task deleted successfully', 'success')
    return redirect(url_for('web.project_detail', project_id=project_id))

@web_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('web.home'))


@web_bp.route('/web/comments/task/<int:task_id>/create', methods=['POST'])
@login_required
def create_comment(task_id):
    content = request.form.get('content')
    task = Task.query.get_or_404(task_id)
    project = Project.query.get_or_404(task.project_id)

    if project.user_id != current_user.id:
        return '', 403

    from app.models.comment import Comment
    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=current_user.id
    )
    db.session.add(comment)
    db.session.commit()

    # Return HTML for the new comment
    return f'''
    <div class="text-xs bg-gray-50 p-1 rounded">
        <span class="font-semibold">{current_user.username}</span>: {content}
    </div>
    '''




@web_bp.route('/web/attachments/task/<int:task_id>/upload', methods=['POST'])
@login_required
def upload_attachment(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get_or_404(task.project_id)

    if project.user_id != current_user.id:
        return '', 403

    import uuid
    import os
    from werkzeug.utils import secure_filename
    from app.models.attachment import Attachment

    file = request.files.get('file')
    if not file:
        return '', 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filepath = os.path.join(upload_dir, unique_filename)
    file.save(filepath)

    attachment = Attachment(
        filename=filename,
        filepath=filepath,
        filesize=os.path.getsize(filepath),
        task_id=task_id,
        uploaded_by=current_user.id
    )
    db.session.add(attachment)
    db.session.commit()

    return f'''
    <div class="text-xs flex justify-between items-center">
        <a href="/web/attachments/{attachment.id}/download" class="text-blue-500 hover:underline">
            📎 {attachment.filename}
        </a>
        <button class="text-red-500 hover:text-red-700"
                hx-delete="/web/attachments/{attachment.id}/delete"
                hx-target="#attachments-{task.id}">
            ×
        </button>
    </div>
    '''


@web_bp.route('/tasks/<int:task_id>/status', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get_or_404(task.project_id)

    if project.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('web.dashboard'))

    new_status = request.form.get('status')
    if new_status in ['pending', 'in_progress', 'completed']:
        task.status = new_status
        db.session.commit()
        flash(f'Task status updated to {new_status}', 'success')

    return redirect(url_for('web.project_detail', project_id=task.project_id))



