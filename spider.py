import urllib.request
import re
import urllib
from collections import deque

# url = "http://www.baidu.com"
# a=urllib.request.urlopen(url)
# 打印response的信息
# print(type(a))
# print(a.geturl())
# print(a.info())
# print(a.getcode())
# data = a.read()
# data = data.decode('UTF-8')
# print(data)

# 存放要访问的队列
queue = deque()
# 存放已经访问过的，set中重复的会自动合并可以通过x in visited查询是否查过
visited = set()

url = 'http://news.sina.com.cn/'  # 入口页面, 可以换成别的
# url = 'http://vip.book.sina.com.cn/weibobook/sina_reader.php?bid=5388658'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()  # 队首元素出队
    visited |= {url}  # 标记为已访问

    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1
    # 会抛出的异常HTTP Error 403: Forbidden：之所以出现上面的异常,是因为如果用 urllib.request.urlopen 方式打开一个URL,
    # 服务器端只会收到一个单纯的对于该页面访问的请求,但是服务器并不知道发送这个请求使用的浏览器,操作系统,硬件平台等信息,
    # 而缺失这些信息的请求往往都是非正常的访问,例如爬虫.
    # 有些网站为了防止这种非正常的访问,会验证请求信息中的UserAgent(它的信息包括硬件平台、系统软件、应用软件和用户个人偏好),
    # 如果UserAgent存在异常或者是不存在,那么这次请求将会被拒绝(如上错误信息所示)
    # 所以可以尝试在请求中加入UserAgent的信息

    # 主要是由于该网站禁止爬虫导致的，可以在请求加上头信息，伪装成浏览器访问User - Agent
    # 在浏览器的地址栏使用js获取userAgent：javascript:alert(navigator.userAgent)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)

    # urllib.error.URLError: <urlopen error [WinError 10060] 无法连接，但是直接点击可以打开并且直接访问可以连接，第364

    # 1.可能是网络访问策略限制：使用proxyHandler代理
    # proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}# The proxy address and port:
    # proxy_support = urllib.request.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})# We create a handler for the proxy
    # opener = urllib.request.build_opener(proxy_support)# We create an opener which uses this handler:
    # urllib.request.install_opener(opener)# Then we install this opener as the default opener for urllib2:


    #2. 可能是网络不稳定的问题：可以尝试多次链接,for tries in range(10)

    # 3.添加超时跳过功能(最终选择)
    # 运行后发现, 当发生超时, 程序因为exception中断.于是我把这一句也放在try.. except 结构里, 问题解决
    try:
        urlOp = urllib.request.urlopen(req ,timeout=2)
    except:
        continue

    # 检测抓取到的文件类型，确认是html再继续分析：可能会存在ico或jpg的连接，这样在将bytes进行decode('UTF-8')解码的时候会抛出异常
    if 'html' not in urlOp.getheader('Content-Type'):
        continue

    # 避免程序异常中止, 用try..catch处理异常
    try:
        data = urlOp.read().decode('utf-8')
    except:
        continue

    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
    linkRe = re.compile('href=\"(.+?)\"')
    for x in linkRe.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('加入队列 --->  ' + x)