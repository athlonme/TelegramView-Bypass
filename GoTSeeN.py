import requests, re
#Work in Python 2.7 - Work with socks4 proxies
# pip install requests
# pip install requests[socks]

def SeenStartFunction(postLink, proxyz):
    link = '{}{}'.format(postLink, '?embed=1')
    sess = requests.session()
    agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; Xbox)'
    proxy = {
        'http': 'socks4://{}'.format(proxyz),    # Remove socks4 if you don't want use Socks!
        'https': 'socks4://{}'.format(proxyz),
    }

    postData = {
        '_rl': 1
    }

    MyHeader = {
        'Host': 't.me',
        'User-Agent': agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': postLink,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        RequestStepOne = sess.get(link, proxies=proxy, headers=MyHeader, timeout=5)
        Data = re.findall('data-view="(.*)"', RequestStepOne.text.encode('utf8'))[0].split('" data-view="')[0]

        MyHeader2 = {
            'Host': 't.me',
            'User-Agent': agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': link,
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': str(RequestStepOne.headers.get('Set-Cookie'))

        }
        try:
            sess.post(link, proxies=proxy, headers=MyHeader2, data=postData, timeout=5)

            MyHeader3 = {
                'Host': 't.me',
                'User-Agent': agent,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': link,
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Cookie': str(RequestStepOne.headers.get('Set-Cookie'))

            }
            try:
                SeenRequest = sess.get('https://t.me/v/?views={}'.format(Data), proxies=proxy, headers=MyHeader3, timeout=5)

                if SeenRequest.text == 'true':
                    print(' {} --> Seen Done!'.format(proxyz))
                else:
                    print(' {} --> Not Seen'.format(proxyz))
            except:
                print(' {} --> error In Send Request in Step tree!'.format(proxyz))
        except:
            print(' {} --> error In Send Request in Step two!'.format(proxyz))
    except:
        print(' {} --> error In Send Request!'.format(proxyz))

if __name__ == '__main__':
    import sys, threading, time
    try:
        proxylist = open(sys.argv[1], 'rb').read().splitlines()
        url = sys.argv[2]
    except:
        print(' Python {} ProxyList.txt https://t.me/PostLink'.format(sys.argv[0]))
        sys.exit()
    thread = []
    for proxy in proxylist:
        t = threading.Thread(target=SeenStartFunction, args=(url, proxy))
        t.start()
        thread.append(t)
        time.sleep(0.08)
    for j in thread:
        j.join()
