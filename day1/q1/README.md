# MCP Q&A Chatbot (Practice)

A simple Q&A chatbot for Model Context Protocol (MCP) questions. Backend uses Node.js + Express + OpenAI API. Frontend is a static HTML page.

## Folder Structure

- `backend/` — Express server, OpenAI integration
- `frontend/` — Static HTML/JS chat UI

## Setup

### Backend
1. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```
2. Install dependencies:
   ```
   cd backend
   npm install
   ```
3. Start the server:
   ```
   npm start
   ```
   The backend runs on http://localhost:3001

### Frontend
Just open `frontend/index.html` in your browser.

## Usage
- Ask questions about MCP in the chat box.
- If you ask about something else, the bot will reply: "Sorry, I only answer questions about MCP."

---
This is a practice project for learning purposes. 