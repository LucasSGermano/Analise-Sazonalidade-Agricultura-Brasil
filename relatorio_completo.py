import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

def gerar_relatorio_pdf_profissional(caminho_arquivo_dados):
    """
    Script definitivo que gera um relatório profissional em PDF, mostrando primeiro um
    resumo das Top 10 culturas e depois uma análise aprofundada para as Top 3.
    """
    print("--- INICIANDO GERAÇÃO DE RELATÓRIO PROFISSIONAL EM PDF ---")

    # --- Etapa 1: Carregar e Analisar os Dados ---
    try:
        df = pd.read_csv(caminho_arquivo_dados, sep=';', decimal=',')
        print("Arquivo de dados carregado com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_arquivo_dados}' não encontrado.")
        return

    print("Realizando análise de sazonalidade...")
    df['Producao bruta'] = pd.to_numeric(df['Producao bruta'], errors='coerce')
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    df['Temp_Media_Dia'] = pd.to_numeric(df.get('Temp_Media_Dia'), errors='coerce')
    df.dropna(subset=['Producao bruta', 'Area', 'Estacao_do_Ano', 'Especie'], inplace=True)
    df = df[df['Area'] > 0]
    df['Produtividade_kg_ha'] = df['Producao bruta'] / df['Area']

    analise_geral = df.groupby(['Estacao_do_Ano', 'Especie']).agg(
        Produtividade_Media_kg_ha=('Produtividade_kg_ha', 'mean'),
        Temperatura_Media_C=('Temp_Media_Dia', 'mean')
    ).round(2)
    
    # Identificar as 3 principais culturas
    principais_especies = df['Especie'].value_counts().nlargest(3).index
    # Criar a tabela Top 10 para o relatório
    top_10_especies = df['Especie'].value_counts().nlargest(10).reset_index()
    top_10_especies.columns = ['Cultura', 'Numero de Registros']
    
    print(f"Análise concluída. Foco nas 3 principais culturas: {list(principais_especies)}")

    # --- Etapa 2: Gerar os Gráficos ---
    print("\nGerando gráficos para as principais culturas...")
    nomes_dos_graficos = []
    # (O código para gerar os gráficos permanece o mesmo)
    for especie in principais_especies:
        analise_focada = analise_geral.loc[(slice(None), especie), :]
        ordem_estacoes = ['Primavera', 'Verao', 'Outono', 'Inverno']
        analise_focada = analise_focada.reindex(ordem_estacoes, level='Estacao_do_Ano')
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=analise_focada.index.get_level_values('Estacao_do_Ano'), y='Produtividade_Media_kg_ha', data=analise_focada, ax=ax1, color='#4c72b0', label='Produtividade Média (kg/ha)')
        ax1.set_xlabel('Estação do Ano de Plantio', fontsize=12)
        ax1.set_ylabel('Produtividade Média (kg/ha)', fontsize=12, color='#4c72b0')
        ax2 = ax1.twinx()
        sns.lineplot(x=analise_focada.index.get_level_values('Estacao_do_Ano'), y='Temperatura_Media_C', data=analise_focada, ax=ax2, color='#dd8452', marker='o', linewidth=2.5, label='Temperatura Média (°C)')
        ax2.set_ylabel('Temperatura Média (°C)', fontsize=12, color='#dd8452')
        plt.title(f'Análise Sazonal para {especie}', fontsize=16, weight='bold', pad=20)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper right')
        fig.tight_layout()
        nome_grafico = f'grafico_{especie.replace(" ", "_").replace(".", "")[:20]}.png'
        plt.savefig(nome_grafico, dpi=200)
        nomes_dos_graficos.append(nome_grafico)
        plt.close()
    print("Gráficos salvos com sucesso.")

    # --- Etapa 3: Montar o PDF Profissional ---
    print("Montando o relatório PDF profissional...")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 10, 'Relatório de Análise de Sazonalidade', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 11)
    texto_intro = (
        "Este relatório apresenta uma análise sobre o impacto de fatores sazonais e climáticos na produtividade de sementes, com base nos dados de produção de 2013 a 2025. "
        "A análise aprofundada a seguir foca nas 3 culturas mais representativas do conjunto de dados, conforme justificado pela tabela abaixo."
    )
    pdf.multi_cell(0, 6, texto_intro)
    pdf.ln(5)

    # --- MUDANÇA AQUI: Inserindo a tabela Top 10 como justificativa ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Top 10 Culturas por Volume de Registros Analisados', 0, 1, 'L')
    pdf.set_font('Courier', 'B', 10)
    # Cabeçalho da tabela
    pdf.cell(130, 6, 'Cultura', 1, 0, 'L')
    pdf.cell(40, 6, 'Registros', 1, 1, 'C')
    # Corpo da tabela
    pdf.set_font('Courier', '', 9)
    for index, row in top_10_especies.iterrows():
        pdf.cell(130, 6, row['Cultura'][:60], 1, 0, 'L') # Limita o tamanho do texto da cultura
        pdf.cell(40, 6, str(row['Numero de Registros']), 1, 1, 'C')
    pdf.ln(10)

    # --- Análise detalhada para cada cultura principal (sem alteração) ---
    for i, especie in enumerate(principais_especies):
        pdf.add_page()
        # ... (O resto do código para gerar as páginas individuais com gráfico e texto é o mesmo)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Análise Detalhada para: {especie}', 0, 1, 'C')
        pdf.ln(5)
        pdf.image(nomes_dos_graficos[i], x=10, y=None, w=190)
        pdf.ln(5)
        analise_focada = analise_geral.loc[(slice(None), especie), :]
        ordem_estacoes = ['Primavera', 'Verao', 'Outono', 'Inverno']
        analise_focada = analise_focada.reindex(ordem_estacoes, level='Estacao_do_Ano')
        melhor_estacao = analise_focada['Produtividade_Media_kg_ha'].idxmax()
        pior_estacao = analise_focada['Produtividade_Media_kg_ha'].idxmin()
        dados_melhor_estacao = analise_focada.loc[melhor_estacao]
        dados_pior_estacao = analise_focada.loc[pior_estacao]
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Conclusões e Recomendações:', 0, 1, 'L')
        pdf.set_font('Arial', '', 11)
        texto_conclusao = (
            f"Melhor Estação: '{melhor_estacao}', com produtividade média de {dados_melhor_estacao['Produtividade_Media_kg_ha']:.2f} kg/ha (Temp. Média: {dados_melhor_estacao['Temperatura_Media_C']:.2f}°C).\n"
            f"Pior Estação: '{pior_estacao}', com produtividade média de {dados_pior_estacao['Produtividade_Media_kg_ha']:.2f} kg/ha (Temp. Média: {dados_pior_estacao['Temperatura_Media_C']:.2f}°C).\n\n"
            f"Recomendação: O plantio na '{melhor_estacao}' é o mais indicado para otimizar o rendimento desta cultura."
        )
        pdf.multi_cell(0, 6, texto_conclusao)

    nome_pdf_final = 'relatorio_profissional.pdf'
    pdf.output(nome_pdf_final)
    print(f"Relatório profissional em PDF '{nome_pdf_final}' criado com sucesso!")

    for grafico in nomes_dos_graficos:
        os.remove(grafico)
    print("Arquivos de imagem temporários removidos.")


# --- Execução ---
arquivo_final_csv = "dados_finais_para_analise.csv" 
gerar_relatorio_pdf_profissional(arquivo_final_csv)