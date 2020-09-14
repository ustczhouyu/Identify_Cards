import re

class taxi_receipt:
    """
    增值税机打发票结构化识别
    识别字段包括：发票代码、发票号码、车号、日期、上下车时间、总金额
    """
    def __init__(self, img, result):
        self.img = img
        self.result = result
        self.N = len(self.result)
        self.res = {}   
        self.code()  # 发票代码
        self.number()  # 发票号码
        self.carnum() # 车号
        self.date()  # 日期
        self.get_in_and_get_off()  # 上下车时间
        self.total_price()  # 金额

    def code(self):
        """
        发票代码识别
        """
        No = {}
        res1 = re.findall(' \d{12} ', self.result)
        if len(res1) > 0:
            No["发票代码"] = res1[0]
            self.res.update(No)

    def number(self):
        """
        识别发票号码
        """
        nu = {}
        res1 = re.findall(' \d{8} ', self.result)
        if len(res1) > 0:
            nu["发票号码"] = res1[0]
            self.res.update(nu)
                
    def date(self):
        """
        识别开票日期
        """
        da = {}
        res1 = re.findall('(\d{4}-\d{1,2}-\d{1,2})', self.result)
        if len(res1) > 0:
            da["日期"] = res1[0]
            self.res.update(da)

    def carnum(self):
        """
        识别车号
        """
        text = re.sub('\s+', '', self.result).strip()
        da = {}
        res1 = re.findall('[\u4E00-\u9FA5]{1}[A-Z]{1}[A-Z0-9]{5}', text)
        if len(res1) > 0:
            da["车号"] = res1[-1]
            self.res.update(da)    
    
    def total_price(self):
        """
        识别金额
        """
        price = {}
        res1 = re.findall('\d+\.\d{2}元 ', self.result)
        if len(res1) > 0:
            price["金额"] = res1[-1]
            self.res.update(price)        
    
    def get_in_and_get_off(self):
        """
        上下车时间
        """
        d = {}
        text = self.result.replace('：', ':')
        res1 = re.findall('上车 (\d{2}[:：]\d{2})', text)
        if len(res1) > 0:
            d["上车"] = res1[-1]
            self.res.update(d)                
        res1 = re.findall('下车 (\d{2}[:：]\d{2})', text)
        if len(res1) > 0:
            d["下车"] = res1[-1]
            self.res.update(d)          
