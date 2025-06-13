# bdmep_temperatura_geojson

Este script lê arquivos CSV de estações meteorológicas do BDMEP, extrai as temperaturas máximas e mínimas, calcula a média por mês e gera um arquivo GeoJSON com as informações e a localização das estações.

✅ Feito para funcionar diretamente com os arquivos originais do BDMEP
O script é compatível com os arquivos CSV baixados diretamente do site do BDMEP, sem necessidade de edição ou pré-processamento.

🔧 Configuração padrão
Atualmente, o script processa os meses de outubro (10), novembro (11) e dezembro (12), mas essa seleção é facilmente customizável para qualquer outro mês, bastando alterar a lista de meses no código.

## O que o script faz:
Lê os metadados de cada CSV (nome, latitude, longitude).

Filtra os dados para os meses definidos.

Calcula as médias de temperatura máxima e mínima por mês.

Gera um GeoDataFrame e salva em formato GeoJSON.

## Bibliotecas necessárias:
pandas

geopandas

shapely

os

## Como usar:
Copie o caminho dos arquivos CSV da BDMEP da pasta original baixada do sistema.

Atualize o caminho da pasta no script (pasta_csv).

Ajuste a lista de meses conforme necessidade (Opcional).

Execute o script.

O resultado será um arquivo .geojson com as médias de temperatura por estação.