const express = require('express');
const router = express.Router();
const callMCPAgent = require('../utils/callMCPAgent');

// 🧠 Schedule a new meeting
router.post('/schedule-meeting', async (req, res) => {
  const { query } = req.body;

  console.log('📥 Received query:', query);

  try {
    const response = await callMCPAgent(query);
    console.log("response",response);
    res.json({ result: response });
  } catch (err) {
    console.error('❌ MCP agent call failed:', err.message);
    res.status(500).json({ error: 'MCP agent error' });
  }
});

// Later we’ll add other routes here: /find-optimal-slots, /conflict-check, etc.

module.exports = router;
