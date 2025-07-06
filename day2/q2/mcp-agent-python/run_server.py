# # Flask API to expose MCP agent
# ❌ run_server.py — not needed anymore (FastMCP launches its own server)

# from flask import Flask, request, jsonify
# from agent import run_agent

# app = Flask(__name__)

# # ✅ Health check route
# @app.route("/")
# def index():
#     return "🧠 MCP Agent is running!"

# # ✅ POST route to receive query from Node.js
# @app.route("/run-agent", methods=["POST"])
# def run():
#     data = request.get_json()
#     query = data.get("query")

#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     print(f"📨 Received query: {query}")
#     response = run_agent(query)
#     print(f"📤 Sending response: {response}")

#     return jsonify({"response": response})

# # ✅ Start the server
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
