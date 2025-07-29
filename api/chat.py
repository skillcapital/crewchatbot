from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot.chatbot import get_chat_response

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
            
            # Extract the message from the request
            user_message = request_data.get('message', '')
            
            if not user_message:
                response_data = {
                    'error': 'No message provided',
                    'response': 'Please provide a message to chat with SkillCapital.'
                }
            else:
                # Get response from the chatbot
                bot_response = get_chat_response(user_message)
                
                response_data = {
                    'response': bot_response,
                    'status': 'success'
                }
            
            # Send the response
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'response': 'Sorry, I encountered an error. Please try again.'
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
            'message': 'SkillCapital Chatbot API is running',
            'endpoints': {
                'POST /api/chat': 'Send a message to chat with the bot',
                'GET /api/chat': 'Health check'
            }
        }
        
        self.wfile.write(json.dumps(response_data).encode()) 