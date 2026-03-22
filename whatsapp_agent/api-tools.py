import os
import requests
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google_auth import get_google_credentials

# --- 1. Weather API (OpenWeatherMap) ---

def get_weather_forecast(location: str) -> str:
    """Fetches the current weather for a given location."""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found in environment variables."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"The current weather in {location} is {temp}°C with {desc}."
    return f"Could not fetch weather for {location}. Check the location name."

# --- 2. Gmail API ---

def send_gmail(to_email: str, subject: str, body: str) -> str:
    """Sends an email using the user's Gmail account."""
    creds = get_google_credentials()
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_email
        message['Subject'] = subject
        
        # The Gmail API requires a base64url encoded string
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return f"Email successfully sent to {to_email}."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# --- 3. Google Calendar API (Schedule/Reminders) ---

def create_calendar_event(title: str, start_time: str, end_time: str) -> str:
    """
    Creates a calendar event. 
    start_time and end_time must be ISO formatted strings (e.g., '2026-03-12T10:00:00+02:00').
    """
    creds = get_google_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        event = {
          'summary': title,
          'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Jerusalem', 
          },
          'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Jerusalem',
          },
        }
        
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event '{title}' created successfully! Link: {event_result.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"