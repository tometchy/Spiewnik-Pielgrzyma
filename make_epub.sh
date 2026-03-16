python3 make_epub.py

ebook-convert book/index.html spiewnik-pielgrzyma.epub \
--chapter "//h1" \
--level1-toc "//h1" \
--max-toc-links=2000 \
--dont-split-on-page-breaks \
--toc-filter "Śpiewnik"
