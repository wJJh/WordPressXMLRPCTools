from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from urllib.parse import urlparse
import time

import markdown
import re
import urllib.parse
from config import *


# 获取已发布文章id列表
def get_posts():
    print(time.strftime('%Y-%m-%d-%H-%M-%S') + "开始从服务器获取文章列表...")
    posts = wp.call(GetPosts({'post_type': 'post', 'number': 1000000000}))
    post_link_id_list = []
    title_list = []
    for post in posts:
        post_link_id_list.append({
            "id": post.id,
            "link": post.link
        })
        title_list.append(post.title)
    print(f'网站文章有{len(post_link_id_list)}篇')
    return post_link_id_list,title_list


# 创建post对象
def create_post_obj(title, content, link, post_status, terms_names_post_tag, terms_names_category):
    post_obj = WordPressPost()
    post_obj.title = title
    post_obj.content = content
    # post_obj.link = link
    post_obj.post_status = post_status
    post_obj.comment_status = "open"
    # print(f'post对象链接创建成功{post_obj.link}')
    print("创建post对象")
    post_obj.terms_names = {
        # 文章所属标签，没有则自动创建
        'post_tag': terms_names_post_tag,
        # 文章所属分类，没有则自动创建
        'category': terms_names_category
    }

    return post_obj


# 新建文章
def new_post(title, content, link, post_status, terms_names_post_tag, terms_names_category):
    post_obj = create_post_obj(
        title=link,
        content=content,
        link=link,
        post_status=post_status,
        terms_names_post_tag=terms_names_post_tag,
        terms_names_category=terms_names_category)
    # 先获取id
    id = wp.call(NewPost(post_obj))
    # 再通过EditPost更新信息
    edit_post(id, title,
              content,
              link,
              post_status,
              terms_names_post_tag,
              terms_names_category)


# 更新文章
def edit_post(id, title, content, link, post_status, terms_names_post_tag, terms_names_category):
    post_obj = create_post_obj(
        title,
        content,
        link,
        post_status,
        terms_names_post_tag,
        terms_names_category)
    res = wp.call(EditPost(id, post_obj))
    print(f'文章更新:{res}')


# 获取特定目录的markdown文件列表
def get_md_list(dir_path):
    md_list = []
    dirs = os.listdir(dir_path)
    for i in dirs:
        if ".md" in i:
            md_list.append(os.path.join(dir_path, i))
    print(f"本地md文件列表:{md_list}")
    return md_list


# 重建md_sha1_dic,将结果写入.md_sha1
def rebuild_md_sha1_dic(file, md_dir):
    md_sha1_dic = {}

    global md_list

    for md in md_list:
        key = os.path.basename(md).split(".")[0]
        value = get_sha1(md)
        md_sha1_dic[key] = {
            "hash_value": value,
            "file_name": key,
            "encode_file_name": urllib.parse.quote(key, safe='').lower()
        }

    md_sha1_dic["update_time"] = time.strftime('%Y-%m-%d-%H-%M-%S')
    write_dic_info_to_file(md_sha1_dic, file)


def post_link_id_list_2_link_id_dic(post_link_id_list):
    link_id_dic = {}
    for post in post_link_id_list:
        link_id_dic[post["link"]] = post["id"]
    return link_id_dic


def href_info(link):
    return f"<br/><br/><br/>\n\n\n\n### [原文地址]({link})"


# 在README.md中插入信息文章索引信息，更容易获取google的收录
def insert_index_info_in_readme():
    """
    这里自己要修改索引地址
    :return:
    """
    # 获取_posts下所有markdown文件
    global md_list
    # 生成插入列表
    insert_info = ""
    md_list.sort(reverse=True)
    # 读取md_list中的文件标题
    for md in md_list:
        (content, metadata) = read_md(md)
        title = metadata.get("title", "")
        insert_info = insert_info + "[" + title + "](" + "https://" + domain_name + "/p/" + \
                      os.path.basename(md).split(".")[0] + "/" + ")\n\n"
    # 替换 ---start--- 到 ---end--- 之间的内容

    insert_info = "---start---\n## 目录(" + time.strftime('%Y年%m月%d日') + "更新)" + "\n" + insert_info + "---end---"
    print("==插入信息==>>", insert_info)
    return True

def md_sh1_repeat():
    # 用来重新创建sha1 根据标题对比
    # 在某次测试中不小心把所有md写进sha1 那时候关闭了md上传。。
    post_link_id_list,title_list = get_posts()
    link_id_dic = post_link_id_list_2_link_id_dic(post_link_id_list)
    print(f"网站文章列表:{link_id_dic}")
    md_sha1_dic = get_md_sha1_dic(os.path.abspath('.md_sha1'))
    for md in md_list:
        # 计算md文件的sha1值，并与md_sha1_dic做对比
        sha1_key = os.path.basename(md).split(".")[0]
        # 用来重新创建sha1 根据标题对比
        if sha1_key in title_list:
            key = os.path.basename(md).split(".")[0]
            value = get_sha1(md)
            md_sha1_dic[key] = {
                "hash_value": value,
                "file_name": key,
                "encode_file_name": urllib.parse.quote(key, safe='').lower()
            }
    md_sha1_dic["update_time"] = time.strftime('%Y-%m-%d-%H-%M-%S')
    write_dic_info_to_file(md_sha1_dic, os.path.join(os.getcwd(), ".md_sha1"))

def main():
    # 1. 获取网站数据库中已有的文章列表
    post_link_id_list,title_list = get_posts()
    link_id_dic = post_link_id_list_2_link_id_dic(post_link_id_list)
    print(f"网站文章列表:{link_id_dic}")
    # 2. 获取md_sha1_dic
    # 查看目录下是否存在md_sha1.txt,如果存在则读取内容；
    # 如果不存在则创建md_sha1.txt,内容初始化为{}，并读取其中的内容；
    # 将读取的字典内容变量名，设置为 md_sha1_dic
    md_sha1_dic = get_md_sha1_dic(os.path.abspath('.md_sha1'))

    # 3. 开始同步
    # 读取_posts目录中的md文件列表
    global md_list

    for md in md_list:
        # 计算md文件的sha1值，并与md_sha1_dic做对比
        sha1_key = os.path.basename(md).split(".")[0]
        sha1_value = get_sha1(md)
        # 如果sha1与md_sha1_dic中记录的相同，则打印：XX文件无需同步;
        if ((sha1_key in md_sha1_dic.keys()) and ("hash_value" in md_sha1_dic[sha1_key]) and (
                sha1_value == md_sha1_dic[sha1_key]["hash_value"])):
            print(md + "无需同步")
        # 如果sha1与md_sha1_dic中记录的不同，则开始同步
        else:
            # 读取md文件信息
            (content, metadata) = read_md(md)
            if not content and not metadata:
                continue
            # 获取title
            title = '[转载]' + metadata.get("title", "")  # 标题
            terms_names_post_tag = metadata.get("tags", domain_name)  # 标签
            terms_names_category = metadata.get("categories", domain_name)  # 分类
            url = metadata.get("link", domain_name)  # 正文链接
            post_status = "publish"
            link = urllib.parse.quote(sha1_key, safe='').lower()
            if '转载' in title:
                content = content + href_info(url)
            content = markdown.markdown(content,
                                        extensions=['tables', 'fenced_code'])
            # 如果文章无id,则直接新建
            if not (link in link_id_dic.keys()):
                new_post(title, content, link, post_status, terms_names_post_tag, terms_names_category)
                print("new_post==>>", {
                    "title": title,
                    # "content": content,
                    "link": link,
                    "post_status": post_status,
                    "terms_names_post_tag": terms_names_post_tag,
                    "terms_names_category": terms_names_category
                })
            # 如果文章有id, 则更新文章
            else:
                # 获取id
                id = link_id_dic["https://" + domain_name + "/p/" + link + "/"]
                edit_post(id, title, content, link, post_status, terms_names_post_tag, terms_names_category)

                print("edit_post==>>", {
                    "id": id,
                    "title": title,
                    # "content": content,
                    "link": link,
                    "post_status": post_status,
                    "terms_names_post_tag": terms_names_post_tag,
                    "terms_names_category": terms_names_category
                })
            time.sleep(2)

    # 4. 重建md_sha1_dic
    rebuild_md_sha1_dic(os.path.join(os.getcwd(), ".md_sha1"), os.path.join(os.getcwd(), "_posts"))
    # 5. 将链接信息写入insert_index_info_in_readme
    # 看自己喜好加吧 我没用自定义链接所以没启动
    # insert_index_info_in_readme()


if __name__ == '__main__':
    url_info = urlparse(xmlrpc_php)
    domain_name = url_info.netloc
    # wp初始化
    wp = Client(xmlrpc_php, username, password)
    # 本地md文件列表
    md_list = get_md_list(os.path.abspath("_posts"))
    main()