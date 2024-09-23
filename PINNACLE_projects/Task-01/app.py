from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
socketio = SocketIO(app)

chat_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    
    send(f"{username} has joined the room.", to=room)
    
    if room not in chat_rooms:
        chat_rooms[room] = []
    
    for message in chat_rooms[room]:
        send(message, to=request.sid)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f"{username} has left the room.", to=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = f"{username}: {data['message']}"
    
    chat_rooms[room].append(message)
    
    send(message, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
