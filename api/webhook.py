from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import only what we need
try:
    from chatbot.chatbot import get_chat_response
except ImportError:
    # Fallback if import fails
    def get_chat_response(message):
        return f"SkillCapital: {message} - CrewAI processing temporarily unavailable."

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Extract message from different possible formats
            user_message = None
            
            # Check for different webhook formats
            if 'message' in request_data:
                user_message = request_data['message']
            elif 'text' in request_data:
                user_message = request_data['text']
            elif 'content' in request_data:
                user_message = request_data['content']
            elif 'query' in request_data:
                user_message = request_data['query']
            elif 'user_message' in request_data:
                user_message = request_data['user_message']
            elif 'input' in request_data:
                user_message = request_data['input']
            
            if not user_message:
                response_data = {
                    'error': 'No message provided',
                    'response': 'Please provide a message in the request body.',
                    'webhook_status': 'error'
                }
            else:
                # Get response from the CrewAI chatbot
                bot_response = get_chat_response(user_message)
                
                response_data = {
                    'response': bot_response,
                    'status': 'success',
                    'webhook_status': 'success',
                    'original_message': user_message,
                    'timestamp': self.get_timestamp()
                }
            
            # Send the response
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'response': 'Sorry, I encountered an error. Please try again.',
                'webhook_status': 'error'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        # Handle GET requests (health check)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = {
            'status': 'online',
            'message': 'SkillCapital CrewAI Webhook is running',
            'endpoints': {
                'POST /api/webhook': 'Send a message to get CrewAI response',
                'GET /api/webhook': 'Health check'
            },
            'supported_formats': [
                '{"message": "your message"}',
                '{"text": "your message"}',
                '{"content": "your message"}',
                '{"query": "your message"}',
                '{"user_message": "your message"}',
                '{"input": "your message"}'
            ]
        }
        
        self.wfile.write(json.dumps(response_data).encode())
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat() 