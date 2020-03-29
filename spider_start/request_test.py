import requests

# result = requests.get("http://www.baidu.com")
# print(result.text)

res = requests.get("http://www.taobao.com")
print(res.status_code)
print(res.text)


