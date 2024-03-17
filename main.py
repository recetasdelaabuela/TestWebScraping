# Test WebScraping
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Importamos los módulos necesarios
import scrappi
import downloads
import concatenate

def scrapping(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Starting, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # Llamamos a las funciones o clases definidas en cada uno de los archivos
    scrappi.scrappi_main()
    downloads.downloads_main()
    concatenate.concatenar('.\Scrapper')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrapping('Web Scraping Recetas Gratis.net')

