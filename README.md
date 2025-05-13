# 📚 Books to Scrape Parser

This project scrapes book data from the test website [books.toscrape.com](https://books.toscrape.com) and saves the results into an Excel spreadsheet.

## Features

- Extracts title, price, availability, and rating of books
- Automatically navigates through all pages
- Outputs a formatted `.xlsx` file
- Includes progress indication with `tqdm`

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `openpyxl`
- `tqdm`

## Usage

```bash
pip install -r requirements.txt
python BookstoScrape\ parcer.py
```

The result will be saved as `products.xlsx`.
