# 🎮 TicTacToe PWA - Advanced Multiplayer Game

A modern, installable Progressive Web App (PWA) featuring an advanced Tic-Tac-Toe game with AI and real-time multiplayer support.

## ✨ Features

### 🎯 Game Modes
- **Single Player vs AI**: Play against intelligent AI with Easy/Hard difficulty levels
- **Multiplayer**: Real-time multiplayer games with room codes
- **Multiple Board Sizes**: 3x3, 4x4, and 5x5 boards with different win conditions

### ⏱️ Timer System
- **Move Timer**: Configurable time limits (2s, 3s, 5s, 10s) for multiplayer games
- **Auto-skip**: Automatic turn skipping when time runs out
- **Visual Countdown**: Color-coded timer with progress bar

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Framer Motion powered transitions and effects
- **PWA Support**: Installable on Android/iOS home screens
- **Offline Support**: Single player mode works without internet

### 🚀 PWA Features
- **Installable**: Add to home screen on mobile devices
- **Offline Capable**: Works without internet connection
- **Fast Loading**: Optimized for performance
- **Native Feel**: App-like experience

### 💬 Social Features
- **Real-time Chat**: In-game messaging for multiplayer
- **Emoji Reactions**: Quick emoji responses
- **Room Sharing**: Easy room code sharing

## 🛠️ Technology Stack

- **Frontend**: React 18 + Vite
- **Styling**: Tailwind CSS + Framer Motion
- **Routing**: React Router DOM
- **Real-time**: Socket.IO Client
- **PWA**: Vite PWA Plugin
- **Icons**: Lucide React
- **Backend**: Flask + Socket.IO (existing)

## 📱 Installation & Setup

### Prerequisites
- Node.js 16+ 
- Python 3.8+ (for backend)
- npm or yarn

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

## 🎮 How to Play

### Single Player Mode
1. Enter your name on the home screen
2. Select "Single Player"
3. Choose AI difficulty (Easy/Hard)
4. Play against the AI!

### Multiplayer Mode
1. Enter your name on the home screen
2. Select "Multiplayer"
3. **Create Room**: Set board size and timer, share room code
4. **Join Room**: Enter room code to join existing game
5. Play with friends in real-time!

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── HomeScreen.jsx
│   ├── GameScreen.jsx
│   ├── CreateRoom.jsx
│   ├── JoinRoom.jsx
│   ├── Board.jsx
│   ├── Timer.jsx
│   ├── TurnIndicator.jsx
│   ├── WinAnimation.jsx
│   ├── Chat.jsx
│   └── PlayAgainExit.jsx
├── context/            # React Context providers
│   ├── GameContext.jsx
│   └── MultiplayerContext.jsx
├── ai/                 # AI logic
│   └── aiLogic.js
├── styles/             # CSS styles
│   └── index.css
└── main.jsx           # App entry point

public/
├── manifest.json       # PWA manifest
├── sw.js              # Service worker
└── pwa-*.png          # PWA icons
```

## 🔧 Configuration

### PWA Settings
- **App Name**: TicTacToe PWA
- **Theme Color**: #3b82f6 (Blue)
- **Display Mode**: Standalone
- **Orientation**: Portrait

### Game Settings
- **Board Sizes**: 3x3, 4x4, 5x5
- **Timer Options**: 2s, 3s, 5s, 10s
- **AI Difficulties**: Easy, Hard

## 🚀 Deployment

### Development
```bash
# Start both frontend and backend
npm run dev  # Frontend on :3000
python app.py  # Backend on :5000
```

### Production
```bash
# Build the PWA
npm run build

# Serve the built files
npm run serve
```

## 📱 PWA Installation

### Android
1. Open the app in Chrome
2. Tap the menu (⋮)
3. Select "Add to Home screen"
4. Follow the prompts

### iOS
1. Open the app in Safari
2. Tap the share button
3. Select "Add to Home Screen"
4. Follow the prompts

## 🎯 Game Rules

### 3x3 Board
- Get 3 in a row to win

### 4x4 Board  
- Get 4 in a row to win

### 5x5 Board
- Get 4 in a row to win

### Timer Rules
- Each player has limited time per move
- If time runs out, turn is automatically skipped
- Timer resets for each new turn

## 🔮 Future Enhancements

- [ ] Dark mode support
- [ ] Sound effects and music
- [ ] Tournament mode
- [ ] Leaderboards
- [ ] Custom themes
- [ ] Voice chat integration
- [ ] Spectator mode
- [ ] Replay system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with React and Vite
- Styled with Tailwind CSS
- Animated with Framer Motion
- Icons from Lucide React
- PWA support via Vite PWA Plugin

---

**Ready to play? Start the server and enjoy your modern Tic-Tac-Toe PWA! 🎮** 