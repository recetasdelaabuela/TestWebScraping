# Test WebScraping
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import pandas as pd

def concatenar(directorio):
    print('Concatenando ficheros csv en directorio ' + str(directorio))
    subdirectorio_list = [subdirectorio for subdirectorio in os.listdir(directorio)]
    print('Subdirectorios: ' + str(subdirectorio_list))

    dfs = []
    for subdirectorio in subdirectorio_list:
        print(subdirectorio)
        ruta_subdirectorio = os.path.join(directorio, subdirectorio)
        print('Subdirectorio: ' + str(ruta_subdirectorio))
        archivos_csv = [archivo for archivo in os.listdir(ruta_subdirectorio) if archivo.endswith('.csv')]
        print('Archivos: ' + str(archivos_csv))
        for archivo_csv in archivos_csv:
            ruta_csv = os.path.join(ruta_subdirectorio, archivo_csv)
            print('Concatenando fichero ' + str(ruta_csv))
            df = pd.read_csv(ruta_csv)
            dfs.append(df)
    df_concatenado = pd.concat(dfs, ignore_index=True)
    fichero_csv = os.path.join(directorio, 'recetas.csv')
    df_concatenado.to_csv(fichero_csv, index=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    concatenar('.\Scrapper')

