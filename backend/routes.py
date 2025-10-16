from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Comment, Task
from .schemas import comment_schema, comments_schema

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json() or {}
    errors = comment_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    task = Task.query.get(data['task_id'])
    if not task:
        task = Task(id=data['task_id'], title=f'Task {data["task_id"]}')
        db.session.add(task)
        db.session.flush()

    comment = Comment(task_id=data['task_id'], author=data['author'], content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return comment_schema.jsonify(comment), 201

@bp.route('/comments', methods=['GET'])
def list_comments():
    task_id = request.args.get('task_id', type=int)
    query = Comment.query
    if task_id:
        query = query.filter_by(task_id=task_id)
    comments = query.order_by(Comment.created_at.asc()).all()
    return comments_schema.jsonify(comments), 200

@bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json() or {}
    errors = comment_schema.validate({**data, 'task_id': comment.task_id})
    if errors:
        return jsonify({'errors': errors}), 400

    comment.author = data.get('author', comment.author)
    comment.content = data.get('content', comment.content)
    db.session.commit()
    return comment_schema.jsonify(comment), 200

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200
