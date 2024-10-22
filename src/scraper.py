import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import os

class DiagnosisSpider(scrapy.Spider):
    name = 'diagnosis'
    start_urls = ['https://www.praktiskmedicin.se/sjukdomar/']

    def __init__(self, *args, **kwargs):
        super(DiagnosisSpider, self).__init__(*args, **kwargs)
        # Create the diagnoses directory at the start
        os.makedirs('diagnoses', exist_ok=True)

    def parse(self, response):
        # Extract all h2 headers from the main page
        h2_headers = response.css('h2::text').getall()
        
        # Save h2 headers to a file
        with open('diagnoses/main_categories.txt', 'w', encoding='utf-8') as f:
            for header in h2_headers:
                f.write(f"{header.strip()}\n")

        # Continue with scraping individual disease pages
        for diagnosis_link in response.css('a[href*="/sjukdomar/"]::attr(href)').getall():
            full_url = urljoin(response.url, diagnosis_link)
            yield scrapy.Request(full_url, callback=self.parse_diagnosis)

    def parse_diagnosis(self, response):
        title = response.css('h1::text').get().strip()
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f'diagnoses/{safe_title}.md'

        with open(filename, 'w', encoding='utf-8') as f:
            # Write title
            f.write(f'# {title}\n\n')
            f.write(f'URL: {response.url}\n\n')

            # Extract and write ICD code
            icd_code = response.css('button::text').get()
            if icd_code:
                f.write(f'{icd_code.strip()}\n\n')

            # Extract and write first button text (category)
            first_button = response.css('button.btn-primary::text').get()
            if first_button:
                f.write(f'Kategori: {first_button.strip()}\n\n')

            # Extract and write content by sections
            for section in response.xpath('//h2 | //h4'):
                section_title = section.xpath('normalize-space()').get()
                if section.root.tag == 'h2':
                    f.write(f'## {section_title}\n\n')
                elif section.root.tag == 'h4':
                    f.write(f'#### {section_title}\n\n')

                # Initialize content list
                content = []
                # Iterate over the following siblings
                for sibling in section.xpath('following-sibling::*'):
                    # If sibling is h2 or h4, break
                    if sibling.root.tag in ['h2', 'h4']:
                        break
                    # If sibling is p, add its text
                    if sibling.root.tag == 'p':
                        paragraph_content = sibling.xpath('normalize-space()').get()
                        if paragraph_content:
                            content.append(paragraph_content)
                    # Handle lists
                    elif sibling.root.tag in ['ul', 'ol']:
                        # Extract list items
                        items = sibling.xpath('.//li')
                        for item in items:
                            item_text = item.xpath('normalize-space()').get()
                            if item_text:
                                content.append(f'- {item_text}')
                    # Handle other elements if needed
                    # Add more conditions here if you need to handle other tags

                # Write the content to file
                if content:
                    f.write('\n'.join(content))
                    f.write('\n\n')

        self.log(f'Saved file {filename}')


    def process_list(self, list_element):
        list_type = 'ul' if list_element.root.tag == 'ul' else 'ol'
        list_items = list_element.css('li')
        formatted_list = ''
        for item in list_items:
            item_text = ' '.join(item.css('::text').getall()).strip()
            if list_type == 'ul':
                formatted_list += f'- {item_text}\n'
            else:
                formatted_list += f'1. {item_text}\n'
        return formatted_list + '\n'

# Main execution
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    process.crawl(DiagnosisSpider)
    process.start()
    print("Scraping completed. Results saved in 'diagnoses' directory.")
