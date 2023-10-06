
import time
import json
import requests
import hashlib
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import unhexlify
import base64

def base64_api(b64_img):
    #  typeid your_typeid
    data = {"username": 'your_username', "password": 'your_pwd', "typeid": 3, "image": b64_img}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""

def generate_random_string():
    chars = string.ascii_letters + string.digits
    random_chars = random.sample(chars, 5)
    result = ''.join(random_chars)
    return result

def convert_js_to_py(t):
    keys_sorted = sorted(t.keys())
    result = ''
    for key in keys_sorted:
        value = t[key]
        if isinstance(value, dict):
            json_str = json.dumps(value, ensure_ascii=False, default=str).replace('/', '\/')
        else:
            json_str = str(value)
        result += key + json_str
    return result

def generate_signature(data=None, headers=None, prefix="a75846eb4ac490420ac63db46d2a03bf"):
    signature = prefix
    if data:
        signature += convert_js_to_py(data)
    if headers:
        signature += convert_js_to_py(headers)
    signature += prefix
    return hashlib.md5(signature.encode('utf-8')).hexdigest()

def encrypt(data, key=b'fX@VyCQVvpdj8RCa', iv_hex="00000000000000000000000000000000"):
    iv_bytes = unhexlify(iv_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv_bytes)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_base64 = base64.b64encode(encrypted_data).decode()
    return encrypted_base64

# Initialize headers and data
Timestemp = str(int(time.time()))[:10]
random_string = generate_random_string()
headers = {
    "App-Ver": "",
    "Os-Ver": "",
    "Device-Ver": "",
    "Imei": "",
    "Access-Token": "",
    "Timestemp": Timestemp,
    "NonceStr": f"{Timestemp}{random_string}",
    "App-Id": "4ac490420ac63db4",
    "Device-Os": "web"
}

captcha_signature = generate_signature(headers=headers)

# Encrypt signatures

encrypted_captcha_signature = encrypt(captcha_signature)
# Update headers
headers['Signature'] = encrypted_captcha_signature

# Make requests
url_captcha = "https://www.epwk.com/api/epwk/v1/captcha/show"
params_captcha = {
    "channel": "common_channel",
    "base64": "1"
}
response_captcha = requests.get(url_captcha, headers=headers, params=params_captcha)
b64_img = response_captcha.json()['data']['base64']
img_str = base64_api(b64_img)
print(img_str)


data = {
    "username": "your_web_username",
    "password": "your_web_pwd",
    "code": img_str,
    "hdn_refer": "https://shimo.im/"
}

del headers['Signature']


# Generate signatures
login_signature = generate_signature(data=data, headers=headers)

encrypted_login_signature = encrypt(login_signature)
# Update headers
headers['Signature'] = encrypted_login_signature


url_login = "https://www.epwk.com/api/epwk/v1/user/login"
response_login = requests.post(url_login, headers=headers, data=data)

print("Login Response:", response_login.text)
