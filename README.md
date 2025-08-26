# Monitoramento de Ações: Altas e Baixas

Este projeto é um web scraper em **Python** que monitora as maiores altas e baixas diárias do mercado de capitais brasileiro, com base na página principal do Status Invest.

O script coleta e organiza os dados do top 5 de ações em alta e em baixa, exportando-os para um formato acessível e estruturado.

### Funcionalidades

* Extrai dados de ações, incluindo ticker, nome da empresa, variação percentual e preço.
* Coleta informações de duas categorias: "Altas do Dia" e "Baixas do Dia".
* Salva os dados de forma limpa e organizada em um arquivo CSV.

### Tecnologias Utilizadas

* **Python**: Linguagem principal do projeto.
* **Requests**: Para fazer as requisições HTTP e acessar o conteúdo da página.
* **BeautifulSoup**: Para navegar e extrair informações do HTML de forma eficiente.
* **Módulo CSV**: Para exportar os resultado para um arquivo de planilha.

### Como Executar o Projeto

1.  **Clone o Repositório:**
    `git clone https://github.com/NicholasFarrel/stock-price-monitor.git`

2.  **Instale as Dependências:**
    ```bash
    pip install requests
    pip install beautifulsoup4
    ```

3.  **Execute o Script:**
    ```bash
    python scraper.py
    ```

Após a execução, um arquivo chamado `altas_e_baixas.csv` será criado na mesma pasta do script, contendo todos os dados coletados.
