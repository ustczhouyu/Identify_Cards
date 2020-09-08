import re
import json
import pandas as pd
import difflib
import Levenshtein
import numpy as np

def get_difflib_dis(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def get_Levenshtein_dis(str1, str2):
   return Levenshtein.ratio(str1, str2)
   
def fix_birthplace(birthplace, idnum, df_district, areacode_unit_address):

    birthplace = ''.join(re.findall('[\u4e00-\u9fa5]', birthplace))

    matchObj = re.match('(\w+省)?(\w+市)?(\w+[区县])?', birthplace)
    province = matchObj[1] 
    city = matchObj[2]
    district = matchObj[3]

    area_code = idnum[:6]

    # 假如区县在dict中，基本是准确的，此时直接返回即可
    if district in list(df_district['name']):
        return birthplace
    # 假如区县非空，且在dict中找不到，有可能是部分字体识别错误，此时对比识别出的曲线与字典中区县最近的那一个
    elif district:
        list_filter = list(df_district.loc[df_district.provinceCode == int(idnum[:2]), 'name'])
        dis_difflib = [get_difflib_dis(district[:-1], x[:-1]) for x in list_filter]
        dis_Levenshtein = [get_Levenshtein_dis(district[:-1], x[:-1]) for x in list_filter]
        dis = np.array(dis_difflib) + np.array(dis_Levenshtein)

        index = np.where(dis == np.max(dis))[0]
        # 有可能识别出多个，此时进行进一步的判断
        if len(index) == 1:
            code = df_district[df_district.provinceCode == int(idnum[:2])].iloc[index[0], 0]
            return areacode_unit_address[str(code)]['address']
        elif len(index) > 1:
            exact_distinct = df_district.loc[df_district.code == int(idnum[:6])]['name']
            exact_distinct = ''.join([i for i in exact_distinct])
            index_ = list_filter.index(exact_distinct)
            if index_ in index:
                birthday = areacode_unit_address[area_code]['address']
                return birthday

    # 假如没有识别出区县，直接拿身份证号的前6位去字典中匹配
    elif not district:
        try:
            district = areacode_unit_address[area_code]['address']
        except:
            pass
    return birthplace

if __name__ == '__main__':
    areacode_unit_address = json.load(open('./Postprocessing/data/areacode_unit_address.json', "r", encoding="utf-8"))
    df_provinces = pd.read_csv('./Postprocessing/data/provinces.csv')
    df_district = pd.read_csv('./Postprocessing/data/district.csv')
    district = fix_birthplace('湖南省南县', '430122199104250341')

    print(district) 