from marshmallow import Schema, fields, validate

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    task_id = fields.Int(required=True)
    author = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
