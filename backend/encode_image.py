import base64

path = r"c:\Users\HP\Desktop\ksum\backend\page0.png"
with open(path, "rb") as f:
    data = f.read()
print(base64.b64encode(data).decode('ascii'))
