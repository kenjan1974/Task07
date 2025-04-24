import requests
from bs4 import BeautifulSoup
# 載入套件與字典檔
import jieba
import string
import re
jieba.load_userdict("dict.txt.big")

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
    paragraphs = news_soup.find('div', class_='article-content__paragraph')
    section = paragraphs.find('section', class_='article-content__editor')
    # print(f'新聞連結: {link}')
    if section:
        # 移除所有 <figure> 標籤及其內容
        for fig in section.find_all('figure'):
            fig.decompose()
        # 移除指定 style 的 <div> 及其內容
        for div in section.find_all('div', style=lambda s: s and s.startswith('position: relative;margin:50px 0 0;')):
            div.decompose()
        article_paragraphs = []
        for p in section.find_all('p'):
            content = p.get_text(strip=True).replace('\n', ' ')
            article_paragraphs.append(content)
        article_content = ' '.join(article_paragraphs)
        news.append(article_content)

# 列印所有新聞內容
# for article in news:
#     print(article)
#     print('=' * 40)

tokens = []
for article in news:
    # 使用 jieba 斷詞
    # 這裡使用 HMM=False 來關閉隱馬可夫模型，避免斷詞不準確
    token = list(jieba.cut(article, HMM=False))
    # 排除標點符號
    token = [w for w in token if re.match(r'^[\w\u4e00-\u9fff]+$', w)]    
    tokens.extend(token)

# 計算每個詞的出現次數
# 使用字典來儲存詞頻
word_count = {}
for word in tokens:
    if len(word) > 1:
        word_count[word] = word_count.get(word, 0) + 1

# 排序並列印，從出現次數最多到最少
word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
for word, count in word_count.items():
    print(f"{word}: {count}")