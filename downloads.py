from pathlib import Path
import pandas as pd
import numpy as np
from newspaper import Article
from newspaper import Config
from bs4 import BeautifulSoup
import os

def gets_properties(soup):
    """Gets the properties of the recipe and returns a dictionary with the info"""
    properties = soup.find('div', class_='properties')
    if properties:
        comensales = properties.find('span', class_='comensales')
        duracion = properties.find('span', class_='duracion')
        para = properties.find('span', class_='para')
        dificultad = properties.find('span', class_='dificultad')
        # Obtener el texto de cada objeto si no es None
        comensales_text = comensales.text.strip() if comensales is not None else None
        duracion_text = duracion.text.strip() if duracion is not None else None
        dificultad_text = dificultad.text.strip() if dificultad is not None else None
        para_text = para.text.strip() if para is not None else None

        # Return info
        info = {
            "comensales": comensales_text,
            "duración": duracion_text,
            "para": para_text,
            "dificultad": dificultad_text
        }
        print(info)

        return info
    return {}

def gets_inline(soup):
    """Gets the inline info and returns a dictionary with the info"""
    # Get the inline info
    inline = soup.find('div', class_='inline')
    if inline is None:
        return {}
    coste = inline.find('span', class_='coste')
    types = inline.find_all("a")
    if types:
        types = [type.text.strip() for type in types]
    
    coste = coste.text if coste else None
    info = {
        "coste": coste,
        "types": types
    }
    return info

def gets_ingredients(soup):
    """Gets the ingredients and returns a dictionary with the info"""
    ingredientes = soup.find('div', class_='ingredientes')
    ingredientes = ingredientes.find_all('label')
    ingredientes = [ingrediente.text.strip() for ingrediente in ingredientes]
    info = {
        "ingredientes": ingredientes
    }
    return info

def gets_recipe_info(soup):
    """Gets the recipe info and returns a dictionary with the info"""
    # Get the recipe info
    recipe_info = soup.find('div', class_='recipe-info')
    if not recipe_info:
        return {}
    properties = gets_properties(recipe_info)
    inline = gets_inline(recipe_info)
    ingredientes = gets_ingredients(recipe_info)
    info = {**properties, **inline, **ingredientes}
    return info

def gets_introduction(soup):
    intro = soup.find('div', class_='intro')
    if intro:
        intro = intro.text.strip()
    return intro

def gets_steps(soup):
    steps = soup.find_all('div', class_='apartado')
    order = []
    for step in steps:
        if step.find('div', class_='orden'):
            text = step.text.strip()
            order.append(text)
    return order
def votes(soup):
    votes = soup.find('span', class_='votos')
    votes = votes.text.strip() if votes else None
    return votes



def gets_info(url):
    info = {}
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 30

    article = Article(url, config=config)
    try:
        article.download()
        article.parse()
    except AttributeError as e:
        print(f"\t\t\tError " + str(e) + " with {url}")
    
    # Get the info
    soup = BeautifulSoup(article.html, 'html.parser')
    print(article.title)
    info["title"] = article.title
    info["intro"] = gets_introduction(soup)
    info["order"] = gets_steps(soup)
    info["votes"] = votes(soup)
    
    recipe_info = gets_recipe_info(soup)
    #Merger the dictionaries
    info = {**info, **recipe_info}
    return info


def inter_batch(links,file_save):
    """Gets the info from a batch of links"""
    infos = []
    erros = []
    for link in links:
        print(f"\t\t{link}")
        try:
            info = gets_info(link)
            print(info)
            info["url"]= link
            info["title"] = info["title"].replace('\n',' ').replace('\t',' ').replace('\f',' ')
            info["intro"] = info["intro"].replace('\n',' ').replace('\t',' ').replace('\f',' ')
            info["order"] = [order.replace('\n', ' ').replace('\t', ' ').replace('\f', ' ') for order in info["order"]]
            infos.append(info)
        except AttributeError as e:
            print(f"\t\t\tError "+str(e)+" with {link}")
            erros.append(link)
    pd.DataFrame(infos).to_csv(file_save, index=False, encoding='utf-8')

    if len(erros) > 0:
        with file_save.with_name("errors.txt").open(mode='a') as f:
            f.write('\n'.join(erros))

def downloads_main():
    dataset_dir = Path("Datasets").glob("*/")
    print(dataset_dir)
    save_info = Path("Scrapper")
    copy = Path("Completed")
    for directory in dataset_dir:
        tag = directory.name
        links_txt = directory.glob(pattern="*.txt")
        print('links_txt:'+str(links_txt))
        save_dir = save_info/tag
        copy_dir = copy/tag
        if (os.path.exists(save_dir) and os.path.isdir(save_dir)):
            print('Esquivando directorio ' + str(save_dir))
        else:
            save_dir.mkdir(parents=True, exist_ok=True)
            copy_dir.mkdir(parents=True, exist_ok=True)
            print(f"Saving info from {tag} in {save_dir}")
            for idx,link in enumerate(links_txt):
                links_batch = np.loadtxt(fname=link, dtype=str).tolist()
                print('links_batch:' + str(links_batch))
                save_file = save_dir/link.name.replace(".txt", ".csv")
                inter_batch(links_batch, save_file)
                print(f"\t{link} done!")
                if os.path.exists(copy_dir/link.name):
                    print(copy_dir/link.name)
                else:
                    link.rename(copy_dir/link.name)
                #break
    print('End of script')

if __name__ == "__main__":
    downloads_main()