from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.extensions import db
from app.models.comment import Comment
from app.models.task import Task
from app.models.project import Project
from app.api.schemas import CommentCreateSchema, CommentResponseSchema

comments_blp = Blueprint('comments', __name__, url_prefix='/tasks/<int:task_id>/comments')

@comments_blp.route('/')
class CommentsList(MethodView):
    @jwt_required()
    @comments_blp.response(200, CommentResponseSchema(many=True))
    def get(self, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        # Έλεγχος ότι το task ανήκει σε project του χρήστη
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
        return comments

    @jwt_required()
    @comments_blp.arguments(CommentCreateSchema)
    @comments_blp.response(201, CommentResponseSchema)
    def post(self, comment_data, task_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        # Έλεγχος ότι το task ανήκει σε project του χρήστη
        task = Task.query.join(Project).filter(
            Task.id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        comment = Comment(
            content=comment_data['content'],
            task_id=task_id,
            user_id=user_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment, 201

@comments_blp.route('/<int:comment_id>')
class CommentDetail(MethodView):
    @jwt_required()
    @comments_blp.response(200, CommentResponseSchema)
    def get(self, task_id, comment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        comment = Comment.query.join(Task).join(Project).filter(
            Comment.id == comment_id,
            Comment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()
        return comment

    @jwt_required()
    @comments_blp.arguments(CommentCreateSchema)
    @comments_blp.response(200, CommentResponseSchema)
    def put(self, comment_data, task_id, comment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        comment = Comment.query.join(Task).join(Project).filter(
            Comment.id == comment_id,
            Comment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        comment.content = comment_data['content']
        db.session.commit()
        return comment

    @jwt_required()
    def delete(self, task_id, comment_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)

        comment = Comment.query.join(Task).join(Project).filter(
            Comment.id == comment_id,
            Comment.task_id == task_id,
            Project.user_id == user_id
        ).first_or_404()

        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'}), 200
