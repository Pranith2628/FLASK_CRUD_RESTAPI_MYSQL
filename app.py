from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__)

db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(30), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    def __int__(self, title, description, due_date, status):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "due_date", "status")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/task"
db.init_app(app)
with app.app_context():
    db.create_all()


# 'POST' = creating new data
@app.route('/task', methods=['POST'])
def add_task():
    _json = request.json
    title = _json['title']
    description = _json['description']
    due_date = _json['due_date']
    status = _json['status']
    new_task = Task(title=title, description=description, due_date=due_date, status=status)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"Message": "your Task has been added successfully"})


# 'GET' = reading a single task from the table by using <id>
@app.route('/task/<id>', methods=['GET'])
def task_byid(id):
    if not str.isdigit(id):
        return jsonify(f"Message: The id of the task cannot be a string")
    else:
        data = []
        product = Task.query.get(id)
        if product is None:
            return jsonify(f"No task was found")
        else:
            data = task_schema.dump(product)
            return jsonify(data)


# 'PUT' = updating a single task from the table by using <id>
@app.route('/task/update/<id>', methods=['PUT'])
def update_task_by_id(id):
    data = request.get_json()
    task = Task.query.get(id)
    if data.get('title'):
        task.name = data['title']
    if data.get('description'):
        task.price = data['description']
    if data.get('due_date'):
        task.category = data['due_date']
    if data.get('status'):
        task.status = data['status']
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "your task has been successfully updated"})


# 'DELETE' = deleting a single task from the table by using <id>
@app.route('/task/delete/<id>', methods=['DELETE'])
def delete_task_by_id(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(f"The task has been deleted")


# 'GET' = reading all the data from the table
@app.route('/tasks', methods=['GET'])
def get_task():
    tasks = []
    data = Task.query.all()
    tasks = tasks_schema.dump(data)
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(debug=True)
