import scrapy


class CountrySpider(scrapy.Spider):
    name = 'country_spider'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_sovereign_states']

    # parsing url
    def parse(self, response):
        # find all countries
        rows = response.xpath('//table[contains(@class,"wikitable")][1]/tbody/tr')
        for row in rows:
            country_name = row.xpath('.//td[1]//a/text()').get()
            membership_un = row.xpath('.//td[contains(.,"UN")]/text()').get()
            sovereignty_dispute_info = row.xpath('.//td[3]/text()').get()
            country_status = row.xpath('.//td[4]//text()').get()
            # link for country page
            link = row.xpath('.//b/a//@href').get()
            # go to the links
            yield response.follow(url=link if link else '/wiki/Zambia', callback=self.parse_country,
                                  meta={'country_name': country_name,
                                        'membership_un': membership_un,
                                        'sovereignty_dispute_info': sovereignty_dispute_info,
                                        'country_status': country_status})

    def parse_country(self, response):
        rows = response.xpath("//table[contains(@class,'infobox ib-country vcard')][1]/tbody")
        for row in rows:
            capital = row.xpath('.//td[contains(@class,"infobox-data")]/a/text()').get()
            demonym = row.xpath('.//a[contains(@title,"Demonym")]/parent::th/following-sibling::td/a/text()').get()

        name = response.request.meta['country_name']
        membership_un = response.request.meta['membership_un']
        sovereignty_dispute_info = response.request.meta['sovereignty_dispute_info']
        country_status = response.request.meta['country_status']
        yield {
            'country': name,
            'capital': capital,
            'membership_un': membership_un.strip(),
            'sovereignty_dispute_info': sovereignty_dispute_info.strip(),
            'country_status': country_status.strip(),
            'demonym': demonym,
        }
