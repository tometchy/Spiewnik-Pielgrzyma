python3 make_epub.py

ebook-convert book/index.html "Spiewnik Pielgrzyma.epub" \
--chapter "//h2" \
--level1-toc "//h2" \
--max-toc-links=2000
