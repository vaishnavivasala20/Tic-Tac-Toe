# Modern Tic-Tac-Toe Game

A modern, feature-rich Tic-Tac-Toe game with both single-player AI and multiplayer online modes, built with Flask, Socket.IO, and Tailwind CSS.

## 🎮 Features

### Single Player Mode
- **AI Opponent**: Play against an intelligent AI
- **Difficulty Levels**:
  - **Easy**: AI makes random moves
  - **Hard**: AI uses Minimax algorithm (unbeatable)
- **Board Sizes**: 3x3, 4x4, and 5x5 boards
- **Winning Conditions**: 3-in-a-row for 3x3, 4-in-a-row for 4x4 and 5x5
- **Turn Indicators**: Clear "Your Turn" and "AI's Turn" indicators
- **Game Results**: Win, Lose, or Draw announcements

### Multiplayer Mode (Online)
- **Real-time Gameplay**: Instant synchronization using Socket.IO
- **Room System**: Create or join game rooms with unique codes
- **Shareable Links**: Direct URL access to game rooms (`/room/CODE`)
- **Player Assignment**: Automatic X/O assignment based on join order
- **Player Limit**: Maximum 2 players per room
- **Chat System**: In-game messaging between players
- **Board Sizes**: 3x3, 4x4, and 5x5 boards
- **Winning Animations**: Highlighted winning combinations

### UI/UX Features
- **Modern Design**: Clean, responsive interface with Tailwind CSS
- **Home Screen**: Choose between Single Player and Multiplayer modes
- **Dynamic Board Rendering**: Adapts to 3x3, 4x4, or 5x5 grids
- **Game Status Display**: Real-time turn and game state information
- **Winning Animations**: Glowing effects for winning combinations
- **Mobile Responsive**: Works on all device sizes
- **Game Over Modal**: Play Again and Exit options

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd tictacteo
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🎯 How to Play

### Single Player Mode
1. **Choose Game Mode**: Click "Single Player" on the home screen
2. **Select Board Size**: Choose 3x3, 4x4, or 5x5
3. **Choose AI Difficulty**: Easy (random) or Hard (unbeatable)
4. **Start Playing**: Click "Start Single Player Game"
5. **Make Moves**: Click on empty cells to place your X
6. **AI Response**: The AI will automatically make its move
7. **Game End**: Win, lose, or draw - then choose to play again

### Multiplayer Mode
1. **Choose Game Mode**: Click "Multiplayer" on the home screen
2. **Select Board Size**: Choose 3x3, 4x4, or 5x5
3. **Create or Join**:
   - **Create Game**: Enter your name and click "Create Game"
   - **Join Game**: Enter room code and your name, then click "Join Game"
4. **Share the Link**: Use "Copy Link" button to share with your friend
5. **Wait for Opponent**: First player waits, second player joins
6. **Play**: Take turns making moves in real-time
7. **Chat**: Use the chat box to communicate with your opponent

### Direct Room Access
- **Shareable URLs**: `http://localhost:5000/room/ABC123`
- **Auto-join**: When someone opens a shared link, they automatically join the room
- **Room Creation**: If the room doesn't exist, it's created automatically

## 🛠️ Technical Details

### Tech Stack
- **Backend**: Flask (Python web framework)
- **Real-time Communication**: Flask-SocketIO
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Tailwind CSS (CDN)
- **WebSocket Library**: Socket.IO client

### Project Structure
```
tictacteo/
├── app.py                 # Flask server with Socket.IO
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── js/
│       └── game.js       # Client-side JavaScript
└── README.md             # This file
```

### Key Features Implementation

#### AI Implementation
- **Easy Mode**: Random selection from available empty cells
- **Hard Mode**: Minimax algorithm with alpha-beta pruning for optimal play
- **Adaptive**: Works with different board sizes (3x3, 4x4, 5x5)

#### Socket.IO Events
- `join_room`: Player joins a game room
- `make_move`: Player makes a move
- `reset_game`: Reset the game board
- `player_joined`: Notify when a player joins
- `game_started`: Start the game when both players are ready
- `move_made`: Broadcast move to all players
- `game_reset`: Reset game state for all players

#### URL Routing
- `/`: Home page with mode selection
- `/room/<room_code>`: Direct room access
- `/api/create-room`: Create a new game room
- `/api/join-room`: Join an existing room
- `/api/room-status/<room_code>`: Check room status

## 🎨 UI Components

### Home Screen
- **Mode Selection**: Single Player vs Multiplayer cards
- **Board Size Options**: Dropdown for 3x3, 4x4, 5x5
- **AI Difficulty**: Easy/Hard selection for single player
- **Modern Design**: Clean cards with hover effects

### Game Screen
- **Dynamic Board**: Grid adapts to selected board size
- **Game Info**: Current player, room code, game mode
- **Sidebar**: Players list and chat system
- **Controls**: Reset, Leave Game, Copy Link buttons

### Game Over Modal
- **Result Display**: Win, Lose, or Draw message
- **Action Buttons**: Play Again or Exit Game
- **Animations**: Smooth transitions and effects

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (default: 'your-secret-key-here')
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: '0.0.0.0')

### Socket.IO Configuration
- **Async Mode**: Threading (compatible with Python 3.13)
- **CORS**: Allowed origins set to "*"
- **Transports**: WebSocket and polling fallback

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```
3. **Run with production server**:
   ```bash
   gunicorn -w 4 -k gevent -b 0.0.0.0:5000 app:app
   ```

### Platform Deployment
- **Render**: Connect your GitHub repository
- **Heroku**: Use the provided `Procfile`
- **Railway**: Deploy directly from GitHub

## 🐛 Troubleshooting

### Common Issues

1. **Socket.IO Connection Failed**
   - Check if the server is running on the correct port
   - Ensure no firewall is blocking the connection
   - Try refreshing the browser page

2. **Room Joining Issues**
   - Verify the room code is correct (case-insensitive)
   - Check browser console for error messages
   - Ensure both players are using the same server

3. **AI Not Responding (Single Player)**
   - Check browser console for JavaScript errors
   - Ensure the game is in "playing" state
   - Try refreshing the page

4. **Board Not Rendering**
   - Check if Tailwind CSS is loading properly
   - Verify JavaScript is enabled in the browser
   - Check browser console for errors

### Debug Mode
The application includes comprehensive logging:
- **Server Logs**: Check terminal for Flask/Socket.IO logs
- **Client Logs**: Open browser console (F12) for JavaScript logs
- **Debug Messages**: Look for `[DEBUG]` prefixed messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎮 Enjoy Playing!

**Features Summary:**
- ✅ Single Player with AI (Easy/Hard difficulty)
- ✅ Multiplayer Online with real-time sync
- ✅ 3x3, 4x4, and 5x5 board sizes
- ✅ Shareable room links
- ✅ Chat system
- ✅ Winning animations
- ✅ Mobile responsive design
- ✅ Modern UI with Tailwind CSS

**Ready to play? Start the server and enjoy your modern Tic-Tac-Toe game! 🎮** 