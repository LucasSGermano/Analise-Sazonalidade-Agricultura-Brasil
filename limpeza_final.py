# --- Bloco 1: Importação das Bibliotecas ---
# Primeiro, importamos as ferramentas que vamos usar.
# 'pandas' é a biblioteca principal para trabalhar com tabelas (que chamamos de DataFrames) em Python.
# 'numpy' é uma biblioteca para cálculos numéricos, que nos ajuda com a fórmula da produtividade.

import pandas as pd
import numpy as np

# --- Bloco 2: Definição da Função Principal ---
# Criamos uma "função" para organizar nosso código. Pense nela como uma "caixa" que contém toda a nossa receita de limpeza.
# Ela recebe o nome do arquivo sujo (caminho_arquivo_original) e o nome que queremos dar ao arquivo limpo (caminho_arquivo_final).

def limpeza_definitiva(caminho_arquivo_original, caminho_arquivo_final):
    """
    Função definitiva para carregar o arquivo de sementes, aplicar todas as
    regras de limpeza que definimos, e salvar um arquivo final pronto para análise.
    """
    
    # Imprimimos uma mensagem para saber que o processo começou.
    print("--- INICIANDO PROCESSO DE LIMPEZA DEFINITIVO ---")
    
    # --- Bloco 3: Carregamento dos Dados Brutos ---
    # Usamos um 'try-except' para o caso de o arquivo não ser encontrado. É uma boa prática para evitar erros.
    try:
        # Aqui, o pandas lê o nosso arquivo CSV.
        # delimiter=';' diz que as colunas são separadas por ponto e vírgula.
        # encoding='latin-1' diz ao pandas como ler os caracteres com acentos do arquivo original.
        df = pd.read_csv(caminho_arquivo_original, delimiter=';', encoding='latin-1')
        
        # Imprime uma confirmação e o número total de linhas antes da limpeza.
        print(f"PASSO 1: Arquivo original carregado. Total de linhas: {len(df)}")
    except FileNotFoundError:
        print(f"Erro Crítico: O arquivo '{caminho_arquivo_original}' não foi encontrado. Verifique se ele está na mesma pasta que o script.")
        return

    # --- Bloco 4: Limpeza e Tratamento dos Dados ---

    # 4.1 - Correção de Acentos (um passo importante antes de salvar)
    # Aqui, nós percorremos todas as colunas que são de texto ('object').
    # Para cada uma, aplicamos a "tradução" de 'latin-1' para 'utf-8', que é o formato universal e correto.
    print("Corrigindo acentuação das colunas de texto...")
    for coluna in df.select_dtypes(include=['object']).columns:
        df[coluna] = df[coluna].str.encode('latin-1', 'ignore').str.decode('utf-8', 'ignore')

    # 4.2 - Filtro de Datas Válidas
    # Converte a coluna 'Data do Plantio' para o formato de data.
    # dayfirst=True ajuda o pandas a entender o formato "DD/MM/AAAA".
    # errors='coerce' transforma qualquer data inválida (como um texto) em um valor Nulo (NaT).
    df['Data do Plantio'] = pd.to_datetime(df['Data do Plantio'], dayfirst=True, errors='coerce')
    
    # Remove qualquer linha que tenha ficado com a data nula após a conversão.
    df.dropna(subset=['Data do Plantio'], inplace=True)
    
    # Aplica o nosso filtro de datas que decidimos juntos.
    # Manter apenas as linhas com data entre 01/01/2013 e 16/07/2025.
    df_filtrado_data = df[(df['Data do Plantio'] >= '2013-01-01') & (df['Data do Plantio'] <= '2025-07-16')].copy()
    print(f"PASSO 2: Linhas após filtro de datas válidas (01/01/2013 a 16/07/2025): {len(df_filtrado_data)}")

    # 4.3 - Preenchimento de Nulos na Coluna 'Categoria'
    # Esta linha encontra todas as células vazias (NaN) na coluna 'Categoria' e preenche com "NAO INFORMADO".
    df_filtrado_data['Categoria'].fillna('NAO INFORMADO', inplace=True)
    print("Passo extra: Valores nulos em 'Categoria' preenchidos.")

    # 4.4 - Filtro de Relevância (manter apenas dados com produção)
    # Converte a coluna 'Producao bruta' para número, transformando erros em nulos.
    df_filtrado_data['Producao bruta'] = pd.to_numeric(df_filtrado_data['Producao bruta'], errors='coerce')
    
    # Remove as linhas onde a 'Producao bruta' é nula.
    df_relevante = df_filtrado_data.dropna(subset=['Producao bruta']).copy()
    
    # Remove as linhas onde a produção é zero (não nos ajudam a calcular produtividade).
    df_relevante = df_relevante[df_relevante['Producao bruta'] > 0].copy()
    print(f"PASSO 3: Linhas após manter apenas registros com produção: {len(df_relevante)}")

    # 4.5 - Filtro de Outliers (a nossa técnica de produtividade)
    # Garante que a coluna 'Area' também é numérica.
    df_relevante['Area'] = pd.to_numeric(df_relevante['Area'], errors='coerce')
    df_relevante.dropna(subset=['Area'], inplace=True)
    df_relevante = df_relevante[df_relevante['Area'] > 0].copy()
    
    # Cria a coluna temporária com o cálculo da produtividade.
    df_relevante['Produtividade_kg_ha'] = df_relevante['Producao bruta'] / df_relevante['Area']
    
    # Aplica o nosso filtro de 100.000 kg/ha, mantendo apenas as linhas realistas.
    df_final = df_relevante[df_relevante['Produtividade_kg_ha'] <= 100000].copy()
    print(f"PASSO 4: Linhas após remover outliers de produtividade (> 100.000 kg/ha): {len(df_final)}")
    
    # Remove a coluna de produtividade que só serviu para nos ajudar na limpeza.
    df_final.drop(columns=['Produtividade_kg_ha'], inplace=True)
    

    # --- Bloco 5: Salvando o Arquivo Final ---
    try:
        # Aqui, salvamos nosso DataFrame limpo em um novo arquivo CSV.
        # index=False para não salvar o índice do pandas no arquivo.
        # sep=';' para que o Excel abra facilmente.
        # decimal=',' para usar vírgula como separador decimal.
        # encoding='utf-8-sig' é o formato final que garante que os acentos funcionem no Excel.
        df_final.to_csv(caminho_arquivo_final, index=False, sep=';', decimal=',', encoding='utf-8-sig')
        
        # Mensagem final de sucesso!
        print(f"\n--- PROCESSO CONCLUÍDO ---")
        print(f"O arquivo final e limpo '{caminho_arquivo_final}' foi criado com {len(df_final)} linhas.")
        print("Este é o nosso ponto de partida seguro e correto para a análise de sazonalidade.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# --- Bloco 6: Execução do Script ---
# Aqui nós definimos os nomes dos arquivos e chamamos a nossa função para fazer todo o trabalho.

# Nome do arquivo original que você baixou.
arquivo_original_novo = 'sigefcamposproducaodesementes.csv'

# Nome que daremos ao nosso novo arquivo, limpo e pronto.
arquivo_limpo_final = 'producao_sazonal_limpo_final.csv'

# Chamando a função para executar a limpeza.
limpeza_definitiva(arquivo_original_novo, arquivo_limpo_final)