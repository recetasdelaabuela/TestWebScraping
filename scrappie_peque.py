from newspaper import Article
from bs4 import BeautifulSoup
from pathlib import Path
ULR = "https://www.pequerecetas.com/receta/page/{}/"

def gets_links(soup):
    """Gets the links of the recipes and returns a list with the links"""
    links = soup.find_all('div', class_="post-isabel")
    links = [link.find('a') for link in links]
    links = [link.get('href') for link in links]
    return links

if __name__ == "__main__":
    path = Path('.')
    #len_txt = len(list(path.glob('*.txt')))
    contador=1
    #for page in range(len_txt+1, 151):
    for page in range(1, 162):
        url = ULR.format(page)
        article = Article(url)
        article.download()
        article.parse()
        soup = BeautifulSoup(article.html, 'html.parser')
        links = gets_links(soup)
        #doc_txt = path/f'{page}.txt'
        doc_txt = path / 'Pequerecetas.txt'
        doc_txt.write_text(doc_txt.read_text() + '\n'.join(links))
        contador = contador + 1
        print()
        print(f'{page}/150 :  for {url}')
        
        