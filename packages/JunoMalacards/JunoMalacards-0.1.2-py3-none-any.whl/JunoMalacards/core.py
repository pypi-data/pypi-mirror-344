from get_url import extract_ncbi_links
from dow_html import dowload_html
from get_ip import get_ip


def getip(proxy_api):
    """
        获取代理ip
    :return: ["127.0.0.1","8080"]
    """
    return get_ip(proxy_api)


def dowhtml(filename, is_proxy=False, proxy_ip=None, proxy_port=None, proxy_api=None):
    """

       :param filename: 文件路径
       :param is_proxy: 第一次爬虫是否需要代理，如果为False，那么proxy_ip 和 proxy_port就必须填
       :param proxy_ip: 代理ip
       :param proxy_port: 代理端口
       :param proxy_api: 提取代理的API(http/https)
       :return:
       """
    dowload_html(filename, is_proxy=is_proxy, proxy_ip=proxy_ip, proxy_port=proxy_port, proxy_api=proxy_api)


def geturl(target_url, output_file):
    extract_ncbi_links(target_url, output_file=output_file)

def main():
    print("欢迎来到Juno爬虫小公举！")

if __name__ == "__main__":
    main()
    getip("https://api.jikip.com/ip-get?num=1&minute=1&format=json&area=all&protocol=1&mode=1&key=j03g8efum64l0j")