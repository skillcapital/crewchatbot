# CrewAI Chatbot for SkillCapital

A smart chatbot built with CrewAI framework that provides information about SkillCapital courses, pricing, and curriculum details.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Option 1: Use the installation script
python install_requirements.py

# Option 2: Install manually
pip install -r requirements.txt
```

### 2. Set Up API Key
Create `.env/api_key.txt` file and add your OpenAI API key:
```
sk-your-api-key-here
```

### 3. Run the Chatbot
```bash
# Option 1: Use the run script
python run_chatbot.py

# Option 2: Run directly
python src/chatbot/chatbot.py

# Option 3: Simple chat interface
python src/chatbot/simple_chat.py

# Option 4: Demo mode
python src/chatbot/simple_chat_demo.py
```

## 📁 Project Structure
```
crewai chatbot/
├── .env/
│   └── api_key.txt          # OpenAI API key
├── src/
│   ├── chatbot/
│   │   ├── chatbot.py       # Main chatbot with CrewAI
│   │   ├── simple_chat.py   # Simple chat interface
│   │   ├── simple_chat_demo.py # Demo mode
│   │   └── auto_reload.py   # Live code updates
│   └── website_data/
│       └── course_curriculum.json # Course data
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── install_requirements.py  # Installation script
├── run_chatbot.py          # Easy run script
└── README.md               # This file
```

## 🎯 Features

### ✅ **Smart Course Detection**
- **React.js**: Detects `react`, `reactjs`, `react js`, `javascript`, `js`
- **AWS**: Detects `aws`, `amazon`, `cloud`
- **Azure**: Detects `azure`, `microsoft`
- **Python**: Detects `python`, `programming`
- **DevOps**: Detects `devops`, `development operations`

### ✅ **Structured Responses**
- **Price Queries**: Only shows price (no duration)
- **Duration Queries**: Only shows duration (no price)
- **Course Content**: Shows course name and modules only
- **Greetings**: Concise "Hello, how can I assist you?"

### ✅ **Dual AI System**
- **CrewAI**: For SkillCapital-related queries
- **ChatGPT**: For general questions (smart, human-like responses)

### ✅ **Live Updates**
- **Auto-reload**: Code changes automatically restart the chatbot
- **Live website data**: Fetches real-time information from SkillCapital

## 🔧 Configuration

### API Key Setup
1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Create `.env/api_key.txt` file
3. Add your API key: `sk-your-key-here`

### Environment Variables
```python
# config.py
OPEN_API_KEY = "your-api-key"
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
CHATBOT_NAME = "SkillCapital CrewAI Chatbot"
```

## 📋 Usage Examples

### Course Information
```
You: reactjs course content
Bot: Course: React JS
     Modules:
     • Introduction to React and Modern JavaScript
     • JSX and React Components
     • State and Props Management
     ...

You: aws cloud modules
Bot: Course: AWS Cloud
     Modules:
     • Introduction to Cloud Computing and AWS
     • AWS Fundamentals and Core Services
     ...
```

### Pricing & Duration
```
You: course price
Bot: All courses are priced at ₹ 999 for 30 hours of comprehensive training.

You: duration
Bot: Duration: 30 Hours
```

### General Questions
```
You: What is machine learning?
Bot: [Smart ChatGPT response about machine learning]
```

## 🛠️ Development

### Auto-reload Development Mode
```bash
python src/chatbot/auto_reload.py
```
This will automatically restart the chatbot when you make code changes.

### Testing
```bash
python test_chatbot.py
```

## 📦 Dependencies

### Core AI
- `crewai>=0.148.0` - AI framework
- `langchain>=0.1.0` - Language model integration
- `langchain-openai>=0.3.28` - OpenAI integration
- `openai>=1.93.3` - OpenAI API client

### Web Scraping
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.2` - HTML parsing
- `lxml>=4.9.3` - XML/HTML parser

### Monitoring
- `watchdog>=3.0.0` - File system monitoring

### Search Tools
- `duckduckgo-search>=4.1.1` - Web search
- `tavily-python>=0.3.1` - AI-powered search
- `wikipedia>=1.4.0` - Wikipedia search

## 🚨 Troubleshooting

### Common Issues

1. **Import Error**: Run `python install_requirements.py`
2. **API Key Error**: Check `.env/api_key.txt` file
3. **Module Not Found**: Ensure you're in the project root directory

### Error Messages
- `AuthenticationError`: Check your OpenAI API key
- `FileNotFoundError`: Check file paths and structure
- `ImportError`: Install missing dependencies

## 📝 License

This project is for educational purposes. Please respect OpenAI's usage policies.

---

**Happy Learning! 🎓**