# Scrapy settings for scrapperjuegos project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapperjuegos"

SPIDER_MODULES = ["scrapperjuegos.spiders"]
NEWSPIDER_MODULE = "scrapperjuegos.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "scrapperjuegos (+http://www.yourdomain.com)"

from user_agent import generate_user_agent

USER_AGENT = generate_user_agent()


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scrapperjuegos.middlewares.ScrapperjuegosSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "scrapperjuegos.middlewares.ScrapperjuegosDownloaderMiddleware": 543,
#}
LOG_LEVEL = 'DEBUG'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #"scrapperjuegos.pipelines.ScrapperjuegosPipeline": 300,
    'scrapperjuegos.pipelines.ScrapperjuegosPipeline': 300,
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500

    #"scrapperjuegos.pipelines.ElasticsearchPipeline": 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

ELASTICSEARCH_SERVERS = ["https://localhost:9200"]  # Cambia la URL por la de tu servidor Elasticsearch en Docker

ELASTICSEARCH_USE_SSL = True
ELASTICSEARCH_VERIFY_CERTS = False  # Agrega esta línea


ELASTICSEARCH_INDEX = "scrapperjuegos-riws-index"  # El nombre del índice donde quieres almacenar tus datos
ELASTICSEARCH_UNIQ_KEY = "url"  # La clave única para cada ítem (si aplica)

#ELASTICSEARCH_CERTIFICATE = "C:\\Users\\MSI\\Desktop\\RIWS\\scrapperjuegos\\http_ca.crt"

ELASTICSEARCH_USERNAME = "elastic"  # Reemplaza con tu nombre de usuario de Elasticsearch
ELASTICSEARCH_PASSWORD = "VjcT4+K6O9FWc8lJO=hp"  # Reemplaza con tu contraseña de Elasticsearch


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
