import requests
from bs4 import BeautifulSoup

def getimageurl():
    url = "https://www.anilibria.tv/release/tokyo-ghoul.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Searching for Image URL")
        soup = BeautifulSoup(response.content, 'html.parser')
        og_image_tag = soup.find('meta', {'property': 'og:image'})
        if og_image_tag and 'content' in og_image_tag.attrs:
            imageurl = og_image_tag['content']
            image = "https://www.anilibria.tv" + imageurl
            print("Found image source")
            print(image)
        else:
            print("Image URL not found in metadata.")
    else:
        print(f"Error: {response.status_code}")

getimageurl()
