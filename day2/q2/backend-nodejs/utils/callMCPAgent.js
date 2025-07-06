// 🎓 LEARNING: This file bridges Node.js to Proper MCP Tools
const axios = require('axios');

module.exports = async function callMCPAgent(query) {
    console.log("🔵 [Node.js] Calling PROPER MCP Bridge with query:", query);
  
    try {
        // 🎓 LEARNING: HTTP POST to our PROPER MCP Bridge (port 5001)
        const response = await axios.post('http://localhost:5001/chat', {
            query: query
        });
        
        console.log("🔵 [Node.js] Received response from PROPER MCP:", response.data);
        
        // Return the AI response to the frontend
        return response.data.response;
        
    } catch (error) {
        console.error("🔴 [Node.js] Error calling PROPER MCP Bridge:", error.message);
        
        // Return a friendly error message
        return `❌ Sorry, I couldn't process your request. Error: ${error.message}`;
    }
};
  