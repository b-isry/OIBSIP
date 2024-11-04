import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import subprocess

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CREDENTIALS_FILE = './credentials.json'

MONTHES = ["january" , "february" , "march" , "april", "may", "june", "july", "august", "september", "october", "november", "december"] 
DAYS = ["monday", "tuesday", "wednsday", "thursday", "friday", " saturday", "sunday"]
DAY_EXTNSIONS = ["rd", "th", "st"]

def note(text):
  date = datetime.datetime.now()
  file_name = str(date).replace(":", "-") + "-note.txt"
  with open(file_name, "w") as f:
    f.write(text)
  
  subprocess.Popen(["notepad.exe", file_name])
  
def speak(text):
    tts = gTTS(text = text, lang = 'en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception "+ str(e))
    return said.lower

def authenticate_google():

  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
      token.write(creds.to_json())

  
  service = build("calendar", "v3", credentials=creds)
  
  return service

def get_events(n, service):
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  print(f"Getting the upcoming {n} events")
  events_result = (
      service.events()
          .list(
          calendarId="primary",
          timeMin=now,
          maxResults=n,
          singleEvents=True,
          orderBy="startTime",
        )
      .execute()
    )
  events = events_result.get("items", [])

  if not events:
    speak("No upcoming events found.")
  else:
    speak(f"you have {len(events)} events on this day.")
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      start_time = str(start.split("T")[1].split("-")[0]) 
      if int(start_time.split(":")[0])< 12:
        start_time = start_time + "am"
      else:
        start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
        start_time = start_time + "pm"
        
      speak(event["summary"] + " at " + start_time)
        
def get_date(text):
  text = text.lower()
  today = datetime.date.today()
  
  if text.count("today") > 0:
    return today
  day = -1
  day_of_week = -1
  month = -1
  year = today.year
  
  for word in text.split():
    if word in MONTHES:
      month = MONTHES.index(word) + 1
    elif word in DAYS:
      day_of_week = DAYS.index(word)
    elif word.isdigit():
      day = int(word)
    else:
      for ext in DAY_EXTNSIONS:
        found = word.find(ext)
        if found > 0:
          try:
            day = int(word[:found])
          except:
            pass
          
  if month < today.month and month != -1:
    year = year + 1
  
  if day < today.day and month == -1 and day != -1:
    month = month + 1
  
  if month == -1 and day == -1 and day_of_week !=1:
    current_day_of_week = today.weekday()
    dif = day_of_week - current_day_of_week
    
    if dif < 0:
      dif += 7
      if text.count("next") >= 1:
        dif += 7
    return today + datetime.timedelta(dif)
  
  return datetime.date(month=month, day=day, year=year)
  
WAKE = "hey"
SERVICE = authenticate_google()
print("start")

while True:
  print("listening...")
  text = get_audio()
  
  if text.count(WAKE) > 0:
    speak("hey")
    text = get_audio()
    
    CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
    for phrase in CALENDAR_STRS:
      if phrase in text:
        date = get_date(text)
        if date:
          get_events(date, SERVICE)
        else:
          speak("please try again")
          
    NOTE_STRS = ["make a note", "write this down", "remember this"]
    for phrase in NOTE_STRS:
      if phrase in text:
        speak("what do you want me to write down?")
        note_text = get_audio()
        note(note_text)
        speak("done")
      
      