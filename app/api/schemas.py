from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

class ProjectCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()

class ProjectResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    owner_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class TaskCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(['pending', 'in_progress', 'review', 'completed']))
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high', 'urgent']))
    due_date = fields.DateTime()
    project_id = fields.Int(required=True)  # ← ΑΥΤΟ ΥΠΑΡΧΕΙ ΉΔΗ
    assigned_to = fields.Int()

class TaskResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    priority = fields.Str()
    due_date = fields.DateTime()
    project_id = fields.Int()
    assigned_to = fields.Int()
    created_by = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class CommentCreateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))

class CommentResponseSchema(Schema):
    id = fields.Int()
    content = fields.Str()
    task_id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
