import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import os

class DiagnosisSpider(scrapy.Spider):
    name = 'diagnosis'
    start_urls = ['https://www.praktiskmedicin.se/sjukdomar/']

    def parse(self, response):
        for diagnosis_link in response.css('a.list-items-ojjqml::attr(href)').getall():
            full_url = urljoin(response.url, diagnosis_link)
            yield scrapy.Request(full_url, callback=self.parse_diagnosis)

    def parse_diagnosis(self, response):
        title = response.css('h1::text').get().strip()
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f'diagnoses/{safe_title}.md'

        os.makedirs('diagnoses', exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            # Write title
            f.write(f'# {title}\n\n')
            f.write(f'URL: {response.url}\n\n')

            # Extract and write content by sections
            for section in response.css('h2, h3, h4, ul, p'):
                if section.css('h2'):
                    section_title = section.css('::text').get().strip()
                    f.write(f'\n## {section_title}\n\n')
                elif section.css('h3'):
                    section_title = section.css('::text').get().strip()
                    f.write(f'\n### {section_title}\n\n')
                elif section.css('h4'):
                    section_title = section.css('::text').get().strip()
                    f.write(f'\n#### {section_title}\n\n')
                elif section.css('ul'):
                    list_items = section.css('li::text').getall()
                    for item in list_items:
                        f.write(f'- {item.strip()}\n')
                    f.write('\n')
                else:
                    # Extract all text from the paragraph, including strong text
                    section_content = ' '.join(section.css('::text').getall()).strip()
                    if section_content:
                        # Check if there's a strong tag
                        strong_text = section.css('strong::text').get()
                        if strong_text:
                            # Write the strong text in bold
                            f.write(f'**{strong_text.strip()}** ')
                            # Write the rest of the content
                            remaining_content = section_content.replace(strong_text, '', 1).strip()
                            f.write(f'{remaining_content}\n\n')
                        else:
                            f.write(f'{section_content}\n\n')

        self.log(f'Saved file {filename}')

# Main execution
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
})

process.crawl(DiagnosisSpider)
process.start()
print("Scraping completed. Results saved in 'diagnoses' directory.")
