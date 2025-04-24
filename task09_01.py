import requests
from bs4 import BeautifulSoup

# 取得主頁面
response = requests.get('https://udn.com/news/breaknews/1')
soup = BeautifulSoup(response.text, 'html.parser')

# 找出所有新聞連結
news_links = []
for h3 in soup.find_all('h3', class_='rounded-thumb__title'):
    a_tag = h3.find('a', href=True)
    if a_tag:
        news_links.append('https://udn.com' + a_tag['href'])

# 逐一請求每則新聞內容
news = []
for link in news_links:
    news_resp = requests.get(link)
    news_soup = BeautifulSoup(news_resp.text, 'html.parser')
    # 取得所有新聞段落內容
    paragraphs = news_soup.find_all('div', class_='article-content__paragraph')
    print(f'新聞連結: {link}')
    for news_content in paragraphs:
        news.append(news_content.get_text(strip=True).replace('\n', ' '))
        print(news_content.get_text(strip=True))
    print('-' * 40)