# 项目标题

这个项目是一个用于模拟登录[某网站](https://www.epwk.com)的Python脚本。它包括获取和解析验证码，生成签名，加密签名和发送HTTP请求等步骤。

## 依赖

- Python 3
- `requests`
- `Crypto` (pycryptodome)
- `hashlib`
- `json`
- `base64`
- `time`
- `random`
- `string`
- `binascii`

## 使用方法

1. 安装依赖:

```bash
pip install requests pycryptodome
```

2. 克隆此仓库或直接下载项目代码。

3. 打开 `main.py` (假设你的脚本文件名为 `main.py`), 并在 `base64_api` 函数中填写你的用户名和密码。

4. 运行脚本:

```bash
python main.py
```

## 代码解析

### 导入必要的库

```python
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
```

### 定义辅助函数

- `base64_api(b64_img)`：向在线OCR服务发送base64编码的图像以获取图像中的文本。
- `generate_random_string()`：生成一个由大小写字母和数字组成的随机字符串。
- `convert_js_to_py(t)`：将JavaScript对象转换为Python字符串。
- `generate_signature(data=None, headers=None, prefix="a75846eb4ac490420ac63db46d2a03bf")`：生成请求的签名。
- `encrypt(data, key=b'fX@VyCQVvpdj8RCa', iv_hex="00000000000000000000000000000000")`：使用AES CBC模式加密数据。

### 主逻辑

1. 初始化请求头和时间戳。
2. 生成并加密验证码请求的签名。
3. 发送验证码请求并解析验证码。
4. 删除签名字段，并为登录请求生成和加密新的签名。
5. 发送登录请求并打印响应。

## 注意

- 该脚本可能仅适用于特定版本的目标网站，如果目标网站的实现有所变化，该脚本可能需要更新。
- 请确保在符合目标网站的使用条款和条件的情况下使用此脚本。不要用于非法或不道德的目的。

## 贡献

如果你发现了bug或有任何改进的建议，请通过GitHub的问题跟踪器提交问题或发送拉取请求。

## 许可

该项目根据MIT许可证获得许可，详情请参见`LICENSE`文件。

---

这个README文档为你的项目提供了一个基本的框架，你可以根据项目的具体情况和需求进行修改和补充。