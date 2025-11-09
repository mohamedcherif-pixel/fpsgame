// Socket.IO Server for FPS Game Multiplayer
// Deploy this to Glitch.com, Heroku, or any Node.js hosting

const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http, {
    cors: {
        origin: "*", // Allow all origins for global multiplayer
        methods: ["GET", "POST"],
        credentials: true
    },
    // Enhanced options for global connections
    pingTimeout: 60000, // 60 seconds for global connections
    pingInterval: 25000, // 25 seconds
    transports: ['websocket', 'polling'], // Support both transports
    allowEIO3: true // Backward compatibility
});

const PORT = process.env.PORT || 3000;

// Store active rooms
const rooms = new Map();

io.on('connection', (socket) => {
    const clientIP = socket.handshake.address || socket.request.connection.remoteAddress;
    console.log('🌍 Player connected from:', clientIP, 'Socket ID:', socket.id);
    
    // Handle ping for latency measurement
    socket.on('ping', (data) => {
        socket.emit('pong', { timestamp: data.timestamp });
    });
    
    // Create room
    socket.on('createRoom', (data) => {
        const { room } = data;
        socket.join(room);
        rooms.set(room, { host: socket.id, players: [socket.id] });
        console.log(`🏠 Room created: ${room} by ${socket.id} from ${clientIP}`);
    });
    
    // Join room
    socket.on('joinRoom', (data) => {
        const { room } = data;
        const roomData = rooms.get(room);
        
        if (roomData && roomData.players.length < 2) {
            socket.join(room);
            roomData.players.push(socket.id);
            
            // Notify both players
            socket.emit('roomJoined', { success: true, room });
            io.to(room).emit('playerJoined', { 
                room, 
                playerId: socket.id 
            });
            
            console.log(`✅ Player ${socket.id} joined room ${room} from ${clientIP}`);
        } else {
            socket.emit('roomJoined', { success: false, message: 'Room not found or full' });
            console.log(`❌ Failed to join room ${room} - not found or full`);
        }
    });
    
    // Forward game data
    socket.on('gameData', (data) => {
        const { room, data: gameData } = data;
        // Send to everyone in room except sender
        socket.to(room).emit('gameData', {
            from: socket.id,
            data: gameData
        });
    });
    
    // Handle disconnect
    socket.on('disconnect', (reason) => {
        console.log('❌ Player disconnected:', socket.id, 'Reason:', reason);
        
        // Find and clean up rooms
        rooms.forEach((roomData, roomId) => {
            if (roomData.players.includes(socket.id)) {
                io.to(roomId).emit('playerLeft', { playerId: socket.id });
                rooms.delete(roomId);
                console.log(`🗑️ Room ${roomId} cleaned up`);
            }
        });
    });
    
    // Handle connection errors
    socket.on('error', (error) => {
        console.error('❌ Socket error:', error);
    });
});

// Health check endpoint for monitoring
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        rooms: rooms.size,
        timestamp: new Date().toISOString()
    });
});

app.get('/', (req, res) => {
    res.json({
        message: 'FPS Game Multiplayer Server',
        status: 'running',
        activeRooms: rooms.size,
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

// CORS headers for all routes
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

http.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
