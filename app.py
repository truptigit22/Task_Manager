from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
def get_tasks():
    tasks = Task.query.all()
    task_list = [{"id": task.id, "title": task.title, "description": task.description,
                  "deadline": task.deadline, "time": task.time, "priority": task.priority} for task in tasks]
    return jsonify(task_list)

# API: Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        deadline=data['deadline'],
        time=data['time'],
        priority=data['priority']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

# API: Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

