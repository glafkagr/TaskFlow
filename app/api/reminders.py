from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.models.task import Task
from app.models.user import User
from app.celery_worker import celery

reminders_blp = Blueprint('reminders', __name__, url_prefix='/reminders')

@reminders_blp.route('/task/<int:task_id>')
class TaskReminder(MethodView):
    @jwt_required()
    def post(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        user = User.query.get(task.assigned_to)
        if not user:
            return jsonify({'error': 'Assignee not found'}), 404

        # Send email reminder using Celery
        celery.send_task('send_task_reminder', args=[
            user.email,
            task.title,
            task.due_date.isoformat() if task.due_date else 'No due date'
        ])

        return jsonify({'message': 'Reminder queued successfully'}), 202

@reminders_blp.route('/daily-summary')
class DailySummary(MethodView):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        # Send daily summary using Celery
        celery.send_task('send_daily_summary', args=[user_id])

        return jsonify({'message': 'Daily summary queued successfully'}), 202
