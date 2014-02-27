import urllib.request, re, json
from flask import Flask

app = Flask(__name__)



def json_list(list):
    lst = []
    for pn in list:
        d = {}
        d['URL']=pn
        lst.append(d)
    return json.dumps(lst, sort_keys=True, indent=4, separators=(',', ': '))

class HTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newreq = urllib.request.HTTPRedirectHandler.redirect_request(self,
            req, fp, code, msg, headers, newurl)
        if newreq is not None:
            self.redirections.append(newreq.get_full_url())
        return newreq

def getRedirections(url):
    h = HTTPRedirectHandler()
    h.max_redirections = 100
    h.redirections = [url]
    opener = urllib.request.build_opener(h)
    response = opener.open(url)
    derniereValeur = len(h.redirections)-1;
    try:
        getXtloc = urllib.parse.parse_qs(h.redirections[derniereValeur])["xtloc"][0]
        h.redirections.append(getXtloc);
    except Exception as e:
        pass
    jsonRedirections = json_list(h.redirections)
    return jsonRedirections


@app.route('/')
def hello_world():
    return getRedirections("http://content.enews-airfrance.com/emessageIRS/servlet/IRSL?v=5&a=10103&r=12114&m=5108&l=1&p=t4F60AE5C76416EF4F48A0961D54FD79ED9DFD33E738149D0BF19B9D69C7E051E0484431514122B31511AB9BDFBFB2571C713EA946FEEB7E174FE4A731716F7FDDE98266D03EC03AEE66A82BF226EF3EB081877DB7D0D3ADBDD5EFF8B1585AD7E23741D404C7D318242246A2AF922E6443086A3429D399F8A87D5352E4C68F0546C4E331BF430A37A9DA09F56F5FACD58E4755D02CAC281100EF96A31D64F01B790F480811275B9614D40661352952AE532ADF72F42A1ECE279666CB5887289054C1B94A13829A4B0078CA25F4270220CD8A31AC0349757FABB31D79F6F87AD85374D88D09C2C73EB&e=4&x=2456709.0").replace("\r","").replace("\n", "<br>").replace(" ",  "&nbsp;")


if __name__ == '__main__':
    app.run()



