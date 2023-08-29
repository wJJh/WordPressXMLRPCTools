import json
import os
import hashlib
import frontmatter
import requests
from lxml import etree
import re

config_file_txt = ""
if os.path.abspath('diy_config.txt'):
    config_file_txt = os.path.abspath('diy_config.txt')
else:
    config_file_txt = os.path.abspath('config.txt')

# wordpress有发文权限帐号与密码 与 xmlrpc接口
username = 'xxxxxxx'
password = 'xxxxxxx'
xmlrpc_php = 'http://xxxxxxx/xmlrpc.php'

# 分类标签 多标签写法  - 转载\n- PYTHON\n- XXX
TAG = '- 转载'

# 计算sha1
def get_sha1(filename,file=1):
    """
    file为使用路径读取计算sha1 默认使用 0为禁用
    """
    if file:
        with open(filename, 'rb') as f:
            return hashlib.sha1(f.read()).hexdigest()
    result = hashlib.sha1(filename.encode()).hexdigest()
    return result


# 获取md_sha1_dic
def get_md_sha1_dic(file):
    result = {}
    if os.path.exists(file):
        with open(file, 'r') as f:
            result = json.loads(f.read())
    else:
        with open(file, 'w') as f:
            f.write(json.dumps({}))
    return result


# 获取markdown文件中的内容
def read_md(file_path):
    try:
        content = ""
        metadata = {}
        with open(file_path) as f:
            post = frontmatter.load(f)
            content = post.content
            metadata = post.metadata
            # print("==>>", post.content)
            # print("===>>", post.metadata)
        return content, metadata
    except Exception as e:
        print(e,file_path)
        return "", {}


#  将字典写入文件
def write_dic_info_to_file(dic_info, file):
    with open(file, 'w') as f:
        f.write(json.dumps(dic_info))
    return True


# 将文件读取为字典格式
def read_dic_from_file(file):
    with open(file, 'r') as f:
        dic = f.write(json.loads(f.read()))
    return dic


def get_response(url):
    """
    请求链接再HTML化给下一级解析
    :return: etree化HTML数据
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    return html

if __name__ == '__main__':
    a = "/data/project/WordPressXMLRPCTools/_posts/Forge 开发经验 —— 创造一个通过消耗耐久值进行合成的物品 - HikariLan's Blog.md"
    b = "/data/project/WordPressXMLRPCTools/_posts/2021-11-21-cs.md"
    read_md(b)