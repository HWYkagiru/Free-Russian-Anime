import os
import requests
from bs4 import BeautifulSoup
import webbrowser
from InquirerPy import inquirer
from tabulate import tabulate
from InquirerPy.base import Choice


def getid(selectedanimeurl, animename):
    animeid = ""
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

    return animeid


def makehtml(animename, animeid, image, description):
    htmlanime = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{animename}</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            transition: background-color 0.3s ease;
            background-color: #111;
            color: #fff;
        }}
        body.light-mode {{
            background-color: #fff;
            color: #111;
        }}
        #anime-title {{
            font-size: 40px;
            text-align: center;
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
        }}
        #iframe-container {{
            width: 80%;
            height: 80%;
            max-width: 800px;
            max-height: 600px;
            position: relative;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        #dark-mode-toggle {{
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 10px;
            background-color: #ddd;
            color: #111;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        #dark-mode-toggle.light-mode {{
            background-color: #111;
            color: #fff;
        }}
        #github-link {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            font-size: 12px;
            color: #aaa;
        }}
        #github-link a {{
            color: #aaa;
            text-decoration: none;
        }}
        #text-id {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: #aaa;
        }}
        #anime-image {{
            position: absolute;
            top: 50px; 
            left: 50px; 
            max-width: 400px; 
            max-height: 400px; 
        }}
        #description-box {{
            position: absolute;
            top: calc(50px + 400px + 20px);
            left: 50px;
            width: 260px;
            height: 300px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }}
        #description-text {{
            font-size: 16px;
            color: #fff;
            overflow-wrap: break-word;
        }}
    </style>
</head>
<body class="dark-mode">
    <img id="anime-image" src="{image}" alt="{animename} Poster">
    <h1 id="anime-title">{animename}</h1>
    <button id="dark-mode-toggle" onclick="toggleDarkMode()">Dark Mode</button>
    <div id="iframe-container">
        <iframe src="https://www.anilibria.tv/public/iframe.php?id={animeid}" frameborder="0" allowfullscreen sandbox="allow-same-origin allow-scripts"></iframe>
    </div>
    <div id="github-link">
        <a href="https://github.com/HWYkagiru/" target="_blank">https://github.com/HWYkagiru/</a>
    </div>
    <div id="text-id">
        ID: {animeid}
    </div>
    <div id="description-box">
        <div id="description-text">
            {description}
        </div>
    </div>

    <script>
        function toggleDarkMode() {{
            var body = document.body;
            body.classList.toggle("dark-mode");
            body.classList.toggle("light-mode");
            var darkModeToggle = document.getElementById("dark-mode-toggle");
            darkModeToggle.classList.toggle("light-mode");
        }}
    </script>
</body>
</html>'''
    animefolder = "animes"
    os.makedirs(animefolder, exist_ok=True)
    filename = os.path.join(animefolder, f"{animename}.html")
    with open(filename, "w", encoding="utf-8") as htmlfile:
        htmlfile.write(htmlanime)
    webbrowser.open_new_tab(filename)

def searchanime():
    anime = input("Anime Name: ")
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
        print("Anime List:")
        soup = BeautifulSoup(response.text, 'html.parser')
        animelink = soup.find_all('a', href=True)
        animedict = {}
        index = 1
        anilelist = []
        for link in animelink:
            animename = link['href'].split('/')[-1].replace('.html', '').replace('-', ' ')
            animeurl = "https://www.anilibria.tv" + link['href'].replace("\\", "")
            animedict[index] = (animename, animeurl)
            anilelist.append([index, animename])
            index += 1
        
        table = tabulate(anilelist, headers=["Index", "Anime Name"], tablefmt="fancy_grid")
        print(table)
        
        choices = [Choice(str(key)) for key in animedict.keys()]
        selection = inquirer.select(
            message="Select anime:",
            choices=choices
        ).execute()
        
        if selection:
            selectedanime = animedict[int(selection)]
            print(selectedanime[1])
            return selectedanime
        else:
            print("Invalid selection.")
            return None
    else:
        print("Error searching for anime:", response.status_code)
        return None

def getimageurl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Searching for Image URL")
        soup = BeautifulSoup(response.content, 'html.parser')
        ogimgtag = soup.find('meta', {'property': 'og:image'})
        if ogimgtag and 'content' in ogimgtag.attrs:
            imageurl = ogimgtag['content']
            image = "https://www.anilibria.tv" + imageurl
            print("Found image source")
            print(image)
            return image
        else:
            print("Image URL not found in metadata.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def getdescription(url):
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
            return description
        else:
            print("Description not found.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    selectedanime = searchanime()
    if selectedanime:
        animename, selectedanimeurl = selectedanime
        animeid = getid(selectedanimeurl, animename)
        image = getimageurl(selectedanimeurl)
        description = getdescription(selectedanimeurl)
        if animeid and image and description:
            makehtml(animename, animeid, image, description)
        else:
            print("Error getting Info.")
