import requests
from bs4 import BeautifulSoup
import time

"""
PaperFinder类用于从指定的基准URL和年份范围内抓取论文信息，并将其保存到本地文件中。

Attributes:
    base_url (str): 基准URL。
    start_year (int): 开始年份。
    end_year (int): 结束年份。
    headers (dict): HTTP请求头，用于模拟浏览器请求。
"""
class PaperFinder:

    """
    初始化PaperFinder类的实例。

    Args:
        base_url (str): 基准URL。
        start_year (int): 开始年份。
        end_year (int): 结束年份。
    """
    def __init__(self, base_url, start_year, end_year):
        self.base_url = base_url
        self.start_year = start_year
        self.end_year = end_year
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    """
    获取指定URL的BeautifulSoup对象。

    Args:
        url (str): 目标URL。

    Returns:
        BeautifulSoup: 解析后的HTML内容。
    """
    def get_soup(self, url):
        response = requests.get(url, headers=self.headers).content
        return response

    """
    将论文信息保存到本地文件。

    Args:
        title (str): 论文标题。
        abstract (str): 论文摘要。
        link (str): 论文链接。
    """
    def save_paper_info(self, title, abstract, link):
        with open('papers.txt', 'a', encoding='utf-8') as f:
            f.write(f'Title: {title}\n')
            f.write(f'Abstract: {abstract}\n')
            f.write(f'Link: {link}\n')
            f.write('\n')

    """
    开始抓取指定年份范围内的论文信息。
    """
    def crawl(self):
        for year in range(self.start_year, self.end_year + 1):
            year_url = f'{self.base_url}/{year}'
            soup = self.get_soup(year_url)
            papers = soup.find_all('div', class_='paper-item')  # Adjust the class name based on the actual HTML structure

            for paper in papers:
                title = paper.find('h2', class_='title').text.strip()
                abstract = paper.find('div', class_='abstract').text.strip()
                link = paper.find('a', class_='link')['href']
                self.save_paper_info(title, abstract, link)
                time.sleep(1)  # Be polite and don't overload the server

if __name__ == '__main__':
    # 调试部分
    test_url = 'https://crad.ict.ac.cn/cn/article/2024/12'
    crawler = PaperFinder(base_url='', start_year=0, end_year=0)

    soup = crawler.get_soup(test_url)
    soup.find('div', class_='articleListBox active')

    output_file = 'output.html' 
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(f"网页内容已保存到 {output_file}")

    '''
    base_url = 'http://example.com/journal'  # Replace with the actual journal URL
    start_year = 2021
    end_year = 2022
    crawler = PaperFinder(base_url, start_year, end_year)
    crawler.crawl()
    '''