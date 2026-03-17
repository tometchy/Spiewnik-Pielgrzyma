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
    in_chorus = False

    for line in text.split("\n"):

        if line.startswith("[V"):
            num = re.findall(r"\d+", line)
            num = num[0] if num else ""
            lines.append(f"\n<b>Zwrotka {num}</b>")
            in_chorus = False

        elif line.startswith("[C"):
            lines.append('\n<div class="chorus"><b>Refren</b><br>')
            in_chorus = True

        elif line.startswith("["):

            # zamknij refren jeśli był
            if in_chorus:
                lines.append("</div>")
                in_chorus = False
            continue

        else:
            lines.append(line)

    if in_chorus:
        lines.append("</div>")

    return "<br>".join(lines)


# 📥 Wczytaj pieśni
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

# 📖 Generuj pieśni
for i, (title, lyrics) in enumerate(songs, 1):

    filename = f"song{i}.html"
    anchor = f"song{i}"

    toc += f'<li><a href="{filename}#{anchor}">{title}</a></li>\n'

    if i == 1:
        pagebreak = "auto"
    else:
        pagebreak = "always"

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
    margin: 0;
    padding: 1em;
}}

h1 {{
    font-size: 1.6em;
    margin-top: 0;
    page-break-before: {pagebreak};
}}

.chorus {{
    border-left: 4px solid #888;
    padding-left: 0.6em;
    margin: 0.6em 0;
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


# 📑 Strona główna
with open(f"{BOOKDIR}/index.html", "w", encoding="utf8") as f:

    f.write(f"""
<html>
<head>
<meta charset="utf-8">
<title>Śpiewnik Pielgrzyma</title>

<style>

body {{
    font-family: serif;
    margin: 1em;
}}

li {{
    margin-bottom: 0.3em;
}}

input {{
    font-size: 1em;
    padding: 0.3em;
}}

button {{
    font-size: 1em;
    padding: 0.3em;
}}

</style>

<script>
function goToSong() {{
    var num = document.getElementById("songnum").value;
    if (num) {{
        window.location.href = "song" + num + ".html#song" + num;
    }}
}}
</script>

</head>
<body>

<h1>Śpiewnik Pielgrzyma</h1>

<h2>Idź do numeru pieśni</h2>

<input id="songnum" type="number" placeholder="np. 355">
<button onclick="goToSong()">Idź</button>

<h2>Spis treści</h2>

<ul>
{toc}
</ul>

</body>
</html>
""")
