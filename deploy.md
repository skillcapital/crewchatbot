# Deployment Guide

## GitHub Setup

### 1. Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: SkillCapital CrewAI Chatbot"
```

### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it `skillcapital-crewai-chatbot`
4. Make it public or private (your choice)
5. Don't initialize with README (we already have one)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/skillcapital-crewai-chatbot.git
git branch -M main
git push -u origin main
```

## Vercel Deployment

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables
```bash
# Set your OpenAI API key
vercel env add OPENAI_API_KEY
# Enter your API key when prompted

# Set other environment variables (optional)
vercel env add OPENAI_MODEL
# Enter: gpt-3.5-turbo

vercel env add OPENAI_TEMPERATURE
# Enter: 0.7
```

### 4. Deploy to Vercel
```bash
vercel --prod
```

### 5. Get Your API URL
After deployment, Vercel will provide you with a URL like:
```
https://your-project-name.vercel.app
```

Your API endpoint will be:
```
https://your-project-name.vercel.app/api/chat
```

## Testing the Deployment

### Test the API
```bash
curl -X POST https://your-project-name.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What courses do you offer?"}'
```

### Expected Response
```json
{
  "response": "We offer various courses including Python, DevOps, AWS, Azure, React.js, and more...",
  "status": "success"
}
```

## Environment Variables Summary

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `OPENAI_MODEL` | OpenAI model to use | No (default: gpt-3.5-turbo) |
| `OPENAI_TEMPERATURE` | Response creativity | No (default: 0.7) |

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   - Make sure you've set the `OPENAI_API_KEY` environment variable in Vercel
   - Check that the API key is valid and has sufficient credits

2. **Deployment Fails**
   - Check that all files are committed to Git
   - Ensure `requirements.txt` is in the root directory
   - Verify `vercel.json` configuration

3. **API Returns Errors**
   - Check Vercel function logs: `vercel logs`
   - Ensure all dependencies are listed in `requirements.txt`

### Useful Commands

```bash
# View deployment logs
vercel logs

# Redeploy
vercel --prod

# View environment variables
vercel env ls

# Remove environment variable
vercel env rm OPENAI_API_KEY
```

## Security Notes

- ✅ API keys are stored as environment variables
- ✅ No sensitive data in the code
- ✅ `.gitignore` excludes sensitive files
- ✅ Vercel environment variables are encrypted

## Next Steps

1. **Custom Domain**: Add a custom domain in Vercel dashboard
2. **Monitoring**: Set up monitoring and alerts
3. **Rate Limiting**: Consider adding rate limiting for production use
4. **Caching**: Implement response caching for better performance 