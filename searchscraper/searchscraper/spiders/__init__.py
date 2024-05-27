import scrapy

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['yahoo.com']  # Replace with the actual domain you are scraping

    def start_requests(self):
        query = 'Python programming tutorials'
        search_url = f"https://www.yahoo.com/search?q={query}"  # Replace with the actual search URL
        yield scrapy.Request(url=search_url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # Update CSS selectors to match the search result structure of the target website
        for result in response.css('div.result'):
            title = result.css('h3::text').get()
            link = result.css('a::attr(href)').get()
            if title and link:
                yield {
                    'title': title,
                    'link': link,
                }

        # Handle pagination if applicable
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_search_results)