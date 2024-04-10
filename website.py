import requests
from bs4 import BeautifulSoup
import json

LIMIT=209999
COUNT=0

def extract_info(base_url,url):
    response = requests.get(base_url+url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting various info from the webpage
    title = soup.find('h1').text.strip()

    print(title)

    metadata = soup.find('p').text.strip().split(' • ')
    episode_number = metadata[0].split(' • ')[0].replace('#', '')
    date_published = metadata[1]
    authors = metadata[2]

    cover_image = soup.find('img', class_='cover-image')['src']

    iframe_src = soup.find('iframe')['src']

    description = soup.find('div', class_='player-center').find_next_sibling('div').text.strip()

    tags = [tag.text.strip() for tag in soup.find_all('a', href=lambda href: href and '/tags.html#' in href)]

    # Extracting link to the previous page if available
    prev_page_link = soup.find('a', class_='prev')
    prev_page_url = prev_page_link['href'] if prev_page_link else None
    
    next_page_link = soup.find('a', class_='next')
    next_page_url = next_page_link['href'] if next_page_link else None

    data = {
        'title': title,
        'episode_number': episode_number,
        'date_published': date_published,
        'authors': authors,
        'cover_image': cover_image,
        'iframe_src': iframe_src,
        'description': description,
        'tags': tags,
        'url': url,
        'next_page_url': next_page_url,
        'previous_page_url': prev_page_url
    }

    return data

def main():
    # Start URL
    base_url = "https://catholicstuffpodcast.com"
    start_url = '/podcast/2010/01/06/stylites.html'
    
    # Extract data recursively
    podcasts=[]

    data = extract_info(base_url,start_url)
    while data.get('next_page_url') and len(podcasts)<LIMIT:
        podcasts.append(data)
        data = extract_info(base_url,data['next_page_url'])

    # Save data to JSON file
    with open('scraped_data.json', 'w') as f:
        json.dump(podcasts, f, indent=4)
    
    print("Data saved to scraped_data.json")

if __name__ == "__main__":
    main()
