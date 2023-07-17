from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

# Helper functions
def create_message(sender, recipient, subject, message):
    """Create a message for sending via Gmail API."""
    message = {
        'raw': base64.urlsafe_b64encode(
            f'From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n{message}'.encode('utf-8')
        ).decode('utf-8')
    }
    return message

def send_message(service, user_id, message):
    """Send a message via Gmail API."""
    service.users().messages().send(userId=user_id, body=message).execute()

