import urllib.request
for url in ('http://localhost:5173/','http://[::1]:5173/'):
    try:
        print('GET', url)
        print(urllib.request.urlopen(url, timeout=5).read()[:200])
    except Exception as e:
        print('ERROR', url, e)
