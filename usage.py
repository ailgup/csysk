import requests
import json
import datetime

# Function to get the usage of the API key
def get_usage(key):
    monthly_time = 0
    url = "https://api.gladia.io/v2/transcription"

    headers = {"x-gladia-key": key}

    # Get the current date
    current_date = datetime.date.today()
    first_day_of_month = current_date.replace(day=1)

    # Convert the first day of the current month to ISO date string
    iso_date_string = first_day_of_month.isoformat()

    # Update the querystring with the ISO date string
    querystring = {"before_date": iso_date_string, "limit":"777"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_reply = response.json()
    
    for i in json_reply["items"]:
        if ("result" in i):
            time = i["result"]["metadata"]["billing_time"]
            monthly_time += time
    
    #print(monthly_time, " seconds")
    #print(monthly_time/(10*60*60) * 100, " %")
    return monthly_time #seconds used