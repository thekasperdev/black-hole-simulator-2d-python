from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from datetime import datetime
import uuid

# Import existing functions
from SpaceD_mission_terminal import load_log_content, load_mission_briefing, BANNER

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon-secret-key-2025'
# Use hybrid session management for reliability
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=True)

# Backup session storage for SocketIO reliability
active_sessions = {}

@app.route('/')
def index():
    # Initialize session if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['operator_name'] = None
        session['current_state'] = 'boot'
        session['unlocked_logs'] = 9  # All logs unlocked for hackathon
        session['current_log'] = None
        session['current_mission'] = None
        session.permanent = True  # Make session persistent
    return render_template('terminal.html')

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

def get_session_data():
    """Get session data with fallback to in-memory storage"""
    session_id = session.get('session_id')
    if not session_id:
        return None

    # Try Flask session first
    if all(key in session for key in ['session_id', 'current_state']):
        return {
            'session_id': session['session_id'],
            'operator_name': session.get('operator_name'),
            'current_state': session.get('current_state', 'boot'),
            'unlocked_logs': session.get('unlocked_logs', 9),
            'current_log': session.get('current_log'),
            'current_mission': session.get('current_mission')
        }

    # Fallback to in-memory storage
    return active_sessions.get(session_id)

def update_session_data(data):
    """Update both Flask session and in-memory storage"""
    session_id = session.get('session_id')
    if not session_id:
        return

    # Update Flask session
    for key, value in data.items():
        if key != 'session_id':
            session[key] = value

    # Update in-memory backup
    if session_id not in active_sessions:
        active_sessions[session_id] = {}
    active_sessions[session_id].update(data)

@socketio.on('connect')
def on_connect():
    # Ensure session is initialized
    if 'session_id' not in session:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session['operator_name'] = None
        session['current_state'] = 'boot'
        session['unlocked_logs'] = 9
        session['current_log'] = None
        session['current_mission'] = None
        session.permanent = True

        # Initialize in-memory backup
        active_sessions[session_id] = {
            'session_id': session_id,
            'operator_name': None,
            'current_state': 'boot',
            'unlocked_logs': 9,
            'current_log': None,
            'current_mission': None
        }
    else:
        # Sync existing session to in-memory backup
        session_id = session['session_id']
        active_sessions[session_id] = {
            'session_id': session_id,
            'operator_name': session.get('operator_name'),
            'current_state': session.get('current_state', 'boot'),
            'unlocked_logs': session.get('unlocked_logs', 9),
            'current_log': session.get('current_log'),
            'current_mission': session.get('current_mission')
        }

    print(f"User connected with session: {session.get('session_id', 'unknown')}")

    emit('boot_sequence', {
        'banner': BANNER,
        'message': 'AE-DOS Terminal Ready. Please enter your name, operator:',
        'show_animation': True
    })

@socketio.on('disconnect')
def on_disconnect():
    print(f"User disconnected: {session.get('session_id', 'unknown')}")
    # Keep session data for reconnection

@socketio.on('user_input')
def handle_input(data):
    # Get session data with fallback
    session_data = get_session_data()
    if not session_data:
        print("No session found, reinitializing...")
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session['operator_name'] = None
        session['current_state'] = 'boot'
        session['unlocked_logs'] = 9
        session['current_log'] = None
        session['current_mission'] = None
        session.permanent = True

        active_sessions[session_id] = {
            'session_id': session_id,
            'operator_name': None,
            'current_state': 'boot',
            'unlocked_logs': 9,
            'current_log': None,
            'current_mission': None
        }

        emit('boot_sequence', {
            'banner': BANNER,
            'message': 'AE-DOS Terminal Ready. Please enter your name, operator:',
            'show_animation': True
        })
        return
    
    user_input = data.get('input', '').strip()
    state = session_data.get('current_state', 'boot')

    print(f"Session {session_data['session_id']}: state={state}, input='{user_input}'")

    if state == 'boot':
        if user_input:
            update_session_data({
                'operator_name': user_input,
                'current_state': 'main_menu'
            })
            emit('clear_screen')
            emit('show_main_menu', {
                'operator': user_input,
                'message': f'Welcome aboard, Operator {user_input}.'
            })
    
    elif state == 'main_menu':
        if user_input.upper() in ['1', 'L', 'LOGS']:
            update_session_data({'current_state': 'logs_menu'})
            emit('show_logs_menu', {
                'logs': get_available_logs(session_data['unlocked_logs'])
            })
        elif user_input.upper() in ['2', 'M', 'MISSIONS']:
            update_session_data({'current_state': 'missions_menu'})
            emit('show_missions_menu', {
                'missions': get_available_missions(session_data['unlocked_logs'])
            })
        elif user_input.upper() in ['3', 'Q', 'EXIT']:
            emit('exit_message', {'message': 'Exiting AE-DOS. Goodbye!'})
    
    elif state == 'logs_menu':
        if user_input.isdigit() and 1 <= int(user_input) <= 9:
            log_num = int(user_input)
            if log_num <= session_data['unlocked_logs']:
                update_session_data({
                    'current_log': log_num,
                    'current_state': 'viewing_log'
                })
                content = load_log_content(log_num)
                emit('show_log_content', {
                    'log_number': log_num,
                    'content': content
                })
        elif user_input.upper() == 'M':
            update_session_data({'current_state': 'main_menu'})
            emit('show_main_menu', {
                'operator': session_data.get('operator_name'),
                'message': 'Returned to main menu.'
            })
        elif user_input.upper() == 'Q':
            emit('exit_message', {'message': 'Exiting AE-DOS. Goodbye!'})
    
    elif state == 'viewing_log':
        if user_input == '' or user_input.upper() == 'ENTER':
            # Continue to mission briefing
            log_num = session_data.get('current_log', 1)
            content = load_mission_briefing(log_num)
            update_session_data({'current_state': 'viewing_mission'})
            emit('show_mission_briefing', {
                'mission_number': log_num,
                'content': content,
                'operator': session_data.get('operator_name')
            })
        elif user_input.upper() == 'R':
            # Return to logs menu
            update_session_data({'current_state': 'logs_menu'})
            emit('show_logs_menu', {
                'logs': get_available_logs(session_data['unlocked_logs'])
            })
        elif user_input.upper() == 'L':
            update_session_data({'current_state': 'logs_menu'})
            emit('show_logs_menu', {
                'logs': get_available_logs(session_data['unlocked_logs'])
            })
        elif user_input.upper() == 'M':
            update_session_data({'current_state': 'main_menu'})
            emit('show_main_menu', {
                'operator': session_data.get('operator_name'),
                'message': 'Returned to main menu.'
            })
        elif user_input.upper() == 'Q':
            emit('exit_message', {'message': 'Exiting AE-DOS. Goodbye!'})
    
    elif state == 'viewing_mission':
        if user_input.upper() == 'R':
            # Return to log
            log_num = session_data.get('current_log', 1)
            update_session_data({'current_state': 'viewing_log'})
            content = load_log_content(log_num)
            emit('show_log_content', {
                'log_number': log_num,
                'content': content
            })
        elif user_input.upper() == 'L':
            update_session_data({'current_state': 'logs_menu'})
            emit('show_logs_menu', {
                'logs': get_available_logs(session_data['unlocked_logs'])
            })
        elif user_input.upper() == 'N':
            update_session_data({'current_state': 'missions_menu'})
            emit('show_missions_menu', {
                'missions': get_available_missions(session_data['unlocked_logs'])
            })
        elif user_input.upper() == 'M':
            update_session_data({'current_state': 'main_menu'})
            emit('show_main_menu', {
                'operator': session_data.get('operator_name'),
                'message': 'Returned to main menu.'
            })
        elif user_input.upper() == 'Q':
            emit('exit_message', {'message': 'Exiting AE-DOS. Goodbye!'})
    
    elif state == 'missions_menu':
        if user_input.isdigit() and 1 <= int(user_input) <= 9:
            mission_num = int(user_input)
            if mission_num <= session_data['unlocked_logs']:
                update_session_data({
                    'current_mission': mission_num,
                    'current_state': 'viewing_mission'
                })
                content = load_mission_briefing(mission_num)
                emit('show_mission_briefing', {
                    'mission_number': mission_num,
                    'content': content,
                    'operator': session_data.get('operator_name')
                })
        elif user_input.upper() == 'M':
            update_session_data({'current_state': 'main_menu'})
            emit('show_main_menu', {
                'operator': session_data.get('operator_name'),
                'message': 'Returned to main menu.'
            })
        elif user_input.upper() == 'Q':
            emit('exit_message', {'message': 'Exiting AE-DOS. Goodbye!'})

def get_available_logs(unlocked_count):
    logs = []
    for i in range(1, 10):
        if i <= unlocked_count:
            logs.append({
                'number': i,
                'title': f'LOG {i}: Decrypted. Mission {i} available.',
                'available': True
            })
        else:
            logs.append({
                'number': i,
                'title': f'LOG {i}: [ENCRYPTED] - Requires Mission Key {i}',
                'available': False
            })
    return logs

def get_available_missions(unlocked_count):
    missions = []
    for i in range(1, 10):
        if i <= unlocked_count:
            missions.append({
                'number': i,
                'title': f'MISSION {i}: Available',
                'available': True
            })
        else:
            missions.append({
                'number': i,
                'title': f'MISSION {i}: [LOCKED]',
                'available': False
            })
    return missions

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    # For local development only; in production use Gunicorn/eventlet
    socketio.run(
        app,
        host='0.0.0.0',
        port=port
    )