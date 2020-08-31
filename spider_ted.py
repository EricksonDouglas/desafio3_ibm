from requests import get as req_get
from lxml import html
import json
from re import sub as re_sub
from re import findall as re_find


def ted(url: str) -> str:
    print("Extrair dados no TED.com")
    _req = req_get(url=url).text
    _title, _author = html.fromstring(_req).xpath('//meta[@itemprop="name"]/@content')
    _body = "".join(list(map(lambda x: re_sub(r"\t", " ", re_sub(r"\n|\t{2}", "", x)).strip(),
                             html.fromstring(_req).xpath('//div[contains(@class, "Grid__cell")]/p/text()'))))
    with open(f'articles/{url.split("/")[4]}.json', "w") as _file:
        _file.write(json.dumps({"author": _author, "body": _body, "title": _title, "type": "video", "url": url}))
    return url.split("/")[4]


def olhardigital(url: str) -> str:
    print("Extrair dados no olhardigital.com.br")
    _json = json.loads(re_sub(r"\n|\t|\r", '', html.fromstring(req_get(url=url).text
                                                          ).xpath('string(//script[@type="application/ld+json"])')))
    _url = (url.split("/")[6] if url.split("/")[3] == "colunistas" else
            url.split("/")[4] if url.split("/")[3] == "noticia" else url.split("/")[5])
    with open(f'articles/{_url}.json', "w") as _file:
        _file.write(json.dumps({"author": _json['author']['name'], "body": _json['articleBody'],
                                "title": _json['headline'], "type": _json['@type'], "url": url}))
    return _url


def startse(url: str) -> str:
    print("Extrair dados no startse.com")
    _req = req_get(url=url).text
    _json = json.loads(re_sub(r"\n|\t|\r", '',
                              html.fromstring(_req).xpath('string(//script[@type="application/ld+json"])')))
    _body = "".join(list(map(lambda x: re_sub(r"\t", " ", re_sub(r"\n|\t{2}", "", x)).strip(),
                             html.fromstring(_req).xpath('//span[@style="font-weight: 400;"]/text()'))))
    with open(f'articles/{url.split("/")[-1]}.json', "w") as _file:
        _file.write(json.dumps({"author": _json['@graph'][5]['name'], "body": _body,
                                "title": _json['@graph'][4]['headline'], "type": _json['@graph'][4]['@type'],
                                "url": url}))
    return url.split("/")[-1]


if __name__ == '__main__':
    with open("links.json", "r") as _file:
        print("A lista salva na pasta articles")
        print(list(map(lambda url:
                       ted(url) if url.startswith("https://www.ted") else
                       olhardigital(url) if url.startswith("https://olhardigital") else
                       startse(url) if url.startswith("https://www.startse") else None,
                       json.load(_file)['urls'])))