import sys
import os
from   selenium             import webdriver
from   time                 import sleep
import speech_recognition   as     sr
from   selenium.webdriver.common.keys import Keys
import urllib
import requests
import pydub

URL = 'https://www.google.com/recaptcha/api2/demo'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# visit url
driver = webdriver.Edge(resource_path('./driver/msedgedriver.exe'))
driver.get(URL)
# switch to first iframe (hopefully captcha)
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
# click on captcha checkbox
checkbox = driver.find_element_by_id('recaptcha-anchor')
checkbox.click()
# switch to captcha challenge iframe
driver.switch_to.default_content()
chalenge_frame = driver.find_element_by_css_selector('iframe[title="recaptcha challenge"]')
driver.switch_to.frame(chalenge_frame)
sleep(1)
# print(chalenge_frame.get_attribute('title'))
audio_option = driver.find_element_by_class_name('rc-button-audio')
audio_option.click()
# switch to captcha challenge iframe
driver.switch_to.default_content()
chalenge_frame = driver.find_element_by_css_selector('iframe[title="recaptcha challenge"]')
driver.switch_to.frame(chalenge_frame)
sleep(1)
play_btn = driver.find_element_by_class_name('rc-audiochallenge-play-button')
play_btn.click()
# downloading and parsing audio from source
audio_src = driver.find_element_by_id("audio-source").get_attribute("src")
urllib.request.urlretrieve(audio_src, resource_path('sample.mp3'))
sound = pydub.AudioSegment.from_mp3(resource_path('sample.mp3'))
sound.export(resource_path('sample.wav'), format="wav")
sample_audio = sr.AudioFile(resource_path('sample.wav'))
# recognize audio using google
r = sr.Recognizer()
with sample_audio as source:
    audio = r.record(source)
text = r.recognize_google(audio)
# print("Recognised audio:" + text.lower())
driver.find_element_by_id("audio-response").send_keys(text.lower())
driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
driver.switch_to.default_content()
sleep(1)
driver.find_element_by_id("recaptcha-demo-submit").click()