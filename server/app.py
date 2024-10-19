from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST'])
def get_messages():

    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response(jsonify(messages), 200)

    elif request.method == 'POST':
        data = request.json
        new_message = Message(
            body=data['body'], 
            username=data['username'],
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
            )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)



@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        return make_response ({"message": "Message not found"}, 400)

    else:
        if request.method == 'GET':
            return make_response(jsonify(message.to_dict()), 200)

        elif request.method == 'PATCH':
            for attr in request.json:
                setattr(message, attr, request.json.get(attr))

            db.session.commit()
            return make_response(jsonify(message.to_dict()), 200)

        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            return make_response({"delete_successful":True, "message": "Message deleted"}, 200)

if __name__ == '__main__':
    app.run(port=5555)
