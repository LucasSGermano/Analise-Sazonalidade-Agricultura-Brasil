# Análise de Sazonalidade para Produção de Sementes no Brasil

Este projeto realiza um ciclo completo de análise de dados para identificar como padrões sazonais e climáticos impactam a produtividade agrícola no Brasil. O objetivo é transformar dados brutos do governo em insights acionáveis para produtores de sementes, utilizando um fluxo de trabalho híbrido com Python e Power Query.

## 🎯 Objetivo
Analisar dados de produção de sementes (SIGEF) e cruzá-los com dados climáticos históricos (INMET) para identificar quais estações do ano são mais propícias para o plantio das principais culturas, fornecendo recomendações estratégicas.

## 🛠️ Ferramentas e Tecnologias
* **Python:** Utilizado para a limpeza inicial dos dados de produção e para a automação do fluxo final de análise e geração de relatórios.
    * **Bibliotecas:** Pandas, Matplotlib, Seaborn, FPDF2.
* **Excel / Power Query:** Utilizado para a complexa tarefa de ETL (Extração, Transformação e Carga), consolidando e limpando mais de 500 arquivos CSV de dados climáticos e agregando os dados horários em um resumo diário.

## 📂 Fontes de Dados
Os dados brutos utilizados neste projeto são públicos e podem ser encontrados nas seguintes fontes:
* **Produção:** [SIGEF - Campos de Produção de Sementes](https://dados.gov.br/dados/conjuntos-dados/dados-referentes-ao-controle-da-producao-de-sementes-sigef)
* **Clima:** [INMET - Banco de Dados Meteorológicos](https://bdmep.inmet.gov.br/)

## 📊 Principal Resultado
A análise identificou padrões claros de produtividade ao longo do ano. O gráfico abaixo demonstra a variação da produtividade da Soja (Glycine max), a principal cultura do dataset, em relação à temperatura média de cada estação, confirmando a **Primavera** como a estação mais produtiva.

*(Lembre-se de apagar esta linha e arrastar o seu arquivo .png do gráfico da Soja para cá)*
![Gráfico de Produtividade vs. Temperatura para Soja]<img width="4200" height="2400" alt="grafico_sazonal_Glycine_max_(L)_Merr" src="https://github.com/user-attachments/assets/47ef068b-3597-4166-8fe8-d9da3c599b97" />

## 📁 Arquivos do Projeto
* **/relatorio_profissional.pdf:** O relatório final completo em formato PDF, contendo um resumo das 10 principais culturas e uma análise aprofundada, com gráficos e recomendações, para cada uma das 3 mais relevantes.
* **/limpeza_final.py:** Script Python para a limpeza e preparação inicial dos dados brutos de produção de sementes.
* **/relatorio_completo.py:** O script Python final que realiza a análise de sazonalidade e gera o relatório completo em PDF.

## 🚀 Como Executar o Fluxo de Trabalho
O projeto é dividido em duas grandes etapas, refletindo um fluxo de trabalho real de análise de dados:

**Etapa 1: Preparação e Enriquecimento dos Dados (ETL)**
O arquivo de dados principal para a análise (`producao_analise_final.csv`) não está incluído neste repositório devido ao seu tamanho. Ele é o resultado do seguinte processo de ETL:
1.  Execute o script `limpeza_final.py` para limpar o arquivo de produção original (baixado da fonte SIGEF), gerando o arquivo `producao_sementes_limpa.csv`.
2.  Utilize o Power Query para consolidar, limpar e agregar os 500+ arquivos de dados climáticos do INMET (2013-2025), transformando-os em um resumo diário.
3.  Ainda no Power Query, mescle o `producao_sementes_limpa.csv` com a tabela de clima diário para criar a base de dados final e enriquecida.
4.  Exporte o resultado como `producao_analise_final.csv`.

**Etapa 2: Análise e Geração do Relatório (Python)**
1.  **Pré-requisitos:** Instale todas as bibliotecas necessárias.
    ```bash
    pip install pandas matplotlib seaborn fpdf2
    ```
2.  **Execução:** Coloque o script `relatorio_completo.py` e o arquivo `producao_analise_final.csv` (gerado na etapa anterior) na mesma pasta e rode o seguinte comando no terminal:
    ```bash
    python relatorio_completo.py
    ```
3.  **Resultado:** O script irá gerar o relatório `relatorio_profissional.pdf` e as imagens dos gráficos na pasta.
