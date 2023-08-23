# HCaptcha_Ebay
针对于Ebay人机识别
HCaptcha 图像识别模拟点击Python selenium

## Usage

Clone this repo:

```
git clone https://github.com/Python3WebSpider/HCaptchaResolver.git
```

Then go to https://yescaptcha.com/i/CnZPBu and register your account, then get a `clientKey` from portal.
![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/d7fa9819-4e7b-412f-887b-c3089e7481f2)

Then create a `.env` file in root of this repo, and write this content:

```
CAPTCHA_RESOLVER_API_KEY=<Your Client Key>
```
Next, you need to install packages:

```
pip3 install -r requirements.txt
```

At last, run demo:

```
python3 main.py
```

Result:
![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/8cc800ae-8292-45ec-9ad3-c6aaffff9c7d)
![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/b4431e16-b2af-4c62-becb-b0f8ad853621)