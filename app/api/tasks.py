from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.extensions import db
from app.models.task import Task
from app.models.project import Project
from app.api.schemas import TaskCreateSchema, TaskResponseSchema

tasks_blp = Blueprint('tasks', __name__, url_prefix='/tasks')

# @tasks_blp.route('/')
# class TasksList(MethodView):
#     @jwt_required()
#     @tasks_blp.response(200, TaskResponseSchema(many=True))
#     def get(self):
#         user_id = get_jwt_identity()
#         if isinstance(user_id, str):
#             user_id = int(user_id)

#         # Φιλτράρισμα by project (optional)
#         # Θα το κάνουμε αργότερα
#         tasks = Task.query.join(Project).filter(Project.user_id == user_id).all()
#         return tasks

@tasks_blp.route('/')
class TasksList(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        query = Task.query.join(Project).filter(Project.user_id == user_id)

        project_id = request.args.get('project_id', type=int)
        if project_id:
            query = query.filter(Task.project_id == project_id)

        status = request.args.get('status')
        if status:
            query = query.filter(Task.status == status)

        tasks = query.all()

        # Serialize with comments and attachments
        result = []
        for task in tasks:
            task_dict = TaskResponseSchema().dump(task)
            task_dict['comments'] = [{'id': c.id, 'content': c.content, 'username': c.author.username} for c in task.comments]
            task_dict['attachments'] = [{'id': a.id, 'filename': a.filename, 'filesize': a.filesize} for a in task.attachments]
            result.append(task_dict)

        return result, 200
# @tasks_blp.route('/')
# class TasksList(MethodView):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         if isinstance(user_id, str):
#             user_id = int(user_id)

#         query = Task.query.join(Project).filter(Project.user_id == user_id)

#         # Φιλτράρισμα
#         project_id = request.args.get('project_id', type=int)
#         if project_id:
#             query = query.filter(Task.project_id == project_id)

#         status = request.args.get('status')
#         if status:
#             query = query.filter(Task.status == status)

#         tasks = query.all()
#         return TaskResponseSchema(many=True).dump(tasks), 200

    @jwt_required()
    @tasks_blp.arguments(TaskCreateSchema)
    @tasks_blp.response(201, TaskResponseSchema)
    def post(self, task_data):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        # Έλεγχος ότι το project ανήκει στον χρήστη
        project = Project.query.filter_by(id=task_data['project_id'], user_id=user_id).first_or_404()
        
        task = Task(
            title=task_data['title'],
            description=task_data.get('description', ''),
            status=task_data.get('status', 'pending'),
            priority=task_data.get('priority', 'medium'),
            due_date=task_data.get('due_date'),
            project_id=task_data['project_id'],
            assigned_to=task_data.get('assigned_to'),
            created_by=user_id
        )
        db.session.add(task)
        db.session.commit()
        return task, 201

@tasks_blp.route('/<int:task_id>')
class TaskDetail(MethodView):
    @jwt_required()
    @tasks_blp.response(200, TaskResponseSchema)
    def get(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()
        return task

    @jwt_required()
    @tasks_blp.arguments(TaskCreateSchema)
    @tasks_blp.response(200, TaskResponseSchema)
    def put(self, task_data, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()
        
        task.title = task_data['title']
        task.description = task_data.get('description', '')
        task.status = task_data.get('status', task.status)
        task.priority = task_data.get('priority', task.priority)
        task.due_date = task_data.get('due_date', task.due_date)
        task.assigned_to = task_data.get('assigned_to', task.assigned_to)
        
        db.session.commit()
        return task

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200

@tasks_blp.route('/<int:task_id>/status')
class TaskStatus(MethodView):
    @jwt_required()
    def patch(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()
        
        from flask import request
        data = request.get_json()
        task.status = data.get('status', task.status)
        db.session.commit()
        
        return jsonify({'message': 'Status updated', 'status': task.status}), 200
