import requests

url = "http://192.168.68.107:81/stream"
response = requests.get(url, stream=True, timeout=5)

print("Status:", response.status_code)
print("Headers:", response.headers)