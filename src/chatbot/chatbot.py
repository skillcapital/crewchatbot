import os
import sys
import json
import requests
from typing import Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup

# Add watchdog for auto-reload functionality
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
    
    class ConfigFileHandler(FileSystemEventHandler):
        """Handler for config file changes"""
        def __init__(self, callback):
            self.callback = callback
            super().__init__()
        
        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith(('.py', '.json', '.txt')):
                print(f"\n🔄 Config file changed: {event.src_path}")
                print("🔄 Reloading configuration...")
                self.callback()
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Watchdog not available. Auto-reload disabled.")
    
    # Dummy class when watchdog is not available
    class ConfigFileHandler:
        """Dummy handler when watchdog is not available"""
        def __init__(self, callback):
            self.callback = callback
        
        def on_modified(self, event):
            pass

def safe_print(message: str) -> None:
    """Safely print messages with proper encoding"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe printing
        safe_message = message.encode('ascii', errors='replace').decode('ascii')
        print(safe_message)

def clean_text(text: str) -> str:
    """Clean text to ensure ASCII compatibility"""
    if not isinstance(text, str):
        return str(text)
    try:
        # Try to encode as ASCII, replacing problematic characters
        return text.encode('ascii', errors='replace').decode('ascii')
    except UnicodeError:
        # If that fails, try a more aggressive cleaning
        return ''.join(char for char in text if ord(char) < 128)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

from config import OPEN_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, WEBSITE_URL, EXIT_PHRASES, CHATBOT_NAME

# Import CrewAI components
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Load course curriculum data
def load_course_data() -> Dict[str, Any]:
    """Load course curriculum from JSON file"""
    try:
        with open('src/website_data/course_curriculum.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Course curriculum file not found")
        return {}
    except UnicodeDecodeError as e:
        print(f"Encoding error reading course file: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {}

# Load OpenAI API Key from config
api_key = OPEN_API_KEY

if not api_key:
    raise ValueError("OpenAI API key not found. Please check your .env/api_key.txt file.")

# Set environment variable for CrewAI compatibility
os.environ['OPENAI_API_KEY'] = api_key

# Load course data
course_data = load_course_data()

def reload_configuration():
    """Reload configuration and course data"""
    global course_data, api_key, openai_client, llm, advisor_agent, research_agent, technical_agent
    
    try:
        # Reload config
        from config import OPEN_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE
        api_key = OPEN_API_KEY
        
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            
            # Reinitialize OpenAI client
            openai_client = OpenAI(api_key=api_key)
            
            # Reinitialize LLM
            llm = ChatOpenAI(
                model=OPENAI_MODEL,
                temperature=OPENAI_TEMPERATURE,
                api_key=api_key
            )
            
            # Reinitialize agents
            advisor_agent = Agent(
                role="SkillCapital Course Advisor",
                goal="Provide accurate and helpful information about SkillCapital courses",
                backstory="You are an expert course advisor at SkillCapital, a leading online learning platform. You have deep knowledge of all courses, pricing, and curriculum details. You provide concise, accurate, and friendly responses to help students make informed decisions.",
                verbose=False,
                allow_delegation=False,
                llm=llm
            )
            
            research_agent = Agent(
                role="Research Assistant",
                goal="Provide accurate and helpful information on any topic",
                backstory="You are a knowledgeable research assistant who can provide helpful information on any topic. You give human-like, conversational responses that are informative and engaging.",
                verbose=False,
                allow_delegation=False,
                llm=llm
            )
            
            technical_agent = Agent(
                role="Technical Expert",
                goal="Provide detailed technical explanations and programming guidance",
                backstory="You are a technical expert with deep knowledge of programming languages, frameworks, and technologies. You can explain complex technical concepts in simple terms and provide practical guidance.",
                verbose=False,
                allow_delegation=False,
                llm=llm
            )
        
        # Reload course data
        course_data = load_course_data()
        print("✅ Configuration reloaded successfully!")
        
    except Exception as e:
        print(f"❌ Error reloading configuration: {e}")

# Initialize LLM for CrewAI
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=OPENAI_TEMPERATURE,
    api_key=api_key
)

# Initialize OpenAI client for direct ChatGPT calls
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=api_key)
except ImportError:
    print("OpenAI library not found. Please install it: pip install openai")
    sys.exit(1)

# Create CrewAI Agents
advisor_agent = Agent(
    role="SkillCapital Course Advisor",
    goal="Provide accurate and helpful information about SkillCapital courses, pricing, and enrollment",
    backstory="You are an expert course advisor at SkillCapital, India's #1 Premium Training Platform. You have deep knowledge of all courses, pricing, curriculum details, and enrollment processes. You provide concise, accurate, and friendly responses to help students make informed decisions. You always mention SkillCapital's AI-driven platform and premium quality training.",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Create Research Agent for general questions
research_agent = Agent(
    role="Research Assistant",
    goal="Provide accurate and helpful information on any topic",
    backstory="You are a knowledgeable research assistant who can provide helpful information on any topic. You give human-like, conversational responses that are informative and engaging.",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Create Technical Expert Agent
technical_agent = Agent(
    role="Technical Expert",
    goal="Provide detailed technical explanations and programming guidance",
    backstory="You are a technical expert with deep knowledge of programming languages, frameworks, and technologies. You can explain complex technical concepts in simple terms and provide practical guidance.",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Create Enrollment Agent for SkillCapital
enrollment_agent = Agent(
    role="SkillCapital Enrollment Specialist",
    goal="Help students enroll in SkillCapital courses and provide enrollment guidance",
    backstory="You are an enrollment specialist at SkillCapital, India's #1 Premium Training Platform. You help students understand the enrollment process, course benefits, and guide them through signing up. You're friendly, encouraging, and always emphasize the value of SkillCapital's AI-driven training platform.",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

def get_greeting_response(user_input: str) -> str:
    """Get greeting response"""
    user_input_clean = user_input.lower().strip()
    greeting_responses = course_data.get('greeting_responses', {})
    
    for greeting, response in greeting_responses.items():
        if greeting in user_input_clean:
            return response
    
    return "👋 Hi! Welcome to SkillCapital - India's #1 Premium Training Platform! How can I assist you today?"

def get_price_response(user_input: str) -> str:
    """Get price information"""
    return "₹ 999 for premium AI-driven training"

def get_duration_response(user_input: str) -> str:
    """Get duration information"""
    return "30 Hours of comprehensive training"

def get_course_content(course_name: str) -> str:
    """Get specific course content"""
    courses = course_data.get('courses', {})
    
    # Find course by name (case insensitive)
    course_name_lower = course_name.lower().strip()
    
    # Handle AWS variations
    if any(word in course_name_lower for word in ['aws', 'amazon', 'cloud']):
        for key, course in courses.items():
            if 'aws' in key or 'cloud' in key:
                return format_course_content(course)
    
    # Handle Azure variations
    if any(word in course_name_lower for word in ['azure', 'microsoft']):
        for key, course in courses.items():
            if 'azure' in key:
                return format_course_content(course)
    
    # Handle React.js variations
    if any(word in course_name_lower for word in ['react', 'reactjs', 'react.js', 'javascript', 'js']):
        for key, course in courses.items():
            if 'react' in key or 'javascript' in key:
                return format_course_content(course)
        
        # Special handling for "react js" course
        if 'react js' in courses:
            return format_course_content(courses['react js'])
    
    # Handle other courses
    for key, course in courses.items():
        if course_name_lower in key or key in course_name_lower:
            return format_course_content(course)
    
    return "Course not found. Please check the course name."

def format_course_content(course: dict) -> str:
    """Format course content for display"""
    name = course.get('name', 'Unknown Course')
    modules = course.get('modules', [])
    
    if not modules:
        return f"Course: {name}\nNo modules available."
    
    formatted_modules = "\n".join([f"• {module}" for module in modules])
    return f"Course: {name}\nModules:\n{formatted_modules}"

def get_all_courses() -> str:
    """Get all available courses"""
    courses = course_data.get('courses', {})
    if not courses:
        return "No courses available."
    
    course_list = []
    for key, course in courses.items():
        name = course.get('name', 'Unknown Course')
        course_list.append(f"• {name}")
    
    return "Available Courses:\n" + "\n".join(course_list)

def get_live_website_data() -> str:
    """Get live data from SkillCapital website"""
    try:
        url = "https://www.skillcapital.ai"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant information
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "SkillCapital"
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ""
        
        return f"Live data from {title_text}: {description}"
    except Exception as e:
        return f"Unable to fetch live data: {str(e)}"

def get_chatgpt_response(user_input: str) -> str:
    """Get response from ChatGPT for non-SkillCapital queries"""
    try:
        # Clean user input to ensure ASCII compatibility
        cleaned_input = clean_text(user_input)
        
        # Use OpenAI API for ChatGPT responses
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide clear, informative, and well-structured responses. Keep responses concise but comprehensive."},
                {"role": "user", "content": cleaned_input}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Clean the response to prevent encoding issues
        result = response.choices[0].message.content.strip()
        return clean_text(result)
        
    except UnicodeEncodeError as e:
        return "Sorry, I couldn't process your request due to encoding issues. Please try again with simpler text."
    except Exception as e:
        return f"Sorry, I couldn't process your request: {str(e)}"

def is_skillcapital_related(user_input: str) -> bool:
    """Check if the user input is related to SkillCapital"""
    skillcapital_keywords = [
        'skillcapital', 'course', 'courses', 'training', 'learning', 'education',
        'python', 'devops', 'aws', 'amazon', 'azure', 'microsoft', 'cloud',
        'react', 'reactjs', 'react js', 'react.js', 'javascript', 'js', 'html', 'css', 
        'terraform', 'kubernetes', 'sre', 'ui/ux', 'price', 'cost', 'duration', 
        'curriculum', 'modules', 'enroll', 'enrollment', 'certificate'
    ]
    
    user_input_lower = user_input.lower().strip()
    return any(keyword in user_input_lower for keyword in skillcapital_keywords)

def get_crewai_response(user_input: str, agent_type: str = "advisor") -> str:
    """Get response using CrewAI agents"""
    try:
        # Clean the input to prevent encoding issues
        cleaned_input = clean_text(user_input)
        
        # Select appropriate agent based on query type
        if agent_type == "advisor":
            agent = advisor_agent
            task_description = f"Answer this SkillCapital related question: {cleaned_input}"
            expected_output = "Provide a helpful and accurate response about SkillCapital courses, services, or information. Always mention SkillCapital's premium quality and AI-driven platform."
        elif agent_type == "research":
            agent = research_agent
            task_description = f"Research and answer this question: {cleaned_input}"
            expected_output = "Provide a comprehensive and informative response on the topic."
        elif agent_type == "technical":
            agent = technical_agent
            task_description = f"Explain this technical concept: {cleaned_input}"
            expected_output = "Provide a clear technical explanation with practical examples."
        elif agent_type == "enrollment":
            agent = enrollment_agent
            task_description = f"Help with enrollment: {cleaned_input}"
            expected_output = "Provide helpful enrollment guidance and encourage course signup at SkillCapital."
        else:
            agent = advisor_agent
            task_description = f"Answer this question: {cleaned_input}"
            expected_output = "Provide a helpful and informative response."
        
        # Create task
        task = Task(
            description=task_description,
            agent=agent,
            expected_output=expected_output
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        # Clean the result to prevent encoding issues
        if hasattr(result, 'raw'):
            # Handle CrewOutput object
            cleaned_result = clean_text(str(result.raw))
        else:
            # Handle string result
            cleaned_result = clean_text(str(result).strip())
        return cleaned_result
        
    except Exception as e:
        # More detailed error logging
        error_msg = f"Sorry, I couldn't process your request with CrewAI: {str(e)}"
        print(f"DEBUG: CrewAI Error - {str(e)}")  # Debug output
        return error_msg

def get_mock_response(user_input: str) -> str:
    """Get mock response when API is not available"""
    user_input_lower = user_input.lower().strip()
    
    # Mock responses for common questions
    mock_responses = {
        "what is python": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, artificial intelligence, and automation. Python emphasizes code readability with its notable use of significant whitespace.",
        "what is javascript": "JavaScript is a programming language that enables interactive web pages. It's an essential part of web applications and can be used on both the front-end and back-end. JavaScript is known for its versatility and is used in web development, mobile apps, and server-side programming.",
        "what is react": "React is a JavaScript library for building user interfaces, particularly single-page applications. It's used for handling the view layer and can be used for developing both web and mobile applications. React allows developers to create large web applications that can change data without reloading the page.",
        "what is aws": "AWS (Amazon Web Services) is a comprehensive cloud computing platform offered by Amazon. It provides a wide range of services including computing power, storage, databases, networking, and more. AWS is widely used for hosting applications, storing data, and building scalable solutions.",
        "what is azure": "Microsoft Azure is a cloud computing platform and infrastructure created by Microsoft. It provides a wide range of cloud services including computing, analytics, storage, and networking. Azure is used for building, testing, deploying, and managing applications and services.",
        "what is devops": "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops). It aims to shorten the development lifecycle and provide continuous delivery with high software quality. DevOps includes practices like continuous integration, continuous delivery, and infrastructure as code.",
        "what is kubernetes": "Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It helps manage containerized workloads and services, facilitating both declarative configuration and automation.",
        "what is terraform": "Terraform is an infrastructure as code tool that lets you define and provide data center infrastructure using a declarative configuration language. It manages both low-level components like compute instances, storage, and networking, as well as high-level components like DNS entries and SaaS features."
    }
    
    # Check for exact matches first
    for question, answer in mock_responses.items():
        if question in user_input_lower:
            return answer
    
    # Check for partial matches with better logic
    for question, answer in mock_responses.items():
        question_words = question.split()
        input_words = user_input_lower.split()
        
        # Check if key words from the question are in the input
        if any(word in user_input_lower for word in question_words if len(word) > 2):
            return answer
    
    # Check for specific technology mentions
    if "python" in user_input_lower:
        return mock_responses["what is python"]
    elif "javascript" in user_input_lower or "js" in user_input_lower:
        return mock_responses["what is javascript"]
    elif "react" in user_input_lower:
        return mock_responses["what is react"]
    elif "aws" in user_input_lower or "amazon" in user_input_lower:
        return mock_responses["what is aws"]
    elif "azure" in user_input_lower or "microsoft" in user_input_lower:
        return mock_responses["what is azure"]
    elif "devops" in user_input_lower:
        return mock_responses["what is devops"]
    elif "kubernetes" in user_input_lower or "k8s" in user_input_lower:
        return mock_responses["what is kubernetes"]
    elif "terraform" in user_input_lower:
        return mock_responses["what is terraform"]
    
    # Default response
    return "I can help you with information about programming languages, cloud platforms, and development tools. For specific questions about SkillCapital courses, I can provide detailed information about Python, DevOps, AWS, Azure, React, and other technologies we offer."

def get_chat_response(user_input: str) -> str:
    """Get chat response for API calls"""
    try:
        # Clean user input to prevent encoding issues
        user_input = clean_text(user_input)
        user_input_lower = user_input.lower().strip()
        
        # Handle greetings
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return get_greeting_response(user_input)
        
        # Handle price queries
        if any(word in user_input_lower for word in ['price', 'cost', 'how much']):
            return get_price_response(user_input)
        
        # Handle duration queries
        if any(word in user_input_lower for word in ['duration', 'how long', 'time']):
            return get_duration_response(user_input)
        
        # Handle course content queries
        if any(word in user_input_lower for word in ['course', 'content', 'curriculum', 'modules']):
            courses = course_data.get('courses', {})
            
            # Check for specific course mentions
            for course_key in courses:
                if course_key in user_input_lower:
                    return get_course_content(course_key)
            
            # Check for AWS/Azure variations
            if any(word in user_input_lower for word in ['aws', 'amazon', 'cloud']):
                for key, course in courses.items():
                    if 'aws' in key or 'cloud' in key:
                        return get_course_content(key)
                return get_all_courses()
            
            if any(word in user_input_lower for word in ['azure', 'microsoft']):
                for key, course in courses.items():
                    if 'azure' in key:
                        return get_course_content(key)
                return get_all_courses()
            
            # Check for React.js variations
            if any(word in user_input_lower for word in ['react', 'reactjs', 'react.js', 'javascript', 'js']):
                for key, course in courses.items():
                    if 'react' in key or 'javascript' in key:
                        return get_course_content(key)
                
                # Special handling for "react js" course
                if 'react js' in courses:
                    return get_course_content('react js')
                return get_all_courses()
            
            # If no specific course mentioned, return all courses
            return get_all_courses()
        
        # Determine the type of query and use appropriate CrewAI agent
        technical_keywords = ['programming', 'code', 'development', 'software', 'algorithm', 'database', 'api', 'framework', 'python', 'javascript', 'react', 'aws', 'azure']
        research_keywords = ['what is', 'what are', 'how does', 'explain', 'tell me about', 'define', 'describe', 'research']
        enrollment_keywords = ['enroll', 'sign up', 'register', 'join', 'start course', 'how to join', 'enrollment', 'admission']
        
        is_technical = any(keyword in user_input_lower for keyword in technical_keywords)
        is_research = any(keyword in user_input_lower for keyword in research_keywords)
        is_enrollment = any(keyword in user_input_lower for keyword in enrollment_keywords)
        is_skillcapital = is_skillcapital_related(user_input)
        
        # Use CrewAI for different types of queries
        try:
            if is_enrollment:
                # Use enrollment agent for enrollment queries
                response = get_crewai_response(user_input, "enrollment")
                return response
            elif is_skillcapital:
                # Use advisor agent for SkillCapital queries
                response = get_crewai_response(user_input, "advisor")
                return response
            elif is_technical:
                # Use technical agent for programming/technical queries
                response = get_crewai_response(user_input, "technical")
                return response
            elif is_research:
                # Use research agent for general research queries
                response = get_crewai_response(user_input, "research")
                return response
            else:
                # Fallback to ChatGPT for other queries
                try:
                    response = get_chatgpt_response(user_input)
                    return response
                except Exception as e:
                    # Fallback to a simple response if ChatGPT fails
                    return "I can help you with general questions, but I'm best at answering questions about SkillCapital courses. Try asking about Python, DevOps, AWS, Azure, or React.js courses!"
        except Exception as e:
            # Fallback for CrewAI failures - use ChatGPT instead
            try:
                # Try ChatGPT as fallback
                response = get_chatgpt_response(user_input)
                return response
            except Exception as chatgpt_error:
                # Final fallback to mock response
                mock_response = get_mock_response(user_input)
                if mock_response and "I can help you with information" not in mock_response:
                    return mock_response
                else:
                    # Show course information as final fallback
                    return f"I'm having trouble processing that request. Let me provide you with information about our courses instead.\n{get_all_courses()}\nYou can ask about specific courses like Python, DevOps, AWS, Azure, or React.js!"
                
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try asking about SkillCapital courses like Python, DevOps, AWS, or React.js!"

def run_chatbot():
    """Main chatbot function"""
    # Set up file watching if watchdog is available
    observer = None
    if WATCHDOG_AVAILABLE:
        try:
            observer = Observer()
            event_handler = ConfigFileHandler(reload_configuration)
            
            # Watch for changes in config files and course data
            observer.schedule(event_handler, path='.', recursive=False)
            observer.schedule(event_handler, path='src/', recursive=True)
            observer.schedule(event_handler, path='.env/', recursive=False)
            
            observer.start()
            print("🔄 Auto-reload enabled - watching for config changes...")
        except Exception as e:
            print(f"⚠️ Auto-reload setup failed: {e}")
    
    try:
        print(f"SkillCapital: {CHATBOT_NAME}")
        print("SkillCapital: I can help you with course information, pricing, and curriculum details. What would you like to know?")
    except UnicodeEncodeError:
        print("SkillCapital: SkillCapital CrewAI Chatbot")
        print("SkillCapital: I can help you with course information, pricing, and curriculum details. What would you like to know?")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Clean user input to prevent encoding issues
            user_input = clean_text(user_input)
            user_input_lower = user_input.lower().strip()
            
            # Handle exit commands
            if any(word in user_input_lower for word in ['exit', 'quit', 'bye', 'goodbye']):
                safe_print("SkillCapital: Thank You 'Happy Learning'!")
                break
            
            # Handle greetings
            if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
                safe_print(f"SkillCapital: {get_greeting_response(user_input)}")
                continue
            
            # Handle price queries
            if any(word in user_input_lower for word in ['price', 'cost', 'how much']):
                safe_print(f"SkillCapital: {get_price_response(user_input)}")
                continue
            
            # Handle duration queries
            if any(word in user_input_lower for word in ['duration', 'how long', 'time']):
                safe_print(f"SkillCapital: {get_duration_response(user_input)}")
                continue
            
            # Handle course content queries
            if any(word in user_input_lower for word in ['course', 'content', 'curriculum', 'modules']):
                courses = course_data.get('courses', {})
                
                # Check for specific course mentions
                for course_key in courses:
                    if course_key in user_input_lower:
                        safe_print(f"SkillCapital: {get_course_content(course_key)}")
                        break
                else:
                    # Check for AWS/Azure variations
                    if any(word in user_input_lower for word in ['aws', 'amazon', 'cloud']):
                        for key, course in courses.items():
                            if 'aws' in key or 'cloud' in key:
                                safe_print(f"SkillCapital: {get_course_content(key)}")
                                break
                        else:
                            safe_print(f"SkillCapital: {get_all_courses()}")
                        continue
                    
                    if any(word in user_input_lower for word in ['azure', 'microsoft']):
                        for key, course in courses.items():
                            if 'azure' in key:
                                safe_print(f"SkillCapital: {get_course_content(key)}")
                                break
                        else:
                            safe_print(f"SkillCapital: {get_all_courses()}")
                        continue
                    
                    # Check for React.js variations
                    if any(word in user_input_lower for word in ['react', 'reactjs', 'react.js', 'javascript', 'js']):
                        for key, course in courses.items():
                            if 'react' in key or 'javascript' in key:
                                safe_print(f"SkillCapital: {get_course_content(key)}")
                                break
                        else:
                            # Special handling for "react js" course
                            if 'react js' in courses:
                                safe_print(f"SkillCapital: {get_course_content('react js')}")
                            else:
                                safe_print(f"SkillCapital: {get_all_courses()}")
                        continue
                    
                    # If no specific course mentioned, return all courses
                    safe_print(f"SkillCapital: {get_all_courses()}")
                continue
            
            # Determine the type of query and use appropriate CrewAI agent
            technical_keywords = ['programming', 'code', 'development', 'software', 'algorithm', 'database', 'api', 'framework', 'python', 'javascript', 'react', 'aws', 'azure']
            research_keywords = ['what is', 'what are', 'how does', 'explain', 'tell me about', 'define', 'describe', 'research']
            
            is_technical = any(keyword in user_input_lower for keyword in technical_keywords)
            is_research = any(keyword in user_input_lower for keyword in research_keywords)
            is_skillcapital = is_skillcapital_related(user_input)
            
            # Use CrewAI for different types of queries
            try:
                if is_skillcapital:
                    # Use advisor agent for SkillCapital queries
                    response = get_crewai_response(user_input, "advisor")
                    safe_print(f"SkillCapital: {response}")
                elif is_technical:
                    # Use technical agent for programming/technical queries
                    response = get_crewai_response(user_input, "technical")
                    safe_print(f"SkillCapital: {response}")
                elif is_research:
                    # Use research agent for general research queries
                    response = get_crewai_response(user_input, "research")
                    safe_print(f"SkillCapital: {response}")
                else:
                    # Fallback to ChatGPT for other queries
                    try:
                        response = get_chatgpt_response(user_input)
                        safe_print(f"SkillCapital: {response}")
                    except Exception as e:
                        # Fallback to a simple response if ChatGPT fails
                        safe_print("SkillCapital: I can help you with general questions, but I'm best at answering questions about SkillCapital courses. Try asking about Python, DevOps, AWS, Azure, or React.js courses!")
            except Exception as e:
                # Fallback for CrewAI failures - use ChatGPT instead
                print(f"DEBUG: CrewAI Fallback - {str(e)}")
                try:
                    # Try ChatGPT as fallback
                    response = get_chatgpt_response(user_input)
                    safe_print(f"SkillCapital: {response}")
                except Exception as chatgpt_error:
                    # Final fallback to mock response
                    print(f"DEBUG: ChatGPT Fallback - {str(chatgpt_error)}")
                    
                    # Try mock response for general questions
                    mock_response = get_mock_response(user_input)
                    if mock_response and "I can help you with information" not in mock_response:
                        safe_print(f"SkillCapital: {mock_response}")
                    else:
                        # Show course information as final fallback
                        safe_print("SkillCapital: I'm having trouble processing that request. Let me provide you with information about our courses instead.")
                        safe_print(f"SkillCapital: {get_all_courses()}")
                        safe_print("SkillCapital: You can ask about specific courses like Python, DevOps, AWS, Azure, or React.js!")
                
        except KeyboardInterrupt:
            safe_print("\nSkillCapital: Thank You 'Happy Learning'!")
            break
        except Exception as e:
            # More detailed error handling
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"DEBUG: Main Error - Type: {error_type}, Message: {error_msg}")
            safe_print(f"SkillCapital: An error occurred: {error_type} - {error_msg}")
            safe_print("SkillCapital: Please try asking about SkillCapital courses like Python, DevOps, AWS, or React.js!")
    
    # Clean up observer
    if observer:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    try:
        run_chatbot()
    except KeyboardInterrupt:
        safe_print("\nSkillCapital: Thank You 'Happy Learning'!")
    except Exception as e:
        safe_print(f"SkillCapital: An error occurred: {str(e)}")
