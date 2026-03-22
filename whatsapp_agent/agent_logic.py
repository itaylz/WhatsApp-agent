import google.generativeai as genai
import os

# Initialize your API keys
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- Define Your Tools ---

def get_weather_forecast(location: str) -> str:
    """Fetches the current weather for a given location."""
    # TODO: Implement OpenWeatherMap API call here
    return f"The weather in {location} is 22°C and sunny."

def send_gmail(to_email: str, subject: str, body: str) -> str:
    """Sends an email using the user's Gmail account."""
    # TODO: Implement Google Gmail API call here
    return f"Email sent to {to_email}."

def create_calendar_event(title: str, start_time: str, end_time: str) -> str:
    """Creates a calendar event or reminder."""
    # TODO: Implement Google Calendar API call here
    return f"Event '{title}' scheduled for {start_time}."

# --- Setup the Agent ---

# Map the functions so the model can use them
tools = [get_weather_forecast, send_gmail, create_calendar_event]

# Initialize the model with the tools
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash', 
    tools=tools
)

chat = model.start_chat(enable_automatic_function_calling=True)

def process_message(user_input: str) -> str:
    """Sends the user input to the AI and returns the response."""
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Sorry, I ran into an error: {str(e)}"