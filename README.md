# assessor-scraper

The goal of this project is to transform the data from the Orleans Parish
Assessor's Office [website](http://nolaassessor.com/) into formats that
are better suited for data analysis.

## development environment setup

### prerequisites

You must have Python 3 installed.  You can download it
[here](https://www.python.org/downloads/).

### first setup a python [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments)

```
python3 -m venv .venv
. .venv/bin/activate
```

### install the dependencies with [pip](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
```
pip install -r requirements.txt
```


## Getting started

If you want to explore how to extract data using scrapy, use the [scrapy
shell](https://doc.scrapy.org/en/latest/intro/tutorial.html#extracting-data) to interactively
work with the response.

For example,
```
scrapy shell http://qpublic9.qpublic.net/la_orleans_display.php?KEY=2336-OCTAVIAST
owner = response.xpath('//td[@class="owner_value"]/text()')[0]
owner.extract()
next_page = response.xpath('//td[@class="header_link"]/a/@href').extract_first()
```

### Get all the parcel ids

Getting a list of parcel ids allows us to build urls for every property
so we can scrape the data for that parcel.  These parcel ids are used
in the url like `http://qpublic9.qpublic.net/la_orleans_display.php?KEY=701-POYDRASST`,
where `701-POYDRASST` is the parcel id.

Running the `parcel_id_extractor.py` script will cleverly use the owner search to
extract all available parcel ids, then save them in a file `parcel_ids.txt`.

The file is checked in to the repo, but if you want to run it yourself
to update it with the latest, run 

```
python parcel_id_extractor.py
```


### Running the spider
Running the spider from the command line will crawl the assessors website and
[output the data](https://doc.scrapy.org/en/latest/topics/feed-exports.html) to a destination of your choice.

By default, the spider will output data to a postgres database, which is configured
in `scraper/settings.py`. You can use a hosted postgres instance or run one locally using
[Docker](https://store.docker.com/search?type=edition&offering=community):

> Important Note: Scraping should always be done responsibly so check the [robots.txt](http://www.robotstxt.org/robotstxt.html) file to ensure the site doesn't explicitly instruct crawlers to not crawl.  Also when running the scraper, be careful not to cause unexpected load to the assessors website - consider running during non-peak hours or profiling the latency to ensure you aren't overwhelming the servers.


To run the spider,
```
scrapy runspider scraper/spiders/assessment_spider.py
```
> Warning: this will take a long time to run...you can kill the process with ctrl+c.

To run the spider and output to a csv
```
scrapy runspider scraper/spiders/assessment_spider.py -o output.csv
```

#### Running on Heroku
Set required environment variables:
```
heroku config:set DATABASE_URL=postgres://user:pass@host:5432/assessordb
heroku config:set MAPZEN_API_KEY=mapzen-abc123
```

You can run the scraper on Heroku by scaling up the worker dyno:
```
heroku ps:scale worker=1
```

See [the Heroku docs](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) for more info on how to deploy Python code.
