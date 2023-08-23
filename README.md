# HCaptcha_Ebay
针对于Ebay人机识别
HCaptcha 图像识别模拟点击Python selenium

## Usage

Clone this repo:

```
git clone https://github.com/Python3WebSpider/HCaptchaResolver.git
```

Then go to https://yescaptcha.com/i/CnZPBu and register your account, then get a `clientKey` from portal.

![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/02d26fe0-1e8a-47c0-b271-e1e08d96baa0)


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
![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/f43266aa-7864-4c2b-b76e-7eb5bfc487b7)

![image](https://github.com/kingqky/HCaptcha_Ebay/assets/99392534/a40c175e-a06f-4197-805f-4acb1d494615)

