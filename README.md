# SkillCapital CrewAI Chatbot

A sophisticated AI-powered chatbot built with CrewAI that provides information about SkillCapital courses, technical guidance, and general assistance.

## Features

- **Multi-Agent System**: Uses specialized agents for different types of queries
  - Course Advisor Agent: Handles SkillCapital course inquiries
  - Research Agent: Provides general information and research
  - Technical Expert Agent: Offers programming and technical guidance
- **Course Information**: Detailed curriculum and pricing for SkillCapital courses
- **Real-time Responses**: Powered by OpenAI's GPT models
- **Web API**: RESTful API for integration with web applications
- **Auto-reload**: Configuration hot-reloading during development

## Project Structure

```
crewai-chatbot/
├── api/                    # Vercel deployment files
│   ├── chat.py            # API endpoint handler
│   └── requirements.txt   # API dependencies
├── src/
│   ├── chatbot/
│   │   └── chatbot.py     # Main chatbot logic
│   └── website_data/
│       └── course_curriculum.json  # Course data
├── config.py              # Configuration (uses env vars)
├── requirements.txt       # Main dependencies
├── vercel.json           # Vercel deployment config
└── README.md
```

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd crewai-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_TEMPERATURE=0.7
   ```

4. **Run the chatbot**
   ```bash
   python src/chatbot/chatbot.py
   ```

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Set environment variables in Vercel**
   ```bash
   vercel env add OPENAI_API_KEY
   # Enter your OpenAI API key when prompted
   ```

4. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

## API Usage

### Endpoint: `/api/chat`

**Method:** POST

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What courses do you offer?"
}
```

**Response:**
```json
{
  "response": "We offer various courses including Python, DevOps, AWS, Azure, React.js, and more...",
  "status": "success"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `OPENAI_TEMPERATURE` | Response creativity (0-1) | `0.7` |

## Security Notes

- API keys are stored as environment variables, not in code
- The `.gitignore` file excludes sensitive files
- Never commit API keys or secrets to version control

## Available Courses

The chatbot can provide information about:
- Python Programming
- DevOps Engineering
- AWS Cloud Computing
- Microsoft Azure
- React.js Development
- UI/UX Design
- HTML & CSS
- Terraform Infrastructure
- Kubernetes
- Site Reliability Engineering (SRE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the GitHub repository.