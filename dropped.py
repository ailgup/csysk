import requests
import feedparser
import os
import json

FEED = "https://pinecast.com/feed/catholicstuff2010-2013"

def get_transcription(transcription_id, key):
    url = f"https://api.gladia.io/v2/transcription/{transcription_id}"
    headers = {"x-gladia-key": key}
    response = requests.get(url, headers=headers)
    return response.json()

def get_todo():
    feed = feedparser.parse(FEED)
    todo = []
    total_done = 0
    total = 0
    for entry in feed.entries:
        audio_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
        episode_number = entry.id.split('/')[-1].split('-')[0].zfill(3)
        episode_name = (entry.id.split('-', 1)[1]).split('/')[-1].split('.mp3')[0] if audio_url else "None"
        time_str = entry.itunes_duration
        hours, minutes, seconds = map(int, time_str.split(':'))
        # Convert hours, minutes, and seconds to seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        total += total_seconds
        json_filename = f"{episode_number}-{episode_name}"
        if not os.path.exists(f"transcripts/{json_filename}.json"):
            todo.append(entry)
            print(episode_number)
        else:
            total_done += total_seconds
    print(f"Total {total//3600}:{(total%3600)//60}:{total%60}")
    print(f"Done {total_done//3600}:{(total_done%3600)//60}:{total_done%60}")
    todo = total-total_done
    print(f"TODO {todo//3600}:{(todo%3600)//60}:{todo%60}")
    print(f"Total time: {total_done/(total) * 100}% ")
    return todo
def main(key):
    url = "https://api.gladia.io/v2/transcription"
    headers = {"x-gladia-key": key}
    querystring = {"limit": "777"}
    response = requests.get(url, headers=headers, params=querystring)
    json_reply = response.json()
    
    feed = feedparser.parse(FEED)

    # Add entries to the queue
    for i in json_reply["items"]:
        for entry in feed.entries:
            audio_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
            episode_number = entry.id.split('/')[-1].split('-')[0].zfill(3)
            episode_name = (entry.id.split('-', 1)[1]).split('/')[-1].split('.mp3')[0] if audio_url else "None"
            json_filename = f"{episode_number}-{episode_name}"
            
            if i["status"] == "done" and "audio_url" in i["request_params"] and i["request_params"]["audio_url"] == audio_url:
                if not os.path.exists(f"transcripts/{json_filename}.json"):
                    transcription = get_transcription(i["id"], key)
                    transcription["result"]["metadata"]["rss"] = entry
                    with open(f"transcripts/{json_filename}.json", "w") as file:
                        json.dump(transcription, file)
                        print(f"Transcription saved to {json_filename}.json")
                break
    
    print("Done")
def get_entries(key):
    todo=[]
    url = "https://api.gladia.io/v2/transcription"
    headers = {"x-gladia-key": key}
    querystring = {"limit": "777"}
    response = requests.get(url, headers=headers, params=querystring)
    json_reply = response.json()
    
    feed = feedparser.parse(FEED)
    entries = []
    for entry in feed.entries:
        audio_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
        episode_number = entry.id.split('/')[-1].split('-')[0].zfill(3)
        episode_name = (entry.id.split('-', 1)[1]).split('/')[-1].split('.mp3')[0] if audio_url else "None"
        json_filename = f"{episode_number}-{episode_name}"
        
        #no file yet, check cloud
        if not os.path.exists(f"transcripts/{json_filename}.json"):
            found = False
            for i in json_reply["items"]:
                #if in cloud, save to file
                if i["status"] == "done" and "audio_url" in i["request_params"] and i["request_params"]["audio_url"] == audio_url:
                    transcription = get_transcription(i["id"], key)
                    transcription["result"]["metadata"]["rss"] = entry
                    with open(f"transcripts/{json_filename}.json", "w") as file:
                        json.dump(transcription, file)
                        print(f"Transcription saved to {json_filename}.json")
                        found = True
                        break
            #if not found in cloud, add to todo
            if not found:
                #print(f"Transcription not found for {json_filename}.json")
                todo.append(entry)
           
    print(len(todo))
    return todo
if __name__ == "__main__":
    get_todo()
    main("25e814bc-0df6-43fe-90af-2e53c2e5de02")
