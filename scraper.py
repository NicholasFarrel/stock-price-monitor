import requests
from bs4 import BeautifulSoup
import csv 
import re # Importa a biblioteca de expressões regulares para limpeza de texto

# URL da página principal que contém as listas de altas e baixas.
URL = 'https://statusinvest.com.br/acoes'

# Define o User-Agent para simular um navegador real e evitar o erro 403.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

# Realiza a requisição HTTP para a URL, passando os headers definidos.
try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a página: {e}")
    exit()

# Cria o objeto BeautifulSoup a partir do conteúdo HTML da resposta.
soup = BeautifulSoup(response.text, 'html.parser')

def extrair_dados_secao(nome_secao):
    """
    Função para extrair dados de uma seção de ações (altas ou baixas)
    com base no nome da seção.
    """
    print(f"Extraindo dados da seção '{nome_secao}'...")

    secao_container = soup.find('h3', string=nome_secao.upper())
    
    if not secao_container:
        print(f"Seção '{nome_secao}' não encontrada.")
        return []
    
    lista_de_itens = secao_container.find_next_sibling('div').find_all('div', role='listitem')
    
    dados_secao = []
    
    for item in lista_de_itens:
        try:
            # --- Início das correções de extração ---

            # Extrai o Ticker e o Nome da Empresa separadamente para evitar repetição.
            # O ticker está no texto direto do <h4>, sem a sub-tag.
            ticker_tag = item.find('h4', title='ticker/código do ativo')
            ticker = ticker_tag.find(text=True, recursive=False).strip()
            
            # O nome da empresa está na tag <small> aninhada.
            nome_tag = item.find('small', title='Nome da empresa')
            nome = nome_tag.text.strip() if nome_tag else 'N/A'

            # Extrai a variação, limpando o texto da seta e os espaços extras.
            variacao_tag = item.find('span', title='Variação atual no preço do ativo')
            variacao_texto = variacao_tag.text.strip()
            variacao = re.sub(r'arrow_(up|down)ward', '', variacao_texto).strip()

            # O preço está na tag <span> com o título.
            preco_tag = item.find('span', title='Preço atual do ativo')
            preco = preco_tag.text.strip().replace('R$', '').strip()

            # --- Fim das correções de extração ---

            dados_secao.append({
                'ticker': ticker,
                'nome': nome,
                'variacao': variacao,
                'preco': preco,
                'categoria': nome_secao
            })
        except (AttributeError, TypeError):
            continue
    
    return dados_secao

# ---

# Chama a função para extrair os dados das seções de altas e baixas.
dados_altas = extrair_dados_secao('ALTAS')
dados_baixas = extrair_dados_secao('BAIXAS')

# Combina as duas listas de dados em uma única lista.
todos_dados = dados_altas + dados_baixas

# ---

# Exporta os dados combinados para um arquivo CSV.
nome_arquivo = 'altas_e_baixas.csv'

# Define os nomes das colunas para o arquivo CSV.
nomes_colunas = ['ticker', 'nome', 'variacao', 'preco', 'categoria']

# Abre o arquivo CSV em modo de escrita e cria um escritor de dicionários.
with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=nomes_colunas)
    
    # Escreve a linha de cabeçalho no arquivo.
    writer.writeheader()
    
    # Escreve todas as linhas de dados.
    writer.writerows(todos_dados)

print(f"\nDados exportados com sucesso para '{nome_arquivo}'!")