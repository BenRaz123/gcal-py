import datetime
from datetime import UTC, datetime as dt_t
from zoneinfo import ZoneInfo
import os.path
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def epoch_to_dt(epoch: float, tz_db_str: str) -> dt_t:
    dt_utc = dt_t.fromtimestamp(epoch, UTC)
    return dt_utc.astimezone(ZoneInfo(tz_db_str))

def main():
    parser = argparse.ArgumentParser(prog="gcal", description="add calendar event")
    parser.add_argument("-t", "--token-file", default="token.json")
    parser.add_argument("-c", "--credentials-file", default="credentials.json")
    parser.add_argument("-S", "--summary", required=True)
    parser.add_argument("-d", "--description", required=False, default="Automatically generated calendar event from gcal-py")
    parser.add_argument("-s", "--start-time", help="epoch time", required=True)
    parser.add_argument("-e", "--end-time", help="epoch time")
    parser.add_argument("-z", "--time-zone", help="in tzinfo db format", default="Etc/UTC")

    args = parser.parse_args()

    creds = None

    if os.path.exists(args.token_file):
        creds = Credentials.from_authorized_user_file(args.token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    args.credentials_file, SCOPES
                    )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(args.token_file, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        
        start_time = epoch_to_dt(float(args.start_time), args.time_zone).isoformat()

        ev = {
            'summary': args.summary,
            'description': args.description,
            'start': {
                'dateTime': start_time,
                'timeZone': args.time_zone,
            },
            'end': {
                'dateTime': epoch_to_dt(float(args.end_time), args.time_zone).isoformat() if args.end_time else start_time,
                'timeZone': args.time_zone,
            },
        }
        
        print("Event created: " + service.events().insert(calendarId="primary", body=ev).execute().get("htmlLink"))
        

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
