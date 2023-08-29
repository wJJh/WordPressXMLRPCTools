import time
from config import *
import html2text

def tab(url):
    """
    本来想写通用列表页链接获取的 但是wordpress每个站点格式都会改放弃了
    :param url: 列表链接
    :return: 组合成字典数据
    """
    try:
        html = get_response(url)  # 获取列表数据
        list_url = html.xpath("//ul[@id='catlist']/li")  # 获取文章链接列表
        result = {}
        for i in list_url:
            if i.xpath('.//a/@href'):
                link = i.xpath('.//a/@href')[0]
                html = get_response(link)  # 获取列表数据
                title, content = analysis_(html)
                result[link] = [title,content]
                time.sleep(1)
        return result
    except Exception as e:
        print(f'{url},Sakura解析失败请检查{e}')


def analysis_(html):
    """
    详情页解析获取数据 这部分倒是通用的 若有错误可以提去Gitee提
    :param html:
    :return:文章标题，正文对象
    """
    content = html.xpath(f'//div[@id="Article"]/div[@class="content"]')[0]
    title = html.xpath('//div[@id="Article"]/h1[1]/text()')[0]
    return title, content


if __name__ == '__main__':
    url_list = 'https://www.pythontab.com/html/pythonhexinbiancheng/'
    # url1 = 'https://2heng.xin/archives/hacking/'
    url = 'https://www.pythontab.com/html/2019/pythonweb_0506/1430.html'
    # # html = get_response(url)  # 获取列表数据
    # a = tab(url_list)
    # print(a)
    html = get_response(url)  # 获取列表数据
    title, content = analysis_(html)
    content = etree.tostring(content, encoding='utf-8', method="html").decode()
    print(html2text.html2text(content))