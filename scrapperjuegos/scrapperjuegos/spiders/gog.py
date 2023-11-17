import scrapy
from scrapperjuegos.items import juegosItem
from datetime import datetime
import locale
import re
class GogSpider(scrapy.Spider):
    name = "gog"
    allowed_domains = ["www.gog.com"]
    start_urls = ["https://www.gog.com/en/games"]

    def parse(self, response):
        # Extraer y seguir enlaces a juegos
        game_links = response.css('a.product-tile--grid::attr(href)').getall()
        for link in game_links:
            yield response.follow(link, self.parse_game)

        # Seguir a la siguiente página de resultados si existe
        current_page = response.css('input.pagination-input__item::attr(value)').get()
        if current_page:
            current_page_number = int(current_page)
            next_page_number = current_page_number + 1
            next_page_url = f"https://www.gog.com/en/games?page={next_page_number}"
            yield response.follow(next_page_url, self.parse)

    def parse_game(self, response):
        item = juegosItem()
        item["url"] = response.request.url
        item["name"] = response.css('h1.productcard-basics__title::text').get().strip()
        price_text = response.css('span.product-actions-price__final-amount::text').get()
        if price_text:
            try:
                # Convertir el precio a flotante
                item["price"] = float(price_text)
            except ValueError:
                # Manejo de errores si la conversión falla
                item["price"] = None
        else:
            item["price"] = None
        item["developer_company"] = response.css('div.details__content a[href*="/games?developers="]::text').get()
        item["publisher_company"] = response.css('div.details__content a[href*="/games?publishers="]::text').get()
        date_release_string = response.css('div.details__content span::text').re_first(r'(\d{4}-\d{2}-\d{2})')
        if date_release_string:
            try:
                # Convertir la fecha a formato YYYY-MM-DD
                date_release = datetime.strptime(date_release_string, '%Y-%m-%d').date()
                item["date_release"] = date_release.isoformat()
            except ValueError:
                # Manejo de errores si la conversión de la fecha falla
                item["date_release"] = None
            
        # Intentar extraer la URL de la imagen
        image_url_set = response.css('.productcard-player__logo::attr(srcset)').get()

        # Inicializar image_url como None por defecto
        image_url = None

        # Procesar solo si image_url_set contiene algo
        if image_url_set:
            # Dividir las URLs y seleccionar la primera (de menor resolución)
            image_url = image_url_set.split(',')[0].split()[0]  # Toma la primera URL del srcset

        item["image"] = image_url


        genre_selector = '//div[div[@class="details__category table__row-label"]' \
                        '[contains(text(), "Genre:")]]/div[@class="details__content table__row-content"]//a/text()'
        item["genre_type"] = response.xpath(genre_selector).getall()

        
        score_element = response.css('.productcard-rating__score::text').extract_first()
        
        if score_element:
            score_number = float(score_element.strip().split('/')[0])
            
            # Multiplicamos por 2 y redondeamos ya que en la web viene puesto sobre 5 con decimales y manipulamos enteros en la web
            rounded_score = int(round(score_number * 2))
            
            item['score'] = rounded_score
        else:
            item['score'] = int(0)


        pegi_text = response.xpath("//div[contains(text(), 'PEGI Rating')]/text()").get()
        if pegi_text:
            pegi_rating_match = re.search(r'PEGI Rating:\s*(\d+)', pegi_text)
            if pegi_rating_match:
                pegi_rating = pegi_rating_match.group(1)
                item["pegi"] = f"PEGI {pegi_rating}"
            else:
                item["pegi"] = "Desconocido"
        else:
            item["pegi"] = "Desconocido"
        
        item["web"] = "gog"

        yield item
