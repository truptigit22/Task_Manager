from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

app = Flask(__name__)

# Connect to Redis
redis_client = Redis(host='localhost', port=6379, db=0)

# Configure Flask-Limiter with Redis backend
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model (Database structure)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    deadline = db.Column(db.String(20), nullable=True)  # Date
    time = db.Column(db.String(10), nullable=True)  # Time
    priority = db.Column(db.String(10), nullable=True)

# Initialize database
with app.app_context():
    db.create_all()

# Serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# API: Fetch all tasks
@app.route('/tasks', methods=['GET'])
@limiter.limit("10 per minute")
def get_tasks():
    tasks = Task.query.all()
    task_list = [{"id": task.id, "title": task.title, "description": task.description,
                  "deadline": task.deadline, "time": task.time, "priority": task.priority} for task in tasks]
    return jsonify(task_list)

# API: Fetch a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
@limiter.limit("10 per minute")
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "deadline": task.deadline,
        "time": task.time,
        "priority": task.priority
    })

# API: Add a new task
@app.route('/tasks', methods=['POST'])
@limiter.limit("5 per minute")
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=data.get('deadline', ''),
        time=data.get('time', ''),
        priority=data.get('priority', '')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully", "task_id": new_task.id}), 201

# API: Edit a task
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
@limiter.limit("5 per minute")
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

# API: Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@limiter.limit("5 per minute")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=False)
