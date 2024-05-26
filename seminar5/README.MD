```commandline
cd seminar5
conda install scrapy
scrapy startproject country_scrapy
cd country_scrapy
scrapy genspider country_spider en.wikipedia.org/wiki/List_of_sovereign_states
scrapy crawl country_spider
scrapy crawl country_spider -o countries.json
scrapy crawl country_spider -o countries.csv -t csv
```