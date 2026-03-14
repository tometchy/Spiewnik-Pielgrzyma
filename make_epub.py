import os
import xml.etree.ElementTree as ET

songs = []

for file in sorted(os.listdir(".")):
    if file.endswith(".xml") or file[0].isdigit():
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            title = root.findtext("title", "Bez tytułu")
            lyrics = root.findtext("lyrics", "")

            lyrics = lyrics.replace("[V", "\n\nZwrotka ").replace("]", "\n")

            songs.append((title, lyrics))
        except:
            pass

html = "<html><head><meta charset='utf-8'></head><body>"
html += "<h1>Śpiewnik Pielgrzyma</h1>"

for title, lyrics in songs:
    html += f"<h2>{title}</h2>"
    html += "<p>" + lyrics.replace("\n", "<br>") + "</p>"

html += "</body></html>"

open("spiewnik.html","w",encoding="utf8").write(html)
