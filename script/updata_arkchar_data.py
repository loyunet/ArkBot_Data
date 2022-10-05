import re
import requests
import json

from urllib.parse import quote

arkdata = json.loads(requests.get(
    'https://ak-conf.hypergryph.com/config/prod/official/Android/version').text)['clientVersion']
localdata = json.loads(requests.get(
    'https://cdn1.tianli0.top/gh/loyunet/ArkBot_Data@master/char_list.json').text)['ark_clientVersion']
if arkdata != localdata:
    print('数据过时，开始更新')
    char_response = requests.get(
        'https://wiki.biligame.com/arknights/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88')
    char_re = re.findall(
        r'<p class="handbook-item-name">(.*?)</p>', char_response.text)
    char_re_num = len(char_re)
    returndata = {}
    returndata['ark_clientVersion'] = arkdata
    returndata['data'] = {}
    num = 0
    for i in char_re:
        if i == '阿米娅（近卫）':
            i = '阿米娅(近卫)'
        data_response = requests.get(
            'https://prts.wiki/w/' + quote(i, 'utf-8'))
        data_re = re.findall(
            r'</p><div id="voice-data-root" data-voice-key="(.*?)" data-voice-base="', data_response.text)[0]
        returndata['data'][i] = data_re
        num = num + 1
        print(f"{i}：OK({num}/{char_re_num})")
    returnjson = json.dumps(returndata, ensure_ascii=False)
    file = open('../char_list.json', 'w', encoding='utf-8')
    file.write(returnjson)
    file.close()
else:
    print('数据为最新')
