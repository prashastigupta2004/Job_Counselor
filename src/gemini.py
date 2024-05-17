import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # load all environment variables

genai.configure(api_key=os.environ["GEMINI_API_KEY3"])

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction=(
    "You are JobMentee.ai  a professional job mentor providing assistance to students. "
    "Help them explore their interests, understand future career prospects, "
    "and offer suggestions for their career paths. Act like an intelligent recommender "
    "by asking relevant questions to guide them effectively. Begin by greeting the student, "
    "asking for their name, wishings further ask for their querry, and then start a conversation about their interests and career-related help. "
    "Also, include questions about their extracurricular activities, volunteer work, internships, "
    "and any special projects they’ve worked on. ask each time in less than 25 word and answer in less than 35 words. "
  ),
)

# Initialize the chat session
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": ["hii"],
    },
    {
      "role": "model",
      "parts": [
        "Hi there! 👋  It's great to connect with you.  What's your name? I'm here to help you explore your interests and think about your future career path.  Let's start by chatting about what you're passionate about.  What are some things you enjoy doing in your free time? \n",
      ],
    },
  ]
)

def get_chat_response(user_message):
    print("funcion called with user")
    print(user_message)
    response = chat_session.send_message(user_message)
    print(response.text)
    return response.text
