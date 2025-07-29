from http.server import BaseHTTPRequestHandler
import json
import os

def get_simple_response(user_message):
    """Simple response function without heavy dependencies"""
    user_message_lower = user_message.lower().strip()
    
    # SkillCapital specific responses
    if any(word in user_message_lower for word in ['hello', 'hi', 'hey']):
        return "👋 Hi! Welcome to SkillCapital - India's #1 Premium Training Platform! How can I assist you today?"
    
    if any(word in user_message_lower for word in ['price', 'cost', 'how much']):
        return "₹ 999 for premium AI-driven training"
    
    if any(word in user_message_lower for word in ['duration', 'how long', 'time']):
        return "30 Hours of comprehensive training"
    
    if any(word in user_message_lower for word in ['course', 'courses']):
        return "We offer Python, DevOps, AWS, Azure, React.js, UI/UX, HTML/CSS, Terraform, Kubernetes, and SRE courses. Which one interests you?"
    
    if any(word in user_message_lower for word in ['python']):
        return "Python Programming Course: Learn Python from basics to advanced concepts. Perfect for beginners and experienced developers."
    
    if any(word in user_message_lower for word in ['aws', 'amazon']):
        return "AWS Cloud Course: Master Amazon Web Services including EC2, S3, Lambda, and more. Get AWS certified!"
    
    if any(word in user_message_lower for word in ['azure', 'microsoft']):
        return "Microsoft Azure Course: Learn cloud computing with Azure services, deployment, and management."
    
    if any(word in user_message_lower for word in ['react', 'javascript']):
        return "React.js Course: Build modern web applications with React, JavaScript, and modern frontend technologies."
    
    if any(word in user_message_lower for word in ['devops']):
        return "DevOps Course: Learn CI/CD, Docker, Kubernetes, and modern deployment practices."
    
    if any(word in user_message_lower for word in ['enroll', 'sign up', 'register']):
        return "Great! To enroll in our courses, visit our website or contact our support team. All courses are ₹999 for 30 hours of premium training."
    
    # Default response
    return "Thank you for your message! I'm here to help with information about SkillCapital courses, pricing, and enrollment. What would you like to know?"

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
                # Get response from the simple chatbot
                bot_response = get_simple_response(user_message)
                
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
            'message': 'SkillCapital Simple Chatbot API is running',
            'endpoints': {
                'POST /api/simple': 'Send a message to chat with the bot',
                'GET /api/simple': 'Health check'
            }
        }
        
        self.wfile.write(json.dumps(response_data).encode()) 