from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime,timedelta
 
api = Blueprint('api', __name__, url_prefix='/api/v1') 

TEST_ITEM = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2023-02-27T00:00:00",
    "created_at": "2023-02-20T00:00:00",
    "updated_at": "2023-02-20T00:00:00"
}
 
@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


@api.route('/todos', methods=['GET'])
def get_todos():
    # -todos = Todo.query.all()
    # request = []
    # for todo in todos:
    #     request.append(todo.to_dict())
    # return jsonify(request)

    todos = Todo.query
    # 1.filter `completed=true`
    if request.args.get('completed') == 'true':
        todos = todos.filter_by(completed=True)

    # 2.filter `window=5`
    if 'window' in request.args:
        try:
            days = int(request.args['window'])
            cutoff = datetime.utcnow() + timedelta(days=days)
            todos = todos.filter(Todo.deadline_at <= cutoff)
        except ValueError:
            return jsonify({'error': 'Invalid window value'}), 400

    todos = todos.all()
    response = [todo.to_dict() for todo in todos]
    return jsonify(response)

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({
            'error':'Todo not found'
        }),404
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    allowed_fields = {'title', 'description', 'completed', 'deadline_at'}
    for field in data.keys():
        if field not in allowed_fields:
            return jsonify({'error': f'Unknown field: {field}'}), 400
        
    todo = Todo(
        title = data['title'],
        description = data.get('description'),
        completed = data.get('completed', False)
    )
    if 'deadline_at' in request.json:
        todo.deadline_at = datetime.fromisoformat(data['deadline_at'])

    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if todo is None:
        return jsonify({'error':'Todo not found'}),404
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()

    if 'id' in data and data['id'] != todo_id:
        return jsonify({'error': 'ID cannot be modified'}), 400
    
    allowed_fields = {'title', 'description', 'completed'}
    for field in data.keys():
        if field not in allowed_fields:
            return jsonify({'error': f'Unknown field: {field}'}), 400
    
    # request.json.get('key',default) (if does not exist, use defalut)
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    todo.deadline_at = data.get('deadline_at',todo.deadline_at)
    db.session.commit()
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error':'Todo not found'}),200
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify(todo.to_dict()),200
