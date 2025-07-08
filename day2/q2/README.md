# Smart Meeting Assistant with AI Scheduling

A comprehensive meeting management system built with **Model Context Protocol (MCP)** that provides intelligent scheduling, conflict detection, and optimal time slot recommendations with AI-powered features.

## 🚀 Features

### Core AI Features
- **Intelligent Meeting Scheduling** with conflict detection
- **Optimal Time Slot Recommendations** based on participant availability
- **Meeting Pattern Analysis** (frequency, duration, productivity trends)
- **Automatic Conflict Resolution** with AI-powered suggestions
- **Participant Workload Balancing** across different time zones
- **Meeting Effectiveness Scoring** and improvement recommendations

### Technical Capabilities
- **Multi-timezone Support** for global teams
- **Work Hours Validation** for each participant
- **Real-time Conflict Detection** with severity scoring
- **AI-powered Insights** for meeting optimization
- **RESTful API** for easy integration
- **MCP Tool Integration** for extensible functionality

## 🏗️ Architecture

The system follows a **3-tier architecture** with MCP integration:

```
Frontend (Web) → Backend (Node.js) → MCP Agent (Python) → OpenAI API
                                   ↓
                              Tools & Data Storage
```

### Components

1. **MCP Agent (Python)** - Core AI engine with FastMCP
2. **Backend (Node.js)** - REST API and HTTP bridge
3. **Frontend** - Web interface (to be implemented)
4. **Data Storage** - JSON-based meeting and user data

## 📁 Project Structure

```
day2/q2/
├── mcp-agent-python/           # Main MCP server implementation
│   ├── server.py              # FastMCP server setup
│   ├── http_server.py         # HTTP bridge for manual tool calling
│   ├── http_server_simple_mcp.py # Proper MCP tool pattern
│   ├── agent.py               # Legacy agent implementation
│   ├── run_server.py          # Server runner (deprecated)
│   ├── tools/                 # MCP tools
│   │   ├── create_meeting.py          # Meeting creation tool
│   │   ├── find_optimal_slots.py      # Optimal scheduling tool
│   │   └── detect_scheduling_conflicts.py # Conflict detection tool
│   └── data/                  # Data storage
│       ├── meetings.json      # Meeting database
│       └── users.json         # User profiles with timezones
├── backend-nodejs/            # Node.js REST API
│   ├── index.js              # Express server
│   ├── routes/agent.js       # API routes
│   └── utils/callMCPAgent.js # MCP bridge utility
└── frontend/                 # Web interface (empty)
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### 1. Python MCP Agent Setup

```bash
cd day2/q2/mcp-agent-python

# Install dependencies
pip install fastmcp flask flask-cors openai python-dotenv pydantic pytz

# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 2. Node.js Backend Setup

```bash
cd day2/q2/backend-nodejs

# Install dependencies
npm install

# Start the backend server
npm run server
```

### 3. Start MCP Agent

```bash
cd day2/q2/mcp-agent-python

# Start the HTTP bridge server (recommended)
python http_server_simple_mcp.py

# Or start the basic FastMCP server
python server.py
```

## 🎯 Usage

### API Endpoints

#### 1. Schedule Meeting
```bash
POST http://localhost:3001/api/schedule-meeting
Content-Type: application/json

{
  "query": "Schedule a meeting with Alice and Bob for 30 minutes on 2024-12-15 at 2 PM"
}
```

#### 2. Find Optimal Slots
```bash
POST http://localhost:3001/api/schedule-meeting
Content-Type: application/json

{
  "query": "Find optimal meeting slots for Alice, Bob, and Charlie for 60 minutes between 2024-12-15 to 2024-12-20"
}
```

#### 3. Detect Conflicts
```bash
POST http://localhost:3001/api/schedule-meeting
Content-Type: application/json

{
  "query": "Check for scheduling conflicts for Alice between 2024-12-15T09:00 to 2024-12-15T17:00"
}
```

### Sample Data

The system comes with pre-populated data:

**Users (5 users across different timezones):**
- Alice (Asia/Kolkata, 09:00-17:00)
- Bob (Europe/London, 08:00-16:00)
- Charlie (America/New_York, 09:00-17:00)
- Diana (Asia/Tokyo, 10:00-18:00)
- Ethan (Australia/Sydney, 08:00-16:00)

**Meetings (8+ sample meetings)** with various participants and time slots.

## 🔧 MCP Tools

### 1. Create Meeting Tool
- **Function**: `create_meeting_tool`
- **Purpose**: Schedule new meetings with conflict validation
- **Parameters**: title, participants, duration, start_time
- **Features**: Auto-generates meeting IDs, validates time formats

### 2. Find Optimal Slots Tool
- **Function**: `find_optimal_slots_tool`
- **Purpose**: AI-powered time slot recommendations
- **Parameters**: participants, duration, date_range
- **Features**: Considers work hours, existing meetings, timezone conflicts

### 3. Detect Scheduling Conflicts Tool
- **Function**: `detect_scheduling_conflicts_tool`
- **Purpose**: Identify and analyze scheduling conflicts
- **Parameters**: user_id, time_range
- **Features**: Severity scoring, workload analysis, improvement suggestions

## 🤖 AI Features

### Conflict Detection
- **Overlapping Meetings**: Identifies double-booked time slots
- **Work Hours Violations**: Flags meetings outside work hours
- **Timezone Conflicts**: Handles cross-timezone scheduling
- **Severity Scoring**: Categorizes conflicts as high/medium/low

### Optimal Scheduling
- **Availability Analysis**: Checks all participants' calendars
- **Work Hours Optimization**: Prioritizes business hours
- **Conflict Avoidance**: Suggests conflict-free time slots
- **AI Reasoning**: Provides explanations for recommendations

### Meeting Insights
- **Workload Analysis**: Calculates meeting load percentages
- **Pattern Recognition**: Identifies scheduling trends
- **Productivity Scoring**: Evaluates meeting effectiveness
- **Improvement Suggestions**: AI-powered recommendations

## 🔄 Development Workflow

### Adding New Tools

1. Create tool function in `tools/` directory
2. Register with MCP registry in `http_server_simple_mcp.py`
3. Add OpenAI function calling schema
4. Test with sample queries

### Testing

```bash
# Test MCP server directly
python -c "from tools.create_meeting import create_meeting; print(create_meeting('Test', ['Alice'], 30, '2024-12-15T14:00:00'))"

# Test HTTP bridge
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Schedule a test meeting"}'

# Test full stack
curl -X POST http://localhost:3001/api/schedule-meeting \
  -H "Content-Type: application/json" \
  -d '{"query": "Schedule a meeting with Alice for 30 minutes tomorrow at 2 PM"}'
```

## 📊 Data Models

### User Model
```json
{
  "id": "u1",
  "name": "Alice",
  "timezone": "Asia/Kolkata",
  "work_hours": ["09:00", "17:00"],
  "calendar": [...]
}
```

### Meeting Model
```json
{
  "id": "m1",
  "title": "Weekly Sync",
  "participants": ["u1", "u2"],
  "start": "2025-07-06T10:00",
  "end": "2025-07-06T11:00"
}
```

## 🚀 Future Enhancements

- [ ] Web frontend implementation
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Real-time notifications
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] Meeting transcription and summarization
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Slack/Teams integration

## 🛡️ Security Considerations

- Environment variables for API keys
- Input validation for all parameters
- Rate limiting for API endpoints
- CORS configuration for frontend access
- Data sanitization for JSON storage

## 📝 License

This project is part of the MisogiAI Week 4 curriculum and is for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions or issues:
- Check the setup instructions
- Review the API documentation
- Test with sample data
- Verify environment variables

---

**Built with ❤️ using MCP, OpenAI, and modern web technologies** 