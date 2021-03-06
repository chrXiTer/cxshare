#coding: utf-8
import urllib
import requests
import shutil
import gzip, io


def check_gzip(response, html):
    """ 检查是否经过gzip压缩，并解压后返回 """
    if response.info().get('Content-Encoding') == 'gzip':
        buf = io.StringIO(html)
        fd = gzip.GzipFile(fileobj=buf)
        html = fd.read()
    return html


def open_url(url, timeout=60):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive'
    }
    request = urllib.request.Request(url,headers=header)
    request.add_header('Accept-encoding', 'gzip')
    request.get_method = lambda: 'GET'
    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    response = opener.open(request, timeout=timeout)
    if response.code == 200:
        html = response.read()
        html = check_gzip(response, html)
        return html


def post_url(url, data):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    }
    request = urllib.request.Request(url,headers=header)
    data = urllib.parse.urlencode(data)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()) 
    response = opener.open(request, data)
    return response.read()


def download_file(url, filename):
    try:
        req = requests.get(url, stream = True, timeout = 3)
    except:
        return False
    if req.status_code == 200:
        with open(filename, "wb") as fd:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, fd)
            return True
    return False


def url2filename(url):
    parse = urllib.parse.urlparse(url)
    path = parse.path.strip("/")
    return path.replace("/", " ")


def full_url(url, src):
    src_parse = urllib.parse.urlparse(src)
    if not src_parse.netloc and not src_parse.scheme:
        if not src.startswith("/"):
            end_index = url.rfind("/")
            url = url[:end_index]
            src = u"{0}/{1}".format(url, src)
        else:
            url = urllib.parse.urlparse(url)
            src = u"{0}://{1}{2}".format(url.scheme, url.netloc, src)
    elif not src_parse.scheme:
        url = urllib.parse.urlparse(url)
        src = u"{0}:{1}".format(url.scheme, src)
    return src
 

