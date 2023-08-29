import time
from config import *


def sakura_(url):
    """
    本来想写通用列表页链接获取的 但是wordpress每个站点格式都会改放弃了
    :param url: 列表链接
    :return: 组合成字典数据
    """
    try:
        html = get_response(url)  # 获取列表数据
        list_url = html.xpath("//article")  # 获取文章链接列表
        result = {}
        for i in list_url:
            if i.xpath('.//a[1]/@href'):
                link = i.xpath('.//a[1]/@href')[0]
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
    div = html.xpath('//article//div')
    content = ''
    for i in div:
        # 用来判断content标签 每个模板不一样所以这样写
        i = i.xpath('@class')
        if i and 'content' in i[0]:
            content = html.xpath(f'//div[@class="{i[0]}"]')[0]
            break
    title = html.xpath('//title/text()')[0]
    return title, content


if __name__ == '__main__':
    url_list = 'https://2heng.xin/archives/hacking/'
    # url1 = 'https://2heng.xin/archives/hacking/'
    url = 'https://my.minecraft.kim/tech/785/%e8%ae%ba%e5%a6%82%e4%bd%95%e4%bc%98%e9%9b%85%e7%9a%84%e5%b0%86%e8%87%aa%e5%b7%b1%e7%9a%84%e6%9c%8d%e5%8a%a1%e6%8e%a5%e5%85%a5%e5%ad%a6%e6%a0%a1%e7%9a%84-cas-%e7%bb%9f%e4%b8%80%e8%ae%a4%e8%af%81/'
    html = get_response(url)  # 获取列表数据
    # sakura_(url_list)
    analysis_(html)
    # content = etree.tostring(content, encoding='utf-8').decode()
    # print(title)
    # print(content)
