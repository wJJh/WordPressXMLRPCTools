import html2text
import time
from config import *
from url_analysis.Sakura import sakura_
from url_analysis.Python_Tab import tab


def run_spider(dict_url):
    """
    value[0]是xpath 网站函数内使用 value[1]是网站标签 自己创建
    :param dict_url: 链接字典
    :return:
    """
    result_dict = {
        'Sakura': sakura_,
        'Tab': tab,
        '标签': '函数'
    }  # TODO (网站模板加入) 新网站写好将标签和对应函数放这里就行
    for url, value in dict_url.items():
        if value not in result_dict.keys():
            continue
        result = result_dict[value](url)
        for link, title_content in result.items():
            try:
                title_content[0] = title_content[0].replace(":", "").replace("：", "")
                content = md_save(title_content, link)
                # 去重 使用获取到的标题和正文的sha1 与 本地相同标题和正文的sha1比较
                # 缺点是作者改了标题之后就会重新生成文章
                # 使用了原作者的去重逻辑(懒的重写
                local_data = get_md_sha1_dic(os.path.abspath('.md_sha1'))  # 本地sha1 文件标题等数据
                server_sha1 = get_sha1(content, file=0)  # 获取到的正文sha1
                if title_content[0] in local_data.keys() and server_sha1 == local_data[title_content[0]]["hash_value"]:
                    break
                # 保存md到本地
                load_name = f'./_posts/[转载]{title_content[0]}.md'
                with open(load_name, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'{load_name}创建成功')
                time.sleep(1)
            except Exception as e:
                print(f'{link}转换md出错{e}')


def md_save(title_content, link):
    """
    :param link: 原文链接
    :param title_content: [0]文章标题
    :param title_content: [1]正文xpath格式
    :return: md的内容
    """
    title = f"""---
title: {title_content[0]}
link: {link}
categories:
{TAG}
---
"""  # TODO 文章标题与分类 可以自定义
    content = etree.tostring(title_content[1], encoding='utf-8', method="html").decode()
    markdown = html2text.html2text(content)
    data = title + markdown
    return data


if __name__ == '__main__':
    # with open(os.path.abspath('URL.json'), 'r') as f:
    #     result = json.loads(f.read())
    # print(f'本地转载链接:{result}')
    result = {
        "https://www.nosum.cn/category/1": "Sakura1",
        "https://www.pythontab.com/html/pythonhexinbiancheng/": "Tab",
        "https://www.pythontab.com/html/pythonjichu/": "Tab"
    }
    run_spider(result)
    # for i in range(2,11):
    #     result = {
    #         "https://www.nosum.cn/category/1": "Sakura1",
    #         f"https://www.pythontab.com/html/pythonhexinbiancheng/{i}.html": "Tab",
    #         f"https://www.pythontab.com/html/pythonjichu/{i}.html": "Tab"
    #     }
    #     run_spider(result)
