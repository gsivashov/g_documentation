from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pathlib import Path
from argparse import ArgumentParser
import logging


def setSession(url):
    session = HTMLSession()
    response = session.get(url.strip())
    print(url.strip())
    return response


def get_content_from_request(response):
    xpaths = [
        '//section[@class="primary-container"]',
        '//devsite-content',
    ]
    for xpath in xpaths:
        content = response.html.xpath(xpath)
        if not content:
            continue
        return content[0].html


def getTextContent(response):

    h1 = ''.join(response.html.xpath('//h1/text()')
                 ).replace('?', '_').replace(':', '_')
    article = get_content_from_request(response)
    if not article:
        return h1, None

    soup = BeautifulSoup(article, features='lxml')

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.body.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return h1, text


def main(params):
    start_file = str(params.file)
    with open(start_file) as f:
        for link in f:
            url = setSession(link)
            h1, text = getTextContent(url)
            if not text:
                logging.info(
                    f'Error with {link.strip()}, no tags found'
                )
                continue
            filename = f'{h1.replace("/","").replace(" ","_")}.txt'
            with open(Path.cwd() / 'docs' / filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(f'{link}\n{text}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--file',
        type=str,
        help='file path',
        default='url_list.txt',
    )
    params = parser.parse_args()

    logging.basicConfig(
        filename=Path().cwd() / 'logs' / 'google_doc.log',
        filemode='a',
        level=logging.INFO,
        format='%(levelname)s:%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    main(params)
