python3 make_epub.py

ebook-convert book/index.html "Spiewnik Pielgrzyma.epub" \
--level1-toc "//h1" \
--max-toc-links=2000 \
--dont-split-on-page-breaks \
