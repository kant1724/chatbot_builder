from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

def get_href_and_title_by_page(link):
    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(), "html.parser")    
    news = bsObj.findAll(attrs={"class" : "_sp_each_title"})
    ll = []
    for i in range(len(news)):
        ll.append({"title" : news[i]['title'], "url" : news[i]['href']})
    
    return ll

def get_href_and_rest_name_by_page(link):
    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(), "html.parser")  
    rest = str(bsObj.findAll("script"))
    var = "window.PLACE_STATE="
    r1 = rest.find(var);
    r2 = rest.find("</script>", r1)
    r = rest[r1 + len(var):r2]
    jsonObj = json.loads(r)
    a = jsonObj['businesses']
    b = a[a['lastKey']]['items']
    ll = []
    for bb in b :
        if bb is not None:
            detailUrl = 'https://store.naver.com/restaurants/detail?id=' + bb.get('id', '')
            l = {'detailUrl' : detailUrl, 'name' : bb.get('name', ''), 'routeUrl' : bb.get('routeUrl', ''), 'imageSrc' : bb.get('imageSrc', ''), 'phone' : bb.get('phone', ''), 'blogCafeReviewCount' : bb.get('blogCafeReviewCount', '0')}
            ll.append(l)
        
    return ll

def is_possible_crawling(link):
    try:
        urlopen(link)
    except:
        return False
    return True
