#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET

songs = []

for file in sorted(os.listdir(".")):
    if os.path.isfile(file):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            title = root.findtext("title", "Bez tytułu")
            lyrics = root.findtext("lyrics", "")

            lyrics = lyrics.replace("[V", "\n\nZwrotka ").replace("]", "\n")

            songs.append((title, lyrics))
        except:
            pass

html = """
<html>
<head>
<meta charset='utf-8'>
<title>Śpiewnik Pielgrzyma</title>
</head>
<body>
<h1>Śpiewnik Pielgrzyma</h1>

<h2>Spis treści</h2>
<ul>
"""

for i,(title,lyrics) in enumerate(songs,1):
    html += f'<li><a href="#song{i}">{i}. {title}</a></li>\n'

html += "</ul>\n"

for i,(title,lyrics) in enumerate(songs,1):
    html += f'<h2 id="song{i}">{i}. {title}</h2>'
    html += "<p>" + lyrics.replace("\n","<br>") + "</p>\n"

html += "</body></html>"

with open("spiewnik.html","w",encoding="utf8") as f:
    f.write(html)
