import json
import os

import pandas

import scrapy


class UnsplashSpiderSpider(scrapy.Spider):
    name = "unsplash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        # Измененный XPath для извлечения ссылок на страницы изображений, а не непосредственно на изображения
        for image_page in response.xpath('//*[@class="aD8H3"]/a/@href').extract():
            # Переходим на страницу изображения
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

    def parse_image_page(self, response):
        name = response.xpath("//h1[contains(@class,'z5s87')]/text()")
        category = response.xpath("//div[contains(@class,'TeuLI')]/a/text()")

        # Ищем URL полной версии изображения. Допустим, что он находится в элементе с id 'file', а ссылка - в атрибуте 'href'
        full_image_url = response.xpath('//*[@class="WxXog"]/img/@src').extract_first()
        data = {'name': name,
                'category': category,
                'url': full_image_url,
                'localpath': f'{os.path.dirname(os.path.abspath(__file__))}/images/{full_image_url}.jpg'
                }
        df = pandas.DataFrame(data)

        meta_file = 'meta.csv'
        if not os.path.exists(meta_file):
            df.to_csv(meta_file, mode='a', index=False)
        else:
            df.to_csv(meta_file, mode='a', index=False, header=False)

        if full_image_url:
            # Скачиваем полную версию изображения
            yield scrapy.Request(response.urljoin(full_image_url), self.save_image)

    def save_image(self, response):
        # Получаем имя файла изображения
        filename = response.url.split('/')[-1]
        # Сохраняем изображение в папку images
        with open(f'images/{filename}.jpg', 'wb') as f:
            f.write(response.body)

    def parse_meta(self, response):
        category = response.xpath("//div[contains(@class,'TeuLI')]/a/text()")
        yield {
            'category': category, }
