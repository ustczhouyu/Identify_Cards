import requests
from lxml import etree

class business_license:
    def __init__(self, img, url):
        self.img = img
        self.url = url
        self.res = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Host':'gsxt.ynaic.gov.cn',
            'Accept-Language':'zh-CN,zh;q=0.9', 
            'Cache-Control':'max-age=0',
            'Cookie':'td_cookie=18446744070275471524; JSESSIONID_NOTICE=PEeKGSJ0xnGvqEgZhz6KlKrioGCueJUnd08tFtcaKIz7AEztgPe4!-829753696; CoreSessionId=2ccade8d82805b36e7c1e6ce49e40a66d066eac36765dd88; _g_sign=12b1836088d0bbd670f7e439bf665533; UM_distinctid=1747abec03d59a-0e79c03fc46e0c-333769-1fa400-1747abec03e806; elvasid=2c2d212f65c006254babec2438027e76; sign_cookie=010ec1f727bbd3add4986674097478bc; verify_cookie=7985dce80320ceb4dfbc0dfd97d888c6; CNZZDATA1000298231=1936832156-1599786705-http%253A%252F%252Fgsxt.ynaic.gov.cn%252F%7C1600044741; notice=13493987'
            }
        self.fields = ['统一社会信用代码', '企业名称', '类型', '经营者', '组成形式', '注册日期', '登记机关', '登记状态', '经营场所', '经营范围']
        self.response = self.request(self.url)
        self.xpath_structured(self.response)

    def request(self, url):
        return requests.get(url, headers=self.headers)
        
    def xpath_structured(self, response):
        tree = etree.HTML(response.text)
        for field in self.fields:
            content = tree.xpath("//table[@class='tableYyzz']//td[contains(text(), '{field}')]/i/text()".format(field=field))
            if content:
                self.res[field] = content[0]
