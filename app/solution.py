from random import random
import re
from typing import List, Union
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
from loguru import logger
from HCaptcha_Ebay.app.captcha_resolver import CaptchaResolver
from HCaptcha_Ebay.app.settings import CAPTCHA_SINGLE_IMAGE_FILE_PATH
from HCaptcha_Ebay.app.utils import resize_base64_image
from selenium.common.exceptions import NoSuchElementException

class Solution(object):
    def __init__(self, url):
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 10)
        self.captcha_resolver = CaptchaResolver()

    def __del__(self):
        time.sleep(10)
        self.browser.close()

    #定义几个工具方法，分别能够支持切换到入口对应的 iframe 和验证码本身对应的 iframe，代码如下：

    def get_captcha_entry_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_entry_iframe = self.browser.find_element(By.CSS_SELECTOR, '#s0-71-captcha-ui > iframe')
        return captcha_entry_iframe

    def switch_to_captcha_entry_iframe(self) -> None:
        captcha_entry_iframe: WebElement = self.get_captcha_entry_iframe()
        self.browser.switch_to.frame(captcha_entry_iframe)



    def get_captcha_content_iframe(self) -> WebElement:
        self.browser.switch_to.default_content()
        captcha_content_iframe=self.browser.find_element(By.XPATH,'/html/body/div[5]/div[1]/iframe')
        return captcha_content_iframe

    def switch_to_captcha_content_iframe(self) -> None:
        captcha_content_iframe: WebElement = self.get_captcha_content_iframe()
        self.browser.switch_to.frame(captcha_content_iframe)


    def get_captcha_element(self) -> WebElement:
        captcha_element: WebElement = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'body > div > div.challenge-container > div > div > div.task-grid')))
        return captcha_element


    def trigger_captcha(self) -> None:
        self.switch_to_captcha_entry_iframe()
        captcha_entry = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#anchor #checkbox')))
        captcha_entry.click()
        time.sleep(3)
        self.switch_to_captcha_content_iframe()
        captcha_element: WebElement = self.get_captcha_element()
        if captcha_element.is_displayed:
            logger.debug('trigged captcha successfully')






    def get_captcha_target_text(self) -> WebElement:
        captcha_target_name_element: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'body > div > div.challenge-container > div > div > div.challenge-header > div.challenge-prompt > div.prompt-padding > h2')))
        return captcha_target_name_element.text


    def get_verify_button(self) -> WebElement:
        verify_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'body > div > div.interface-challenge > div.button-submit.button')))
        return verify_button

    def is_element_present(self, locator):
        try:
            self.browser.find_element(*locator)
            return True
        except NoSuchElementException:
            return False


    def verify_captcha(self):
        # get target text
        self.captcha_target_text = self.get_captcha_target_text()
        logger.debug(
            f'captcha_target_text {self.captcha_target_text}'
        )
        # extract all images
        single_captcha_elements = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image .image-wrapper .image')))
        resized_single_captcha_base64_strings = []
        for i, single_captcha_element in enumerate(single_captcha_elements):
            single_captcha_element_style = single_captcha_element.get_attribute('style')
            pattern = re.compile('url\("(https.*?)"\)')
            match_result = re.search(pattern, single_captcha_element_style)
            single_captcha_element_url = match_result.group(
                1) if match_result else None
            logger.debug(
                f'single_captcha_element_url {single_captcha_element_url}')
            with open(CAPTCHA_SINGLE_IMAGE_FILE_PATH % (i,), 'wb') as f:
                f.write(requests.get(single_captcha_element_url).content)
            resized_single_captcha_base64_string = resize_base64_image(
                CAPTCHA_SINGLE_IMAGE_FILE_PATH % (i,), (100, 100))
            resized_single_captcha_base64_strings.append(
                resized_single_captcha_base64_string)

        logger.debug(
            f'length of single_captcha_element_urls {len(resized_single_captcha_base64_strings)}')

        # try to verify using API
        captcha_recognize_result = self.captcha_resolver.create_task(
            resized_single_captcha_base64_strings,
            self.captcha_target_text
        )
        if not captcha_recognize_result:
            logger.error('count not get captcha recognize result')
            return
        recognized_results = captcha_recognize_result.get(
            'solution', {}).get('objects')

        if not recognized_results:
            logger.error('count not get captcha recognized indices')
            return

        # click captchas
        recognized_indices = [i for i, x in enumerate(recognized_results) if x]
        logger.debug(f'recognized_indices {recognized_indices}')
        click_targets = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.task-image')))
        for recognized_index in recognized_indices:
            click_target: WebElement = click_targets[recognized_index]
            click_target.click()
            time.sleep(random())

        # after all captcha clicked
        verify_button: WebElement = self.get_verify_button()
        if verify_button.is_displayed:
            verify_button.click()
            time.sleep(3)

        # 判断窗口是否存在并调用 verify_captcha() 函数
        if self.is_element_present((By.XPATH, '/html/body/div[5]/div[1]/iframe')):
            self.verify_captcha()
        else:
            logger.debug('verifed successfully')

    def resolve(self):
        self.trigger_captcha()
        self.verify_captcha()
