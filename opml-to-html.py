from bs4 import BeautifulSoup
from flask import Flask
from yattag import Doc
import requests

# List of ompl docs containing RSS feeds to turn into HTML
urls = ["https://gist.githubusercontent.com/benkehoe/2a846d3bb0044ca5d99073458280f36e/raw/980d9d780edafe63a34b9b9729ee430ed9ed3e78/aws.opml"] # noqa

app = Flask(__name__)


def xml_to_html(url, xml):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        text("Full list: ")
        with tag('a', href=url):
            text(xml.find("title").text)
        with tag('ul'):
            for feed in xml.find_all("outline"):
                if feed.get("xmlUrl"):
                    with tag('li'):
                        with tag('a', href=feed.get("xmlUrl")):
                            text(feed.get("title"))
    return(doc.getvalue())


@app.route('/')
def parse_lists():
    for url in urls:
        xml = BeautifulSoup(requests.get(url).text, 'xml')
        return(xml_to_html(url, xml))
