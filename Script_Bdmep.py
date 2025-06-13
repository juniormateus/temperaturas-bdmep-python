import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Caminho para os CSVs
pasta_csv = r'C:\Users\mateus.souza\Downloads\Dados_Bdbmep\Dados_estacoes'

# Cria uma lista com os CSVs na pasta
arquivos = [f for f in os.listdir(pasta_csv) if f.endswith('.csv')]

registros = []

for arquivo in arquivos:
    path_csv = os.path.join(pasta_csv, arquivo)
    
    # Ler metadados (10 primeiras linhas, estrutura do arquivo do bdmep)
    with open(path_csv, 'r', encoding='utf-8-sig') as f:
        meta = [f.readline().strip() for _ in range(10)]
    
    # Extrair metadados em um dicionario
    meta_dict = {}
    for linha in meta:
        if linha:
            chave, valor = linha.split(':', 1)
            meta_dict[chave.strip()] = valor.strip()
    
    nome = meta_dict.get('Nome')
    latitude = float(meta_dict.get('Latitude'))
    longitude = float(meta_dict.get('Longitude'))
    
    # 2. Ler dados (pulando metadados)
    df = pd.read_csv(path_csv, delimiter=';', encoding='utf-8-sig', skiprows=10)
    
    # Limpar colunas removendo espaços e possíveis colunas vazias extras
    df.columns = [col.strip() for col in df.columns]
    
    # 3. Converter coluna Data Medicao para o tipo datetime
    df['Data Medicao'] = pd.to_datetime(df['Data Medicao'], errors='coerce')
    
    # 4. Filtrar meses: outubro (10), novembro (11), dezembro (12)
    df_out_nov_dez = df[df['Data Medicao'].dt.month.isin([10, 11, 12])]
    
    # 5. Limpar possíveis ; extras no final dos valores (ex: '29.3;')
    for col in df.columns[1:]:  # ignorar coluna Data Medicao
        df_out_nov_dez[col] = df_out_nov_dez[col].astype(str).str.replace(';', '')
        df_out_nov_dez[col] = pd.to_numeric(df_out_nov_dez[col], errors='coerce')
    
    # 6. Calcular médias mensais das temperaturas máximas e mínimas para os três meses
    medias = {}
    for mes in [10, 11, 12]:
        df_mes = df_out_nov_dez[df_out_nov_dez['Data Medicao'].dt.month == mes]
        if not df_mes.empty:
            # As colunas específicas que interessam 'TEMPERATURA MAXIMA MEDIA, MENSAL(°C)'
            temp_max_col = [c for c in df.columns if 'TEMPERATURA MAXIMA' in c][0]
            temp_min_col = [c for c in df.columns if 'TEMPERATURA MINIMA' in c][0]
            
            media_max = df_mes[temp_max_col].mean()
            media_min = df_mes[temp_min_col].mean()
        else:
            media_max = None
            media_min = None
        
        medias[f'media_max_{mes}'] = media_max
        medias[f'media_min_{mes}'] = media_min
    
    # 7. Armazenar o registro
    registros.append({
        'Nome': nome,
        'Latitude': latitude,
        'Longitude': longitude,
        **medias
    })

# 8. Criar DataFrame com resultados
df_result = pd.DataFrame(registros)

# 9. Criar GeoDataFrame para espacializar
gdf = gpd.GeoDataFrame(
    df_result,
    geometry=gpd.points_from_xy(df_result.Longitude, df_result.Latitude),
    crs='EPSG:4326'
)

# 10. Salvar GeoJSON
output_path = r'C:\Users\mateus.souza\Downloads\Dados_Bdbmep\Resumo_estacoes3.geojson'
gdf.to_file(output_path, driver='GeoJSON')

print('Processo concluído! GeoDataFrame criado com', len(gdf), 'registros.')
print('Arquivo salvo em:', output_path)