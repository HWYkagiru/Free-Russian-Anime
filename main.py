import os
import requests
from bs4 import BeautifulSoup
import webbrowser
from InquirerPy import inquirer
from tabulate import tabulate
from InquirerPy.base import Choice


def getid(selectedanimeurl, animename, animeid):
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
            makehtml(animename, animeid)
        else:
            print("ID NOT FOUND")
    else:
        print(f"Error: {response.status_code}")

def makehtml(animename, animeid):
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
        }}
        body.dark-mode {{
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
            top: 0px;
            left: 50%;
            transform: translateX(-50%);
        }}
        #iframe-container {{
            width: 80%;
            height: 80%;
            max-width: 800px;
            max-height: 600px;
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
    </style>
</head>
<body class="dark-mode">
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
    with open(filename, "w") as html_file:
        html_file.write(htmlanime)
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

if __name__ == "__main__":
    selectedanime = searchanime()
    if selectedanime:
        animename, selectedanimeurl = selectedanime
        getid(selectedanimeurl, animename, "001")
