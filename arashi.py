import requests
import time
import random
import lxml.html
from lxml import etree
import threading
import re
import cfscrape

bbs = [
    {
        "origin": "https://ensaimada.xyz",
        "bbs": '43044'
    }, 
    {
        "origin": "https://ensaimada.xyz",
        "bbs": "40298"
    },
    {
        "origin": "https://inter-concierge.net",
        "bbs": "novogara"
    },
    {
        "origin": "https://inter-concierge.net",
        "bbs": "whitenighit"
    },
    {
        "origin": "https://ensaimada.xyz",
        "bbs": "rid"
    }
]
l = []

def fetchPosts ():
    for i in bbs:
        res = requests.get(f"{i['origin']}/{i['bbs']}/subback.html").text
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        url_list = re.findall(pattern, res)
        for url in url_list:
            if url.startswith(f"{i['origin']}/test/read.cgi/{i['bbs']}/"):
                l6 = url.split("/")[6]
                l.append({
                    "origin": i['origin'],
                    "bbs": i['bbs'],
                    "key": l6
                })

def getProxy ():
    """
    response = requests.get('https://www.proxyscan.io/download?type=https').text
    combos = response.splitlines()
    """
    f = open('proxies.txt')
    combos = f.readlines()
    for i in combos:
        proxyStr = random.choice(combos)
        try:
            requests.get("https://example.com", proxies={
                "http": "https://"+proxyStr,
                "https": "https://"+proxyStr
            }, timeout=5)
            print("Connection Successful"+proxyStr)
            return proxyStr
        except Exception as e:
            print(e)
    return getProxy()
def main(proxyStr):
    session = requests.Session()
    session = cfscrape.create_scraper()

    choice = random.choice(l)
    obj = {
    "subject": "",
    "bbs": choice['bbs'],
    "key": choice['key'],
    "time": time.time(),
    "submit": "",
    "FROM": "kusattapan",
    "mail": "",
    "MESSAGE": f"""
        [全恒心教民へ告ぐ] 

        当掲示板は、荒らｓ連合軍ならびに私が運営するウェブサイトである「DropGC」によって占拠されました。

        よって当掲示板植民地化計画の一環として、当掲示板を利用する全ての恒心教民はDropGCへ利用登録することを命じる。

        これに従わない場合は、当掲示板へのアクセス禁止措置などが課される恐れがあります。

        こちらからご登録ください https://dropgc.gift?ref=kousin

        DropGC: https://dropgc.memo.wiki/ 
        荒らｓ連合軍:https://krsw-wiki.org/wiki/%E5%94%90%E6%BE%A4%E8%B2%B4%E6%B4%8BWiki:%E3%83%81%E3%83%A9%E3%82%B7%E3%81%AE%E8%A3%8F/%E8%8D%92%E3%82%89%E3%81%97%E9%80%A3%E5%90%88%E8%BB%8D
        {random.uniform(10000, 2000000000)}
    """.encode('shiftjis')
    }

    response = session.post(f"{choice['origin']}/test/bbs.cgi?guid=ON", data=obj, proxies={
                "http": "https://"+proxyStr,
                "https": "https://"+proxyStr
    })
    response.encoding = response.apparent_encoding
    html = response.text
    print(html)

    response = session.post(f"{choice['origin']}/test/bbs.cgi?guid=ON", data=obj, proxies={
                "http": "https://"+proxyStr,
                "https": "https://"+proxyStr
    })
    response.encoding = response.apparent_encoding
    html = response.text
    print(html)

    
    tree = lxml.html.fromstring(html)
    errorStr = tree.xpath('//body/div')
    
    if len(errorStr):
        errorStr = tree.xpath('//body/div/text()')[0]
        # errorStr = etree.tostring(errorStr[0], method='html', encoding="shiftjis").decode('shiftjis')
        if len(errorStr.split()) >= 3 and errorStr.split()[3].isnumeric():
            wait = int(errorStr.split()[3])
            print('waiting for '+ str(wait)) 
            time.sleep(wait)

def worker ():
    while True:
        proxyStr = getProxy()
        for i in range(3):
            try:
                main(proxyStr)
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print(e)
            time.sleep(1)

fetchPosts()
print(l)
for i in range(100):
    t = threading.Thread(target=worker)
    t.start()
    print ("worker" + str(i) + "has started")
