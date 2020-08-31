### Objetivo

Capturar dados do e-commerce [comper delivery](https://www.comperdelivery.com.br/).

### Instalação e execução

1.  Faça o download e instale o [Python](https://www.python.org/) de acordo com seu sistema operacional. A versão utilizada no desenvolvimento desse projeto foi a **3.6**.

2.  Instale o [Scrapy](https://scrapy.org/).
    <code>\$ pip install -r requirements.txt</code>

    O Scrapy é uma das bibliotecas de scraping mais populares e poderosas do Python, abaixo algumas das suas funcionalidades utilizadas:

    - Um shell interativo para testar expressões CSS e XPath.
    - Suporte integrado para gerar exportações no formato JSON.
    - Cache de requisições.

3.  Execute o *scraper*.
    <code>\$ scrapy runspider -o output.json -a location=DF -s CLOSESPIDER_PAGECOUNT=3 src/comper-spider.py </code>

    - -o: especifica o arquivo de saída.
    - CLOSESPIDER_PAGECOUNT: especifica o número máximo de respostas a rastrear, garante a coleta somente da primeira página de produtos.
    - location: Seleciona a região: DF, MT e MS.

4. Formato JSON
```json
 [{
    "name": "string",
    "img_url": "string",
    "price": "double",
    "availability": "boolean",
    "url": "string"
  }]
```
