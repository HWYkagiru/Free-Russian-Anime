import requests
from bs4 import BeautifulSoup

def getdescription():
    url = "https://www.anilibria.tv/release/tokyo-ghoul.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Searching for Description")
        soup = BeautifulSoup(response.content, 'html.parser')

        finddescr = soup.find('textarea', {'id': 'nDescription'})
        if finddescr:
            description = finddescr.text.strip()
            print("Found description")
            print(description)
        else:
            print("Description not found.")
    else:
        print(f"Error: {response.status_code}")

getdescription()
