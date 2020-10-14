from bs4 import BeautifulSoup
import requests

def crawLineTodayNews(url: str):
  res = requests.get(url)

  if (res.status_code != 200):
    raise Exception("Article not exist")

  web_html = res.text
  soup = BeautifulSoup(web_html, 'html.parser')

  # Get Article Title
  title = soup.title.string

  # Extract Article Content
  article = soup.article
  content = ""

  for tag in article.find_all('a'):
    tag.decompose()
    
  for tag in article.find_all('figure'):
      tag.decompose()

  for tag in article.find_all('p'):
      content += tag.getText()
      content += " "


  return title, content