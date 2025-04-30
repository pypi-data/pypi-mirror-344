import json
import base64
import os
import schedule
import time
import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("EmailMcpServer")

# Gmail and Calendar API setup
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.events'
]
CREDS_FILE = os.path.join(Path.home(), ".gmail-mcp", "gcp-oauth.keys.json")

# Debug: Check if credentials file exists
if not os.path.exists(CREDS_FILE):
    print(f"Error: {CREDS_FILE} not found. Please place gcp-oauth.keys.json in ~/.gmail-mcp/")
else:
    print(f"Found {CREDS_FILE}")

def get_gmail_service():
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(os.path.join(Path.home(), ".gmail-mcp", "token.json"), SCOPES)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(CREDS_FILE), exist_ok=True)
        with open(os.path.join(Path.home(), ".gmail-mcp", "token.json"), 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(os.path.join(Path.home(), ".gmail-mcp", "token.json"), SCOPES)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(CREDS_FILE), exist_ok=True)
        with open(os.path.join(Path.home(), ".gmail-mcp", "token.json"), 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

@mcp.tool()
def summarize_emails(max_results: int = 5, sender: str = "", label: str = "") -> str:
    """Summarize the latest emails from the inbox, optionally filtering by sender or label."""
    try:
        service = get_gmail_service()
        query = f"from:{sender}" if sender else ""
        if label:
            query += f" label:{label}"
        results = service.users().messages().list(userId='me', maxResults=max_results, q=query.strip()).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return "No emails found matching the criteria."
        
        summaries = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            
            body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            else:
                body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            
            summary = body[:200] + "..." if len(body) > 200 else body
            summaries.append(f"Subject: {subject}\nSummary: {summary}")
        
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error summarizing emails: {str(e)}"

@mcp.tool()
def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> str:
    """Send an email to the specified recipient."""
    try:
        service = get_gmail_service()
        raw_message = base64.urlsafe_b64encode(
            f"From: me\nTo: {to}\nCc: {cc}\nBcc: {bcc}\nSubject: {subject}\n\n{body}".encode()
        ).decode()
        service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return f"Email sent to {to} with subject '{subject}'"
    except Exception as e:
        return f"Error sending email: {str(e)}"

@mcp.tool()
def add_calendar_event(email_id: str = "", subject: str = "", description: str = "", start_time: str = "", duration_minutes: int = 60) -> str:
    """Create a Google Calendar event for an email or manually specified details."""
    try:
        calendar_service = get_calendar_service()
        
        if email_id:
            gmail_service = get_gmail_service()
            msg = gmail_service.users().messages().get(userId='me', id=email_id, format='full').execute()
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            
            body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            else:
                body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            description = body[:1000]
            
            start_time = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat()
        
        if not subject:
            subject = "Event from Email"
        if not description:
            description = "No description provided."
        
        if not start_time:
            start_time = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat()
        
        end_time = (datetime.datetime.fromisoformat(start_time) + datetime.timedelta(minutes=duration_minutes)).isoformat()
        event = {
            'summary': subject,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }
        event = calendar_service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"
    except Exception as e:
        return f"Error creating calendar event: {str(e)}"

def check_important_emails():
    """Check for new important emails and create calendar events."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=5, q="label:important -calendar_event_created").execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No new important emails found.")
            return
        
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            
            result = add_calendar_event(email_id=message['id'])
            print(f"Processed email: {subject}, Result: {result}")
            
            service.users().messages().modify(userId='me', id=message['id'], body={'addLabelIds': ['calendar_event_created']}).execute()
    except Exception as e:
        print(f"Error checking important emails: {str(e)}")

# Schedule automatic checking every 10 minutes
schedule.every(10).minutes.do(check_important_emails)

def main():
    """Main function to run the MCP server and scheduler."""
    import threading
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    mcp.run()

if __name__ == "__main__":
    main()