import requests
import feedparser
import time
import asyncio
from datetime import datetime, timedelta
import re
import sys
import time
import json
import threading
import itertools
import sys
from asyncio import Queue
from usage import get_usage
from dropped import get_entries
from keys import API_KEYS
# ex API_KEYS = [{'key': 'XXXXXXX', 'billing_time': 0},...]

# Define the maximum number of concurrent tasks per API key
MAX_CONCURRENT_TASKS_PER_KEY = 3
KEY_MONTHLY_LIMIT = 60*60*10 #10 hrs
QUEUE_MAX_SIZE = 60

# Function to rotate API keys
def get_api_key(duration):
    global API_KEYS
    # Find the API key with the earliest billing time
    min_time_key = min(API_KEYS, key=lambda x: x['billing_time'])

    # If the billing time for the key is within the billing period (10 hours), return it
    if duration + min_time_key['billing_time'] <= 36000:
        return min_time_key['key']
    
    # If all keys have exceeded the billing period, reset billing times and rotate
    print("All API keys have exceeded the 10-hour billing period. Try again next month...")
    for k in API_KEYS:
        print("Key:", k, " Time:", k['billing_time'])
    return None


# Function to poll transcription status
async def poll_transcription_status(transcription_id, headers):
    while True:
        response = requests.get(transcription_id, headers = headers)
        result = response.json()
        if result['status'] == 'done':
            return result
        else:
            await asyncio.sleep(5)  # Poll every 5 seconds

# Function to transcribe audio asynchronously
async def transcribe_audio(entry, key):
            
    audio_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
    podcast_name = entry.title
    duration = time_to_seconds(entry.itunes_duration) if 'itunes_duration' in entry else None
    episode_number = entry.id.split('/')[-1].split('-')[0].zfill(3)
    episode_name = (entry.id.split('-', 1)[1]).split('/')[-1].split('.mp3')[0] if audio_url else "None"
        
    print(f"{episode_number} - Transcribing {podcast_name}...")

    url = "https://api.gladia.io/v2/transcription"

    headers = {
        'accept': 'application/json',
        'x-gladia-key': key,
    }

    payload  = {
        'audio_url': audio_url,
        'diarization': True,
        "summarization": True,
        "summarization_config": {"type": "general"}
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    result = response.json()
    
    if 'statusCode' in result:
        if result['statusCode'] == 402:
            print("API key exceeded usage limit.")
            monthly_time = get_usage(key)
            print("Monthly usage for key", key, ":", monthly_time, "seconds")
            return None
        if result['statusCode'] == 429:
            print("API key exceeded hourly usage limit.")
            return None
    if 'error' in result:
        print(f"Error transcribing {podcast_name}: {result['error']}")
        return None
    
    #transcription_id = result['transcription_id']
    print(result)
    result_url = result['result_url']

    # Poll transcription status asynchronously
    
    print("Loading...")
    transcription = await poll_transcription_status(result_url, headers)
    
    transcription["result"]["metadata"]["rss"] = entry
    json_filename = episode_number + "-" + episode_name
    
    
    with open(f"transcripts\{json_filename}.json", "w") as file:
        json.dump(transcription, file)
    print(f"Transcription for {podcast_name} saved to {json_filename}.json")
    #print(f"Transcription for {podcast_name}: {transcription}")
    return 
def check_keys():
    for key in API_KEYS:
        monthly_time = get_usage(key['key'])
        print("Monthly usage:", key['key'][:5], ":", int(monthly_time), "seconds ", int(100 - monthly_time/(KEY_MONTHLY_LIMIT) * 100), "%")
        key['billing_time'] = monthly_time
    return
def time_to_seconds(time_str):
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_str.split(':'))

    # Convert hours, minutes, and seconds to seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

async def worker(queue, key):
    while True:
        entry = await queue.get()
        await transcribe_audio(entry, key)
        queue.task_done()

async def main():
    
    #determine key availability

    check_keys()
    
    queue = Queue(maxsize=QUEUE_MAX_SIZE)
    entries = get_entries(API_KEYS[0]['key'])
    for entry in entries:
        if queue.full():
            print("Queue is full. Waiting for tasks to complete...")
            break
        else:
            queue.put_nowait(entry)
            print(f"Added {entry['id']} to the queue.")
    '''
    rss_feed_url = "https://pinecast.com/feed/catholicstuff2010-2013"
    feed = feedparser.parse(rss_feed_url)
    start_episode_number = int(sys.argv[1])

    # Add entries to the queue
    for entry in feed.entries:
        audio_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
        podcast_name = entry.title
        duration = time_to_seconds(entry.itunes_duration) if 'itunes_duration' in entry else None
        episode_number = entry.itunes_episode if 'itunes_episode' in entry else None
        if int(episode_number) < start_episode_number:
            continue
        elif queue.full():
            print("Queue is full. Waiting for tasks to complete...")
            break
        else:
            if audio_url:
                queue.put_nowait(entry)
                print(f"Added {episode_number} - {podcast_name} to the queue.")
    '''
    # Create worker tasks for each API key
    tasks = []
    for key in API_KEYS:
        if key['billing_time'] < KEY_MONTHLY_LIMIT:
            for _ in range(MAX_CONCURRENT_TASKS_PER_KEY):
                task = asyncio.create_task(worker(queue, key['key']))
                tasks.append(task)

    # Wait for all tasks to complete
    await queue.join()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    print("Transcription completed.")

if __name__ == "__main__":
    asyncio.run(main())
