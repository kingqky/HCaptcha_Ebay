from environs import Env

env = Env()
env.read_env()

CAPTCHA_RESOLVER_API_URL = 'https://api.yescaptcha.com/createTask'
CAPTCHA_RESOLVER_API_KEY = env.str("CAPTCHA_RESOLVER_API_KEY")

CAPTCHA_DEMO_URL = 'https://www.ebay.com/splashui/captcha?shield=false&appName=sgninui&ru=https%3A%2F%2Fwww.ebay.com%2Fsignin%3FpageType%3D2510217%26ru%3Dhttps%253A%252F%252Fcart.ebay.com%252Fsc%252Fview'

CAPTCHA_ENTIRE_IMAGE_FILE_PATH = 'captcha_entire_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH = 'captcha_single_image_%s.png'
CAPTCHA_RESIZED_IMAGE_FILE_PATH = 'captcha_resized_image.png'
