import urllib.request

print('GET http://127.0.0.1:8000/health')
print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())
print('\nGET http://127.0.0.1:5173/')
print(urllib.request.urlopen('http://127.0.0.1:5173/').read().decode()[:200])
