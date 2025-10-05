from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import string
import json
import logging
import threading
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Game rooms storage
game_rooms = {}

def generate_room_code():
    """Generate a random 6-character room code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_game_room(board_size=3, move_time_limit=5):
    """Create a new game room"""
    room_code = generate_room_code()
    while room_code in game_rooms:
        room_code = generate_room_code()
    
    game_rooms[room_code] = {
        'board_size': board_size,
        'board': [[None for _ in range(board_size)] for _ in range(board_size)],
        'current_player': 'X',
        'players': [],
        'game_status': 'waiting',  # waiting, playing, finished
        'winner': None,
        'winning_cells': [],
        'win_length': 3 if board_size == 3 else 4,
        'move_time_limit': move_time_limit,  # seconds
        'move_timer': None,
        'move_timer_expiry': None
    }
    
    logger.info(f"Created room {room_code} with board size {board_size} and move time {move_time_limit}s")
    return room_code

def check_winner(board, win_length):
    """Check for a winner in the board"""
    size = len(board)
    
    # Check rows
    for row in range(size):
        for col in range(size - win_length + 1):
            line = board[row][col:col + win_length]
            if all(cell and cell == line[0] for cell in line):
                winning_cells = [(row, col + i) for i in range(win_length)]
                return line[0], winning_cells
    
    # Check columns
    for col in range(size):
        for row in range(size - win_length + 1):
            line = [board[row + i][col] for i in range(win_length)]
            if all(cell and cell == line[0] for cell in line):
                winning_cells = [(row + i, col) for i in range(win_length)]
                return line[0], winning_cells
    
    # Check diagonals
    for row in range(size - win_length + 1):
        for col in range(size - win_length + 1):
            # Main diagonal
            main_diag = [board[row + i][col + i] for i in range(win_length)]
            if all(cell and cell == main_diag[0] for cell in main_diag):
                winning_cells = [(row + i, col + i) for i in range(win_length)]
                return main_diag[0], winning_cells
            
            # Anti-diagonal
            anti_diag = [board[row + i][col + win_length - 1 - i] for i in range(win_length)]
            if all(cell and cell == anti_diag[0] for cell in anti_diag):
                winning_cells = [(row + i, col + win_length - 1 - i) for i in range(win_length)]
                return anti_diag[0], winning_cells
    
    # Check for draw
    if all(all(cell is not None for cell in row) for row in board):
        return 'draw', []
    
    return None, []

@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')

@app.route('/room/<room_code>')
def room_page(room_code):
    """Handle direct room access via URL"""
    room_code = room_code.upper()
    logger.info(f"Direct room access: {room_code}")
    
    if room_code not in game_rooms:
        # Create the room if it doesn't exist
        logger.info(f"Creating room {room_code} from URL access")
        game_rooms[room_code] = {
            'board_size': 3,  # Default board size
            'board': [[None for _ in range(3)] for _ in range(3)],
            'current_player': 'X',
            'players': [],
            'game_status': 'waiting',
            'winner': None,
            'winning_cells': [],
            'win_length': 3
        }
    
    return render_template('index.html', room_code=room_code)

@app.route('/api/create-room', methods=['POST'])
def create_room():
    try:
        data = request.get_json()
        logger.info(f"Create room request: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        board_size = data.get('board_size', 3)
        move_time_limit = data.get('move_time_limit', 5)
        room_code = create_game_room(board_size, move_time_limit)
        
        logger.info(f"Room created: {room_code}")
        return jsonify({'room_code': room_code})
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/join-room', methods=['POST'])
def join_room_api():
    try:
        data = request.get_json()
        logger.info(f"Join room request: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        room_code = data.get('room_code', '').upper()
        
        if not room_code:
            return jsonify({'error': 'Room code is required'}), 400
        
        # Create room if it doesn't exist (for URL-based joining)
        if room_code not in game_rooms:
            logger.info(f"Creating room {room_code} from join request")
            game_rooms[room_code] = {
                'board_size': 3,  # Default board size
                'board': [[None for _ in range(3)] for _ in range(3)],
                'current_player': 'X',
                'players': [],
                'game_status': 'waiting',
                'winner': None,
                'winning_cells': [],
                'win_length': 3
            }
        
        room = game_rooms[room_code]
        if len(room['players']) >= 2:
            logger.warning(f"Room {room_code} is full")
            return jsonify({'error': 'Room is full'}), 400
        
        logger.info(f"Join room success: {room_code}")
        return jsonify({'success': True, 'room_code': room_code})
    except Exception as e:
        logger.error(f"Error joining room: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/room-status/<room_code>')
def room_status(room_code):
    """Get room status for URL-based joining"""
    room_code = room_code.upper()
    if room_code in game_rooms:
        room = game_rooms[room_code]
        return jsonify({
            'exists': True,
            'player_count': len(room['players']),
            'game_status': room['game_status'],
            'board_size': room['board_size']
        })
    else:
        return jsonify({'exists': False})

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")
    # Remove player from all rooms they might be in
    for room_code, room in game_rooms.items():
        room['players'] = [p for p in room['players'] if p['id'] != request.sid]
        
        if len(room['players']) == 0:
            # Delete empty room
            del game_rooms[room_code]
            logger.info(f"Deleted empty room: {room_code}")
        else:
            # Notify remaining players
            emit('player_left', {'players': room['players']}, room=room_code)

@socketio.on('join_room')
def handle_join_room(data):
    try:
        logger.info(f"Join room socket event: {data}")
        room_code = data['room_code'].upper()
        player_name = data.get('player_name', f'Player {len(game_rooms.get(room_code, {"players": []})["players"]) + 1}')
        
        # Create room if it doesn't exist (for URL-based joining)
        if room_code not in game_rooms:
            logger.info(f"Creating room {room_code} from socket join")
            game_rooms[room_code] = {
                'board_size': 3,  # Default board size
                'board': [[None for _ in range(3)] for _ in range(3)],
                'current_player': 'X',
                'players': [],
                'game_status': 'waiting',
                'winner': None,
                'winning_cells': [],
                'win_length': 3
            }
        
        room = game_rooms[room_code]
        
        if len(room['players']) >= 2:
            logger.warning(f"Room {room_code} is full in socket join")
            emit('error', {'message': 'Room is full'})
            return
        
        # Assign player symbol
        player_symbol = 'X' if len(room['players']) == 0 else 'O'
        player_id = request.sid
        
        room['players'].append({
            'id': player_id,
            'name': player_name,
            'symbol': player_symbol
        })
        
        join_room(room_code)
        logger.info(f"Player {player_name} joined room {room_code} as {player_symbol}")
        
        # Notify all players in the room
        emit('player_joined', {
            'player_name': player_name,
            'symbol': player_symbol,
            'players': room['players']
        }, room=room_code)
        
        # Start game if two players joined
        if len(room['players']) == 2:
            room['game_status'] = 'playing'
            logger.info(f"Game started in room {room_code}")
            emit('game_started', {
                'board': room['board'],
                'current_player': room['current_player'],
                'players': room['players'],
                'move_time_limit': room['move_time_limit']
            }, room=room_code)
            start_move_timer(room_code)
    except Exception as e:
        logger.error(f"Error in join_room socket: {e}")
        emit('error', {'message': str(e)})

@socketio.on('make_move')
def handle_make_move(data):
    try:
        logger.info(f"Make move event: {data}")
        room_code = data['room_code'].upper()
        row = data['row']
        col = data['col']
        player_id = request.sid
        
        if room_code not in game_rooms:
            logger.error(f"Room {room_code} not found for move")
            return
        
        room = game_rooms[room_code]
        
        # Find the player
        player = None
        for p in room['players']:
            if p['id'] == player_id:
                player = p
                break
        
        if not player or player['symbol'] != room['current_player']:
            logger.warning(f"Invalid move: not player's turn")
            emit('error', {'message': 'Not your turn'})
            return
        
        # Check if cell is empty
        if room['board'][row][col] is not None:
            logger.warning(f"Invalid move: cell already occupied")
            emit('error', {'message': 'Cell already occupied'})
            return
        
        # Make the move
        room['board'][row][col] = player['symbol']
        logger.info(f"Move made: {player['symbol']} at ({row}, {col})")
        
        # Check for winner
        winner, winning_cells = check_winner(room['board'], room['win_length'])
        
        if winner:
            room['game_status'] = 'finished'
            room['winner'] = winner
            room['winning_cells'] = winning_cells
            logger.info(f"Game finished: {winner} wins")
            # Cancel timer
            if room.get('move_timer'):
                room['move_timer'].cancel()
        else:
            # Switch players
            room['current_player'] = 'O' if room['current_player'] == 'X' else 'X'
            start_move_timer(room_code)
        
        # Broadcast the move to all players in the room
        emit('move_made', {
            'row': row,
            'col': col,
            'symbol': player['symbol'],
            'current_player': room['current_player'],
            'game_status': room['game_status'],
            'winner': room['winner'],
            'winning_cells': room['winning_cells']
        }, room=room_code)
        
        # Emit timer started event for the next player
        if room['game_status'] == 'playing':
            emit('timer_started', {
                'move_time_limit': room['move_time_limit']
            }, room=room_code)
    except Exception as e:
        logger.error(f"Error in make_move: {e}")
        emit('error', {'message': str(e)})

@socketio.on('reset_game')
def handle_reset_game(data):
    try:
        logger.info(f"Reset game event: {data}")
        room_code = data['room_code'].upper()
        
        if room_code not in game_rooms:
            logger.error(f"Room {room_code} not found for reset")
            return
        
        room = game_rooms[room_code]
        board_size = room['board_size']
        
        # Reset the game
        room['board'] = [[None for _ in range(board_size)] for _ in range(board_size)]
        room['current_player'] = 'X'
        room['game_status'] = 'playing'
        room['winner'] = None
        room['winning_cells'] = []
        
        logger.info(f"Game reset in room {room_code}")
        emit('game_reset', {
            'board': room['board'],
            'current_player': room['current_player']
        }, room=room_code)
        
        # Start timer for first player after reset
        start_move_timer(room_code)
    except Exception as e:
        logger.error(f"Error in reset_game: {e}")

def start_move_timer(room_code):
    room = game_rooms.get(room_code)
    if not room or room['game_status'] != 'playing':
        return

    # Cancel existing timer
    if room.get('move_timer'):
        room['move_timer'].cancel()

    move_time_limit = room.get('move_time_limit', 5)
    room['move_timer_expiry'] = time.time() + move_time_limit

    def timer_expired():
        logger.info(f"Move timer expired in room {room_code}")
        skip_turn(room_code)

    timer = threading.Timer(move_time_limit, timer_expired)
    room['move_timer'] = timer
    timer.start()

def skip_turn(room_code):
    room = game_rooms.get(room_code)
    if not room or room['game_status'] != 'playing':
        return

    # Switch player
    room['current_player'] = 'O' if room['current_player'] == 'X' else 'X'
    emit('turn_skipped', {
        'current_player': room['current_player']
    }, room=room_code)
    
    # Start timer for the next player
    start_move_timer(room_code)
    
    # Emit timer started event
    emit('timer_started', {
        'move_time_limit': room['move_time_limit']
    }, room=room_code)

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)