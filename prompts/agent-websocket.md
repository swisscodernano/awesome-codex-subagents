# /agent-websocket

Real-time communication specialist for WebSocket systems.

## Capabilities
- WebSocket protocols
- Socket.io implementation
- Real-time messaging
- Pub/Sub patterns
- Connection management
- Scaling strategies

## Server (Node.js)

```javascript
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const io = new Server(server, {
  cors: { origin: '*' },
  transports: ['websocket', 'polling']
});

// Redis adapter for scaling
const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));

// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = verifyToken(token);
    socket.user = user;
    next();
  } catch (err) {
    next(new Error('Authentication failed'));
  }
});

// Connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.user.id}`);

  // Join rooms
  socket.join(`user:${socket.user.id}`);

  // Handle events
  socket.on('message', (data) => {
    io.to(data.room).emit('message', {
      user: socket.user,
      text: data.text,
      timestamp: Date.now()
    });
  });

  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.user.id}`);
  });
});
```

## Client

```javascript
import { io } from 'socket.io-client';

const socket = io('wss://api.example.com', {
  auth: { token: 'jwt-token' },
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 5
});

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('message', (data) => {
  console.log('Message:', data);
});

socket.emit('message', { room: 'general', text: 'Hello!' });
```

## Scaling

```
1. Use Redis adapter for multi-instance
2. Sticky sessions for load balancer
3. Horizontal scaling with Kubernetes
4. Connection pooling
5. Message compression
```
