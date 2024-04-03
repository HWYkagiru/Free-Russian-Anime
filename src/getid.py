import requests
from bs4 import BeautifulSoup

def getid():
    url = "https://www.anilibria.tv/release/tokyo-ghoul.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Searching Anime Id")
        soup = BeautifulSoup(response.content, 'html.parser')
        findanimeid = soup.find('input', {'id': 'releaseID', 'type': 'hidden'})
        if findanimeid:
            animeid = findanimeid['value']
            print(animeid)
        else:
            print("ID NOT FOUND")
    else:
        print(f"Error: {response.status_code}")
getid()