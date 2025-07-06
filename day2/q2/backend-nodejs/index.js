const express = require('express');
const cors = require('cors');
const app = express();

// Middleware
app.use(cors()); // Allow frontend to talk to backend
app.use(express.json()); // Parse incoming JSON

// Routes
const agentRoutes = require('./routes/agent');
app.use('/api', agentRoutes);


app.use("/",(req,res)=>{
    res.send("Hello World!!")
})

// Start server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`✅ Backend server running on http://localhost:${PORT}`);
});
