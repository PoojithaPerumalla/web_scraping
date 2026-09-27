import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Product URLs and target prices
products = [
    {
        "name": "Raspberry Pi Electronics Projects",
        "url": "https://books.toscrape.com/catalogue/raspberry-pi-electronics-projects-for-the-evil-genius_630/index.html",
        "target_price": 50.00
    },
    {
        "name": "Algorithms to Live By",
        "url": "https://books.toscrape.com/catalogue/algorithms-to-live-by-the-computer-science-of-human-decisions_880/index.html",
        "target_price": 35.00
    },
    {
        "name": "The Literature Book",
        "url": "https://books.toscrape.com/catalogue/the-literature-book-big-ideas-simply-explained_755/index.html",
        "target_price": 20.00
    }
]


# Create images folder automatically
os.makedirs("images", exist_ok=True)


# Browser-like request header
headers = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_product(product, product_number):

    try:
        url = product["url"]
        target_price = product["target_price"]

        # --------------------------------
        # Fetch webpage
        # --------------------------------
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        # --------------------------------
        # Parse webpage
        # --------------------------------
        soup = BeautifulSoup(
            response.content,
            "html.parser"
        )

        # --------------------------------
        # Extract product title
        # --------------------------------
        title_tag = soup.select_one(
            ".product_main h1"
        )

        title = title_tag.get_text(
            strip=True
        )

        # --------------------------------
        # Extract product price
        # --------------------------------
        price_tag = soup.select_one(
            ".product_main .price_color"
        )

        price_text = price_tag.get_text(
            strip=True
        )

        # Extract numeric value from price
        price_match = re.search(
            r"\d+\.\d+",
            price_text
        )

        price = float(
            price_match.group()
        )

        # --------------------------------
        # Extract product image URL
        # --------------------------------
        image_tag = soup.select_one(
            ".product_page img"
        )

        image_url = urljoin(
            url,
            image_tag.get("src")
        )

        # --------------------------------
        # Compare price
        # --------------------------------
        if price <= target_price:
            comparison = "WITHIN TARGET PRICE"
        else:
            comparison = "HIGHER THAN TARGET PRICE"

        # --------------------------------
        # Download product image
        # --------------------------------
        image_response = requests.get(
            image_url,
            headers=headers,
            timeout=15
        )

        image_response.raise_for_status()

        image_path = (
            f"images/product_{product_number}.jpg"
        )

        with open(
            image_path,
            "wb"
        ) as image_file:

            image_file.write(
                image_response.content
            )

        # --------------------------------
        # Display results
        # --------------------------------
        print("\n" + "=" * 65)
        print(f"PRODUCT {product_number}")
        print("=" * 65)

        print(f"Product     : {product['name']}")
        print(f"Title       : {title}")
        print(f"Price       : £{price:.2f}")
        print(f"Target Price: £{target_price:.2f}")
        print(f"Image URL   : {image_url}")
        print(f"Comparison  : {comparison}")
        print("Image       : Downloaded successfully")
        print(f"Saved At    : {image_path}")

    except requests.RequestException as error:

        print(
            f"\nNetwork error for Product {product_number}"
        )

        print(f"Details: {error}")

    except Exception as error:

        print(
            f"\nError processing Product {product_number}"
        )

        print(f"Details: {error}")


# ==========================================
# MAIN PROGRAM
# ==========================================

print("=" * 65)
print("             WEB SCRAPING ASSIGNMENT")
print("=" * 65)

for number, product in enumerate(
    products,
    start=1
):

    scrape_product(
        product,
        number
    )


print("\n" + "=" * 65)
print("             SCRAPING COMPLETED")
print("=" * 65)