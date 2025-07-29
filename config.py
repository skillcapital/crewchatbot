import os
from typing import List

# OpenAI Configuration - Use environment variables for security
OPEN_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# Website Configuration
WEBSITE_URL = "https://www.skillcapital.ai"

# Exit phrases for the chatbot
EXIT_PHRASES = [
    'exit', 'quit', 'bye', 'goodbye', 'stop', 'end', 'close'
]

# Chatbot name
CHATBOT_NAME = "SkillCapital CrewAI Chatbot"

# Validate API key
if not OPEN_API_KEY:
    print("Warning: No OpenAI API key found. Please set OPENAI_API_KEY environment variable.") 