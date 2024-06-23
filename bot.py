from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from composio_crewai import ComposioToolSet, Action, App


import discord
from discord.ext import commands
import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from crewai import Agent, Task
from composio_crewai import ComposioToolSet, Action, App


# Discord Bot Setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

#Tools
composio_toolset = ComposioToolSet()
tools = composio_toolset.get_tools(apps=[App.GITHUB])



llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key="AIzaSyAo4qFsiKLRyRXE-tjYR6oHTTmCJ1dLgv4"
)


# Google Calendar Setup
PORT_NUMBER = 8080

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load or create credentials
creds = None
if os.path.exists('token.pkl'):
    with open('token.pkl', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Set the redirect_uri with fixed port number
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES,
            redirect_uri=f'http://localhost:{PORT_NUMBER}/oauth2callback')
        creds = flow.run_local_server(port=PORT_NUMBER)

    # Save the credentials for the next run
    with open('token.pkl', 'wb') as token:
        pickle.dump(creds, token)

# Now you can use creds to build the service
service = build('calendar', 'v3', credentials=creds)




# Define a function to interact with Google Calendar using tools
async def perform_action(action, **kwargs):
    task = Task(action=Action(name=action, params=kwargs))
    result = Agent().execute(task)
    return result

# List Events Command
@bot.command(name='events')
async def get_events(ctx):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = await perform_action('list_events', calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime')
    events = events_result.get('items', [])

    if not events:
        await ctx.send('No upcoming events found.')
        return

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append(f"{start} - {event['summary']}")

    await ctx.send("\n".join(event_list))

# Create Event Command
@bot.command(name='create_event')
async def create_event(ctx, summary: str, start_time: str, end_time: str):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }

    event_result = await perform_action('create_event', calendarId='primary', body=event)
    await ctx.send(f"Event created: {event_result.get('htmlLink')}")

# Delete Event Command
@bot.command(name='delete_event')
async def delete_event(ctx, event_id: str):
    try:
        await perform_action('delete_event', calendarId='primary', eventId=event_id)
        await ctx.send("Event deleted.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Update Event Command
@bot.command(name='update_event')
async def update_event(ctx, event_id: str, summary: str = None, start_time: str = None, end_time: str = None):
    try:
        event = await perform_action('get_event', calendarId='primary', eventId=event_id)
        
        if summary:
            event['summary'] = summary
        if start_time:
            event['start'] = {'dateTime': start_time, 'timeZone': 'UTC'}
        if end_time:
            event['end'] = {'dateTime': end_time, 'timeZone': 'UTC'}
        
        updated_event = await perform_action('update_event', calendarId='primary', eventId=event_id, body=event)
        await ctx.send(f"Event updated: {updated_event.get('htmlLink')}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Get Event Details Command
@bot.command(name='event_details')
async def event_details(ctx, event_id: str):
    try:
        event = await perform_action('get_event', calendarId='primary', eventId=event_id)
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        await ctx.send(f"Event: {event['summary']}\nStart: {start}\nEnd: {end}\nLink: {event.get('htmlLink')}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# List Calendars Command
@bot.command(name='list_calendars')
async def list_calendars(ctx):
    try:
        calendars_result = await perform_action('list_calendars')
        calendars = calendars_result.get('items', [])

        if not calendars:
            await ctx.send('No calendars found.')
            return

        calendar_list = []
        for calendar in calendars:
            calendar_list.append(f"{calendar['summary']} (ID: {calendar['id']})")

        await ctx.send("\n".join(calendar_list))
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



# Run the bot
bot.run('MTI1NDQ1MzYwNDY4MTc4MTI4MA.GAm3FE.Z-CfqrcReaDIQ2pPkqzHRVJ5m8dBIT9W4SMosQ')

