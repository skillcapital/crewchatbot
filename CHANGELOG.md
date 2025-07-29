# Changelog

## [2.0.0] - 2024-01-XX

### 🔒 Security Improvements
- **Removed hardcoded API keys** from `config.py`
- **Added environment variable support** for all sensitive configuration
- **Updated `.gitignore`** to properly exclude sensitive files
- **Created `env.example`** template for environment setup

### 🏗️ Project Restructuring
- **Removed duplicate files**:
  - `setup_api_key.py`
  - `update_api_key.py`
  - `fix_api_key.py`
  - `clean_history.py`
  - `install_requirements.py`
  - `test_api.py`
  - `run_chatbot.py`
  - `API_README.md`
  - `src/chatbot/git ignore` (empty file)

### 📦 Deployment Ready
- **Updated `vercel.json`** with proper environment variable configuration
- **Enhanced `requirements.txt`** with all necessary dependencies
- **Created comprehensive `README.md`** with setup and deployment instructions
- **Added `deploy.md`** with step-by-step GitHub and Vercel deployment guide

### 🔧 Configuration Changes
- **`config.py`**: Now uses `os.getenv()` for all API keys and configuration
- **Environment variables**:
  - `OPENAI_API_KEY` (required)
  - `OPENAI_MODEL` (default: gpt-3.5-turbo)
  - `OPENAI_TEMPERATURE` (default: 0.7)

### 📚 Documentation
- **Updated README.md** with clear setup instructions
- **Added API usage examples** and endpoint documentation
- **Created deployment guide** for GitHub and Vercel
- **Added troubleshooting section** for common issues

### 🚀 New Features
- **GitHub-ready**: No sensitive data in code, proper `.gitignore`
- **Vercel-deployable**: Proper serverless function configuration
- **Environment-based**: Secure configuration management
- **Production-ready**: Structured for deployment and scaling

## Migration Guide

### For Existing Users
1. **Create `.env` file** in project root with your API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

2. **Update any scripts** that reference removed files

3. **Test locally** before deploying:
   ```bash
   python src/chatbot/chatbot.py
   ```

### For New Deployments
1. **Follow `deploy.md`** for step-by-step GitHub and Vercel setup
2. **Set environment variables** in Vercel dashboard
3. **Deploy with confidence** - no sensitive data in code

## Breaking Changes
- ❌ **Removed**: Hardcoded API keys in `config.py`
- ❌ **Removed**: Multiple utility scripts (consolidated functionality)
- ✅ **Added**: Environment variable support
- ✅ **Added**: Proper deployment configuration 