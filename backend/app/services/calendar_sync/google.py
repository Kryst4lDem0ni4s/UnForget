from typing import List, Dict, Optional
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarService:
    """Service for syncing with Google Calendar."""
    
    def __init__(self, credentials_dict: Dict):
        """
        Initialize Google Calendar service.
        
        Args:
            credentials_dict: OAuth credentials as dictionary
        """
        self.credentials = Credentials(**credentials_dict)
        self.service = build('calendar', 'v3', credentials=self.credentials)
    
    async def list_events(
        self,
        calendar_id: str = 'primary',
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 250
    ) -> List[Dict]:
        """
        Fetch events from Google Calendar.
        
        Args:
            calendar_id: Calendar ID (default 'primary')
            time_min: Start time for event query
            time_max: End time for event query
            max_results: Maximum events to return
            
        Returns:
            List of calendar events
        """
        try:
            if time_min is None:
                time_min = datetime.utcnow()
            
            if time_max is None:
                time_max = time_min + timedelta(days=7)
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Transform to our format
            transformed_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                transformed_events.append({
                    'title': event.get('summary', 'Untitled'),
                    'start_time': start,
                    'end_time': end,
                    'is_fixed': True,  # Google events are considered fixed
                    'source': 'google',
                    'external_id': event.get('id')
                })
            
            return transformed_events
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    async def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        calendar_id: str = 'primary'
    ) -> Optional[Dict]:
        """
        Create an event in Google Calendar.
        
        Args:
            title: Event title
            start_time: Event start time
            end_time: Event end time
            description: Event description
            calendar_id: Calendar ID

            
        Returns:
            Created event data or None if failed
        """
        try:
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            created_event = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            return {
                'external_id': created_event.get('id'),
                'link': created_event.get('htmlLink')
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    async def update_event(
        self,
        event_id: str,
        title: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        calendar_id: str = 'primary'
    ) -> bool:
        """
        Update an existing event.
        
        Args:
            event_id: Google Calendar event ID
            title: New title (optional)
            start_time: New start time (optional)
            end_time: New end time (optional)
            calendar_id: Calendar ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First get the event
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields
            if title:
                event['summary'] = title
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                }
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                }
            
            # Update the event
            self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            return True
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return False
