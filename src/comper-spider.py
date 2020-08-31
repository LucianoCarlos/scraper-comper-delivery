import scrapy
from urllib.parse import urlencode
from enum import Enum

headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
           'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
           'Connection': 'keep-alive',
           'Referer': 'https://www.comperdelivery.com.br/'}


class Location(Enum):
    MT = '1'
    MS = '2'
    DF = '3'


class ComperSpider(scrapy.Spider):
    name = 'comperspider'
    LIMIT = OFFSET = 32

    def __init__(self, name=None, location='DF', **kwargs):
        self.location = location
        super().__init__(name=name, **kwargs)

    def start_requests(self):
        if self.location not in [l.name for l in Location]:
            raise scrapy.exceptions.CloseSpider('Localidade não encontrada.')

        params = {
            'sc': f'{Location[self.location].value}',
            'referrer': 'https://www.comperdelivery.com.br/',
        }

        # Seleciona localidade desejada
        # O cookie é configurado nas próximas requisições para identificar a localidade
        return [scrapy.Request(
            f'https://www.comperdelivery.com.br/Site/Track.aspx?{urlencode(params)}',
            headers=headers,
            callback=self.parse)]

    def parse(self, response):
        ''' Recupera a lista de categorias
        '''
        yield scrapy.Request(
            response.urljoin('/api/catalog_system/pub/category/tree/3/'),
            headers=headers,
            callback=self.parse_category
        )

    def parse_category(self, response):
        for category in response.json():

            params = {
                'fq': f'C:/{category["id"]}/',
                'PS': '32',
                'sl': 'df48a27d-fc0a-47cd-8087-ac49751cd86b',
                'cc': '32',
                'sm': '0',
                'PageNumber': '1',
                'O': 'OrderByScoreDESC',
                '_from': 0,
                '_to': ComperSpider.LIMIT - 1}

            yield scrapy.Request(
                response.urljoin(
                    f'/api/catalog_system/pub/products/search?{urlencode(params)}'),
                callback=self.parse_product,
                cb_kwargs=params
            )

    def parse_product(self, response, **kwargs):

        product_list = response.json()

        for product in product_list:
            #  Preço
            price = product['items'][0]['sellers'][0]['commertialOffer']['Price']

            # Disponibilidade
            availability = product['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'] != 0

            yield {
                "name": product['productName'],
                "img_url": product['items'][0]['images'][0]['imageUrl'],
                "price": price,
                "availability": availability,
                "url": product['link']
            }

        # Segue paginação dos produtos
        if len(product_list):
            params = kwargs
            params['_to'] += ComperSpider.OFFSET
            params['_from'] += ComperSpider.OFFSET

            yield scrapy.Request(
                response.urljoin(
                    f'/api/catalog_system/pub/products/search?{urlencode(params)}'),
                callback=self.parse_product,
                cb_kwargs=params
            )
