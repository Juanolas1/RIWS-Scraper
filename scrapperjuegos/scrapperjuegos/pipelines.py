# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch


from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class ScrapperjuegosPipeline:
    def process_item(self, item, spider):
        return item
    

