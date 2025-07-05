"""
AI Assistant Demo - How AI Connects to Our MCP Server

This simulates exactly how an AI assistant (like Claude or ChatGPT) 
would discover and use our document analysis tools through MCP.

Connection Flow:
1. AI Assistant connects to MCP Server
2. AI discovers available tools  
3. AI calls tools with parameters
4. MCP Server routes calls to our analysis services
5. Results are returned to AI in standard format
"""

import asyncio
import json
import sys
sys.path.append('.')

from proper_mcp_server import ProperDocumentAnalyzerMCPServer

class AIAssistantSimulator:
    """
    Simulates an AI Assistant connecting to our MCP Server
    
    This shows EXACTLY how the connection works:
    AI Assistant ↔ MCP Protocol ↔ Our Server ↔ Analysis Tools
    """
    
    def __init__(self):
        """Initialize the AI assistant simulator"""
        self.server = None
        print("🤖 AI Assistant Simulator starting...")
    
    async def connect_to_mcp_server(self):
        """Step 1: AI Assistant connects to MCP Server"""
        print("\n🔗 Step 1: AI Assistant connecting to MCP Server...")
        
        # In real life, this would be:
        # - AI opens connection (stdio, websocket, etc.)
        # - MCP handshake occurs
        # - Authentication if needed
        
        self.server = ProperDocumentAnalyzerMCPServer()
        print("✅ Connection established!")
        
        return True
    
    async def discover_tools(self):
        """Step 2: AI Assistant discovers what tools are available"""
        print("\n🔍 Step 2: AI Assistant discovering available tools...")
        
        # In real MCP, AI would send: {"method": "tools/list"}
        # Server responds with tool definitions
        
        # Simulate the discovery
        tools = [
            "analyze_document(document_id) - Complete document analysis",
            "get_sentiment(text) - Analyze text sentiment", 
            "extract_keywords(text, limit) - Find important keywords",
            "add_document(title, content, ...) - Store new document",
            "search_documents(query, limit) - Search document library"
        ]
        
        print("📋 AI Assistant discovered these tools:")
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool}")
        
        print("✅ Tool discovery complete!")
        
    async def call_tool_sentiment(self):
        """Step 3a: AI calls get_sentiment tool"""
        print("\n🧠 Step 3a: AI Assistant calls get_sentiment...")
        
        # AI would send MCP request like:
        # {
        #   "method": "tools/call",
        #   "params": {
        #     "name": "get_sentiment", 
        #     "arguments": {"text": "I love this new AI technology!"}
        #   }
        # }
        
        print("📤 AI Request: get_sentiment('I love this new AI technology!')")
        
        # Our server processes the request
        result = await self.server._get_sentiment("I love this new AI technology!")
        
        print("📥 AI Received:")
        print(result[0].text)
        
    async def call_tool_keywords(self):
        """Step 3b: AI calls extract_keywords tool"""
        print("\n🔍 Step 3b: AI Assistant calls extract_keywords...")
        
        sample_text = "Machine learning and artificial intelligence are revolutionizing healthcare by enabling doctors to diagnose diseases more accurately."
        
        print(f"📤 AI Request: extract_keywords('{sample_text[:50]}...', limit=5)")
        
        # Our server processes the request
        result = await self.server._extract_keywords(sample_text, 5)
        
        print("📥 AI Received:")
        print(result[0].text)
    
    async def call_tool_search(self):
        """Step 3c: AI calls search_documents tool"""
        print("\n🔍 Step 3c: AI Assistant calls search_documents...")
        
        print("📤 AI Request: search_documents('Python programming')")
        
        # Our server processes the request
        result = await self.server._search_documents("Python programming", 3)
        
        print("📥 AI Received:")
        print(result[0].text)
    
    async def call_tool_add_document(self):
        """Step 3d: AI calls add_document tool"""
        print("\n📄 Step 3d: AI Assistant calls add_document...")
        
        title = "AI Assistant Created Document"
        content = "This document was created by an AI assistant to demonstrate the MCP connection. It shows how AI can interact with our document analysis tools through the Model Context Protocol."
        
        print(f"📤 AI Request: add_document('{title}', '{content[:50]}...', author='AI Assistant')")
        
        # Our server processes the request
        result = await self.server._add_document(
            title=title,
            content=content,
            author="AI Assistant",
            category="demo",
            tags=["AI", "MCP", "demo"]
        )
        
        print("📥 AI Received:")
        print(result[0].text)
        
        # Extract document ID for next step
        response_text = result[0].text
        if "ID:" in response_text:
            # Find the document ID in the response
            lines = response_text.split('\n')
            for line in lines:
                if "ID:" in line:
                    doc_id = line.split('`')[1] if '`' in line else line.split('ID:')[1].strip()
                    return doc_id
        return None
    
    async def call_tool_analyze(self, document_id):
        """Step 3e: AI calls analyze_document tool"""
        print("\n📊 Step 3e: AI Assistant calls analyze_document...")
        
        if not document_id:
            print("❌ No document ID available")
            return
        
        print(f"📤 AI Request: analyze_document('{document_id[:8]}...')")
        
        # Our server processes the request
        result = await self.server._analyze_document(document_id)
        
        print("📥 AI Received:")
        print(result[0].text)
    
    async def demonstrate_complete_flow(self):
        """Demonstrate the complete AI ↔ MCP ↔ Tools flow"""
        print("🎯 COMPLETE MCP CONNECTION DEMONSTRATION")
        print("=" * 60)
        print("This shows exactly how AI assistants connect to our tools")
        
        # Step 1: Connect
        await self.connect_to_mcp_server()
        
        # Step 2: Discover tools
        await self.discover_tools()
        
        # Step 3: Call various tools (this is where the magic happens!)
        await self.call_tool_sentiment()
        await self.call_tool_keywords()
        await self.call_tool_search()
        
        # Add a document and then analyze it
        document_id = await self.call_tool_add_document()
        await self.call_tool_analyze(document_id)
        
        print("\n" + "=" * 60)
        print("🎉 COMPLETE MCP FLOW DEMONSTRATED!")
        print("✅ AI Assistant successfully used all our tools!")
        
        print("\n🔗 What Just Happened:")
        print("1. 🤖 AI Assistant connected to our MCP Server")
        print("2. 🔍 AI discovered our 5 analysis tools")  
        print("3. 📞 AI called tools by sending MCP requests")
        print("4. ⚙️ MCP Server routed calls to our analysis services")
        print("5. 📊 Our services processed the requests (sentiment, keywords, etc.)")
        print("6. 📤 Results were returned to AI in standard format")
        
        print("\n🌟 This is EXACTLY how Claude, ChatGPT, or any AI assistant")
        print("   would use our Document Analyzer through MCP!")

async def main():
    """Run the AI Assistant demo"""
    ai_simulator = AIAssistantSimulator()
    await ai_simulator.demonstrate_complete_flow()

if __name__ == "__main__":
    asyncio.run(main()) 