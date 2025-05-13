import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font
from tqdm import tqdm


def get_rating(class_name):
    """Конвертирует CSS-класс рейтинга в число звёзд"""
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return rating_map.get(class_name.split()[-1], 0)


def clean_price(price_text):
    """Очищает цену от лишних символов и конвертирует в float"""
    # Удаляем все НЕ-цифры и точки, кроме последней (для десятичных)
    cleaned = ''.join(c for c in price_text if c.isdigit() or c == '.')
    # Оставляем только первую точку (если есть)
    if '.' in cleaned:
        parts = cleaned.split('.')
        cleaned = parts[0] + '.' + ''.join(parts[1:])
    return float(cleaned) if cleaned else 0.0


# Создаем Excel-файл
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Books"
headers = ["Название", "Цена (£)", "Наличие", "Рейтинг (звёзды)"]
ws.append(headers)

# Делаем заголовки жирными
for cell in ws[1]:
    cell.font = Font(bold=True)

base_url = "https://books.toscrape.com/"
current_page = 1
processed_books = 0

with tqdm(desc="Парсинг страниц") as pbar:
    while True:
        try:
            url = f"{base_url}catalogue/page-{current_page}.html"
            response = requests.get(url, timeout=10)

            # Если страница не существует, прерываем цикл
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')

            if not books:
                break

            for book in books:
                try:
                    title = book.h3.a['title']
                    price_text = book.find('p', class_='price_color').get_text(strip=True)
                    price = clean_price(price_text)
                    availability = book.find('p', class_='instock').get_text(strip=True)
                    rating_classes = book.find('p', class_='star-rating')['class']
                    rating = get_rating(rating_classes[1] if len(rating_classes) > 1 else 'Zero')

                    ws.append([title, price, availability, rating])
                    processed_books += 1
                except Exception as e:
                    print(f"Ошибка при обработке книги: {e}")
                    continue

            current_page += 1
            pbar.update(1)

        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы {current_page}: {e}")
            break

# Автоматически подгоняем ширину столбцов
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column].width = adjusted_width

# Сохраняем Excel-файл
wb.save("products.xlsx")
print(f"\nУспешно обработано {processed_books} книг с {current_page - 1} страниц. Данные сохранены в products.xlsx")