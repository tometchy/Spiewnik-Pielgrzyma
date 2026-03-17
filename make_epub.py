#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
import re
import shutil

BOOKDIR = "book"

if os.path.exists(BOOKDIR):
    shutil.rmtree(BOOKDIR)

os.makedirs(BOOKDIR)

songs = []


def format_lyrics(text):

    lines = []

    for line in text.split("\n"):

        if line.startswith("[V"):
            num = re.findall(r"\d+", line)
            num = num[0] if num else ""
            lines.append(f"\n<b>Zwrotka {num}</b>")

        elif line.startswith("[C"):
            lines.append("\n<b>Refren</b>")

        elif line.startswith("["):
            continue

        else:
            lines.append(line)

    return "<br>".join(lines)


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


toc = ""

for i, (title, lyrics) in enumerate(songs, 1):

    filename = f"song{i}.html"
    anchor = f"song{i}"

    # 🔥 TOC wskazuje konkretnie na anchor
    toc += f'<li><a href="{filename}#{anchor}">{title}</a></li>\n'

    with open(f"{BOOKDIR}/{filename}", "w", encoding="utf8") as f:

        f.write(f"""
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>

<style>

body {{
    font-family: serif;
    line-height: 1.6;
    font-size: 1.2em;
    margin: 2em;
}}

h1 {{
    font-size: 1.6em;
}}

</style>

</head>
<body>

<a id="{anchor}"></a>
<h1>{title}</h1>

<p>{lyrics}</p>

</body>
</html>
""")


with open(f"{BOOKDIR}/index.html", "w", encoding="utf8") as f:

    f.write(f"""
<html>
<head>
<meta charset="utf-8">
<title>Śpiewnik Pielgrzyma</title>

<style>

body {{
    font-family: serif;
    margin: 2em;
}}

li {{
    margin-bottom: 0.3em;
}}

</style>

</head>
<body>

<h1>Śpiewnik Pielgrzyma</h1>

<h2>Spis treści</h2>

<ul>
{toc}
</ul>

</body>
</html>
""")
