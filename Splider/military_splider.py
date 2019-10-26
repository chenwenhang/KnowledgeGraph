from requests_html import HTMLSession
import csv

# from fake_useragent import UserAgent

session = HTMLSession()
root_url = 'http://weapon.huanqiu.com/weaponlist/explosive'
path = "data/explosive.csv"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


# 获取所有页面地址
def get_url():
    # 获取根目录内容
    res = session.get(root_url)
    pages = res.html.find('.pages')
    # 获取最大页数
    max_page = int((res.html.find('#hq_team_libs_page_btn'))[0].attrs.get("data-maxpage"))
    # 生成链接公共前缀
    first_link = list(pages[0].absolute_links)[0]
    string = first_link.split('/')
    suffix = ""
    for i in range(len(string) - 1):
        suffix = suffix + string[i] + "/"
    suffix = suffix + "list_0_0_0_0_"
    # 获取所有页面链接
    links = []
    for i in range(1, max_page + 1):
        links.append(suffix + str(i))
    item_links = set()
    for url in links:
        res = session.get(url)
        item_list = res.html.find('.picList ul')
        # 获取当前页面上的所有item的链接，加入到item集合
        item_links = item_links | item_list[0].absolute_links
    return item_links


# 获取item详细信息
def get_item():
    links = get_url()
    # links = ['http://weapon.huanqiu.com/ahl', 'http://weapon.huanqiu.com/39_ab','http://weapon.huanqiu.com/fc_1']
    # 存储属性名，用于后续有序处理item_list
    attr_name_list = ['国家']
    # 存储item信息
    item_list = []
    for link in links:
        print(link)
        item = {}
        res = session.get(link)
        # 获取国家
        if not res.html.find('.country b'):
            continue
        country = (res.html.find('.country b'))[0].text
        item['国家'] = country
        # 获取其他信息
        if not res.html.find('.dataInfo'):
            continue
        content_list = (res.html.find('.dataInfo'))[0].text.splitlines()
        # 标记不规则属性名，为空代表当前为规则属性无需特殊处理
        index = ""
        for content_i in content_list:
            content_i_list = content_i.split("：")
            # 如果是正常的“属性：值”的形式
            if len(content_i_list) == 2:
                index = ""
                # 如果属性列表中没有该属性，则添加
                if content_i_list[0] not in attr_name_list:
                    attr_name_list.append(content_i_list[0])
                item[content_i_list[0]] = content_i_list[1]
            # 如果是不规则的形式
            elif len(content_i_list) == 1:
                # 如果上一次是正常的，则为属性名
                if index == "":
                    # 如果属性列表中没有该属性，则添加
                    if content_i_list[0] not in attr_name_list:
                        attr_name_list.append(content_i_list[0])
                    index = content_i_list[0]
                    item[index] = ""
                # 否则为属性值
                else:
                    item[index] = item[index] + content_i_list[0]
        item_list.append(item)

    # print(attr_name_list)
    # for i in item_list:
    #     print(i)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv_write = csv.writer(f)
        csv_head = attr_name_list
        csv_write.writerow(csv_head)
        for item in item_list:
            row = []
            for attr_name in attr_name_list:
                if attr_name not in item.keys():
                    row.append("")
                else:
                    row.append(item[attr_name])
            csv_write.writerow(row)


if __name__ == '__main__':
    print("开始处理")
    get_item()
    print("处理结束")
