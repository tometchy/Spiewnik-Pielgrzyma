#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
import re

songs = []


def format_lyrics(text):

    lines = []
    in_chorus = False

    for line in text.split("\n"):

        if line.startswith("[") and in_chorus:
            lines.append("</div>")
            in_chorus = False

        if line.startswith("[V"):
            num = re.findall(r"\d+", line)
            num = num[0] if num else ""
            lines.append(f"\n<b>Zwrotka {num}</b>")

        elif line.startswith("[C"):
            lines.append('<div class="chorus"><b>Refren</b><br>')
            in_chorus = True

        elif line.startswith("["):
            continue

        else:
            lines.append(line)

    if in_chorus:
        lines.append("</div>")

    return "<br>".join(lines)


# 📥 wczytaj pieśni
for file in sorted(os.listdir(".")):

    if os.path.isfile(file):

        try:
            tree = ET.parse(file)
            root = tree.getroot()

            title = root.findtext("title", "Bez tytułu").strip()
            lyrics = root.findtext("lyrics", "")

            lyrics = format_lyrics(lyrics)

            songs.append((title, lyrics))

        except:
            pass


html = """
<html>
<head>
<meta charset="utf-8">
<title>Śpiewnik Pielgrzyma</title>

<style>

body {
    font-family: serif;
    line-height: 1.6;
    font-size: 1.2em;
    margin: 0;
    padding: 1em;
}

h1 {
    font-size: 1.6em;
    margin-top: 0;
}

.song {
    margin-bottom: 2em;
}

.chorus {
    border-left: 4px solid #888;
    padding-left: 0.6em;
    margin: 0.6em 0;
}

</style>

</head>
<body>

<h1>Śpiewnik Pielgrzyma</h1>

<h2>Spis treści</h2>
<ul>
"""

# 📑 TOC
for i, (title, _) in enumerate(songs, 1):
    html += f'<li><a href="#song{i}">{title}</a></li>\n'

html += "</ul>\n"

# 📖 pieśni
for i, (title, lyrics) in enumerate(songs, 1):

    html += f'''
<div class="song">
<a id="song{i}"></a>
<h2>{title}</h2>
<p>{lyrics}</p>
</div>
'''

html += "</body></html>"

with open("spiewnik.html", "w", encoding="utf8") as f:
    f.write(html)
