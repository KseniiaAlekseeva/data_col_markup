import scrapy


class PopulationSpiderSpider(scrapy.Spider):
    name = "population_spider"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # find all countries
        rows = response.xpath('//table[@id="example2"]/tbody/tr')
        print(len(rows))
        for row in rows:
            country = row.xpath('.//td[2]/a/text()').get()
            population = row.xpath('.//td[3]/text()').get()
            med_age = row.xpath('.//td[10]/text()').get()
            # link for country page
            link = row.xpath('.//td[2]/a/@href').get()
            # go to the links
            yield response.follow(url=link if link else '/world-population/holy-see-population',
                                  callback=self.parse_country,
                                  meta={'country': country,
                                        'population': population,
                                        'med_age': med_age})

    def parse_country(self, response):
        rows = response.xpath("//table[contains(@class,'table table-hover table-condensed table-list')]/tbody")
        main_city_by_pop = rows[0].xpath('.//tr[1]/td[2]/text()').get()

        country = response.request.meta['country']
        population = response.request.meta['population']
        med_age = response.request.meta['med_age']
        yield {
            'country': country,
            'population': population,
            'med_age': med_age,
            'main_city_by_pop': main_city_by_pop,
        }
