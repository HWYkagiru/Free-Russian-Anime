import requests
from bs4 import BeautifulSoup

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
        else:
            print("Invalid selection.")
    else:
        print("Error Searching Animes:", response.status_code)

if __name__ == "__main__":
    searchanime()
