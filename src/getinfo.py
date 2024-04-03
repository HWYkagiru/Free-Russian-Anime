import requests
from bs4 import BeautifulSoup

def getid(selectedanimeurl):
    url = selectedanimeurl
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
            print("Found ID:", animeid)
        else:
            print("ID NOT FOUND")
    else:
        print(f"Error: {response.status_code}")

def searchanime():
    anime = input("Anime Name:")
    url = "https://www.anilibria.tv/public/search.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "*/*"
    }
    payload = {
        "search": anime
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print("Animes:")
        soup = BeautifulSoup(response.text, 'html.parser')
        animelink = soup.find_all('a', href=True)
        animedict = {}
        index = 1
        for link in animelink:
            animename = link['href'].split('/')[-1].replace('.html', '').replace('-', ' ')
            animeurl = "https://www.anilibria.tv" + link['href'].replace("\\", "")
            animedict[index] = animeurl
            print(f"{index}. {animename}")
            index += 1
        
        selection = int(input("Select Anime: "))
        if selection in animedict:
            selectedanimeurl = animedict[selection]
            print(selectedanimeurl)
            return selectedanimeurl
        else:
            print("Invalid selection.")
            return None
    else:
        print("Error Searching Animes:", response.status_code)
        return None

if __name__ == "__main__":
    selectedanimeurl = searchanime()
    if selectedanimeurl:
        getid(selectedanimeurl)
