from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.extensions import db, limiter
from app.extensions import db
from app.models.project import Project
from app.api.schemas import ProjectCreateSchema, ProjectResponseSchema

projects_blp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_blp.route('/')
class ProjectsList(MethodView):
    @limiter.limit("30 per minute")
    @jwt_required()
    @projects_blp.response(200, ProjectResponseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        projects = Project.query.filter_by(user_id=user_id).all()
        return projects

    @limiter.limit("10 per minute")
    @jwt_required()
    @projects_blp.arguments(ProjectCreateSchema)
    @projects_blp.response(201, ProjectResponseSchema)
    def post(self, project_data):
        user_id = get_jwt_identity()
        project = Project(
            name=project_data['name'],
            description=project_data.get('description', ''),
            user_id=user_id
        )
        db.session.add(project)
        db.session.commit()
        return project, 201



@projects_blp.route('/<int:project_id>')
class ProjectDetail(MethodView):
    @jwt_required()
    @projects_blp.response(200, ProjectResponseSchema)
    def get(self, project_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        project = Project.query.filter_by(id=project_id, user_id=user_id).first_or_404()
        return project

    @jwt_required()
    @projects_blp.arguments(ProjectCreateSchema)
    @projects_blp.response(200, ProjectResponseSchema)
    def put(self, project_data, project_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        project = Project.query.filter_by(id=project_id, user_id=user_id).first_or_404()
        project.name = project_data['name']
        project.description = project_data.get('description', '')
        db.session.commit()
        return project

    @jwt_required()
    def delete(self, project_id):
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        project = Project.query.filter_by(id=project_id, user_id=user_id).first_or_404()
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
