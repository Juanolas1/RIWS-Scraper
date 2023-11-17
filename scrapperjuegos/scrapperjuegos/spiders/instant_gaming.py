import scrapy
from scrapperjuegos.items import juegosItem
from datetime import datetime
import locale

class InstantGamingSpider(scrapy.Spider):
    name = "instant-gaming"
    allowed_domains = ["www.instant-gaming.com"]
    start_urls = ["https://www.instant-gaming.com/es/busquedas/?query="]

    def parse(self, response):
        # Extraer y seguir enlaces a juegos
        game_links = response.css('a.cover.video::attr(href)').getall()
        for link in game_links:
            yield response.follow(link, self.parse_game)

        # Seguir a la siguiente página de resultados si existe
        next_page = response.css('a.arrow.right::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_game(self, response):
        item = juegosItem()
        item["url"] = response.request.url
        item["name"] = response.css('h1.game-title::text').get().strip()
        price_text = response.css('meta[itemprop="price"]::attr(content)').get()
        if price_text:
            try:
                # Convertir el precio a flotante
                item["price"] = float(price_text)
            except ValueError:
                # Manejo de errores si la conversión falla
                item["price"] = None
        else:
            item["price"] = None
        #item["platforms"] = response.css('div.platform + span::text').getall()
        item["developer_company"] = response.css('a[itemprop="applicationSubCategory"][href*="/desarrolladores/"]::text').get()
        item["publisher_company"] = response.css('a[itemprop="applicationSubCategory"][href*="/distribuidor/"]::text').get()
        release_date = response.css('div.release-date::text').get()
        #item["date_release"] = release_date.strip() if release_date else ''
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_texto = release_date.strip() if release_date else ''
        try:
            fecha_objeto = datetime.strptime(fecha_texto, "%d %B %Y")
            fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
            item["date_release"] = fecha_formateada
        except ValueError:
            item["date_release"] = None
            
        item["image"] = response.css('picture.banner img::attr(data-src)').get()
        item["genre_type"] = response.css('div.genres a::text').getall()
        
        # Extracción y conversión del score
        score_text = response.css('div.ig-search-reviews-avg::text').get()
        try:
            # Convertir el score a entero
            item["score"] = int(score_text.strip()) if score_text else None
        except ValueError:
            # Manejo de errores si la conversión falla
            item["score"] = None

        pegi_text = response.xpath("//div[contains(text(), 'Puntuación:')]/following-sibling::div/text()").get()
        if pegi_text is not None:
            item["pegi"] = pegi_text.strip()
        else:
            item["pegi"] = "Desconocido"  
        
        item["web"] = "instant-gaming"

        yield item
