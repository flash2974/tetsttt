import requests
import zipfile
import io
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

def download_and_unzip(url):
    rep = requests.get(url)
    rep.raise_for_status()
    
    filename = url.split('/')[-1][:-4]
    os.makedirs(filename, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(rep.content)) as z:
        z.extractall(filename)
    
    csv_file = os.path.join(filename, filename + "_d.csv")
    df = pd.read_csv(csv_file)
    shutil.rmtree(filename)
    
    return df

def download_for_id_year(id, year):
    url = f"https://dati-simc.arpae.it/opendata/eraclito91/timeseries/{id:05d}/{id:05d}_{year}.zip"
    try:
        return download_and_unzip(url)
    except Exception as e:
        print(f"Erreur pour {id:05d}_{year}: {e}")
        return None

def main():
    ids = [
        1227, 1228, 1229, 1230,
        1267, 1268, 1269, 1270,
        1307, 1308, 1309, 1310,
        1185, 1186, 1187, 1225,
        1226, 1265, 1266, 1188,
        1189, 1190, 1350, 1347,
        1348, 1349, 1387, 1388,
        1389, 1390, 1147, 1148,
        1305, 1306, 1345, 1346,
        1107, 1108, 1109, 1110,
        1149, 1150, 1304, 1344,
        1384, 1385, 1386, 1424,
        1425, 1224, 1264, 1151
    ]
    
    all_means = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for id in ids:
            futures = [executor.submit(download_for_id_year, id, year) for year in range(1992, 2025)]
            
            dfs = []
            for future in as_completed(futures):
                df = future.result()
                if df is not None:
                    dfs.append(df)
            
            if dfs:
                # Concat toutes les années pour cet ID
                df_concat = pd.concat(dfs, ignore_index=True)
                
                # Moyenne des 3 dernières colonnes
                mean_values = df_concat.iloc[:, -3:].mean()
                
                # Crée un DataFrame ligne unique pour cet ID
                df_mean = pd.DataFrame([mean_values])
                df_mean["Code"] = id
                all_means.append(df_mean)
                
                print(f"Moyenne calculée pour ID {id}")
    
    # Fusionner toutes les lignes ID
    merged_means = pd.concat(all_means, ignore_index=True) # notre super csv avec les données météo des moyennes sur toutes les années
    df_other = pd.read_csv("data.csv") # le csv avec touuutes les données des cases laa
    df_merged_final = pd.merge(merged_means, df_other, on="Code", how="left")
    
    # Sauvegarde
    df_merged_final.to_csv("data/merged_final.csv", index=False)


if __name__ == "__main__":
    main()
