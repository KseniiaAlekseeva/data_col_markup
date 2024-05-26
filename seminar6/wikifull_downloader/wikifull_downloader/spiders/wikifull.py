import scrapy


class WikifullSpider(scrapy.Spider):
    name = "wikifull"
    start_urls = ['https://commons.wikimedia.org/wiki/Category:Featured_pictures_on_Wikimedia_Commons']

    def parse(self, response):
        # Измененный XPath для извлечения ссылок на страницы изображений, а не непосредственно на изображения
        for image_page in response.xpath('//*[@id="mw-category-media"]/ul/li/div/a/@href').extract():
            # Переходим на страницу изображения
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

    def parse_image_page(self, response):
        # Ищем URL полной версии изображения. Допустим, что он находится в элементе с id 'file', а ссылка - в атрибуте 'href'
        full_image_url = response.xpath('//*[contains(@class, "fullImageLink")]/a/@href').extract_first()
        if full_image_url:
            # Скачиваем полную версию изображения
            yield scrapy.Request(response.urljoin(full_image_url), self.save_image)

    def save_image(self, response):
        # Получаем имя файла изображения
        filename = response.url.split('/')[-1]
        # Сохраняем изображение в папку images
        with open(f'images/{filename}', 'wb') as f:
            f.write(response.body)
