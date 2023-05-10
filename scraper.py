import tls_client
import requests
import os
import re
import math
import base64
import hashlib
import datetime
import time
import json
import cv2
import imagehash
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk




class hCaptchaScraper:
    def __init__(self, host, sitekey, specific_query=None):
        # Scraper
        self.host = host
        self.sitekey = sitekey
        self.v = requests.get('https://hcaptcha.com/1/api.js').text.split('assetUrl:"https://newassets.hcaptcha.com/captcha/v1/')[1].split('/')[0]
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
        self.questions = os.listdir(self.output_dir)
        self.session = tls_client.Session(client_identifier='chrome_110', random_tls_extension_order=True)
        self.specific_query = None  # specific_query  # Currently not working

        # Scraped Queue [(img, img_hash, question)...]
        self.scraped_queue = []

        # UI
        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.root.title("hCaptcha Scraper")

        # Static Label
        self.label = tk.Label(self.root, text="hCaptcha Scraper", font="Helvetica 16 bold italic")
        self.label.pack()

        # Question label
        self.qlabel = tk.Label(self.root, text="Click scrape to start", font="Helvetica 12 bold")
        self.qlabel.pack()

        # Create the image label
        self.photo = None
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Create the yes and no buttons
        self.yes_button = tk.Button(self.root, text="Yes", command=self.yes, pady=10, padx=100, bg="green")
        self.no_button = tk.Button(self.root, text="No", command=self.no, pady=10, padx=100, bg="red")
        self.yes_button.pack()
        self.no_button.pack()

        # Create the scrape button
        self.scrape_button = tk.Button(self.root, text="Scrape", command=self.scrape_func, pady=10, padx=90, bg="cyan")
        self.scrape_button.pack()

    def get_c(self):
        r = self.session.get(
            'https://hcaptcha.com/checksiteconfig',
            headers={
                'authority': 'hcaptcha.com',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'text/plain',
                'origin': 'https://newassets.hcaptcha.com',
                'referer': 'https://newassets.hcaptcha.com/',
                'sec-ch-ua': '"Chromium";v="110", "Google Chrome";v="110", "Not:A-Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            },
            params={
                'v': self.v,
                'host': self.host,
                'sitekey': self.sitekey,
                'sc': '1',
                'swa': '1',
            }
        )
        return r.json()['c']

    def get_n(self, req):
        # cred: h0nde
        x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        req = req.split(".")

        req = {
            "header": json.loads(
                base64.b64decode(
                    req[0] +
                    "=======").decode("utf-8")),
            "payload": json.loads(
                base64.b64decode(
                    req[1] +
                    "=======").decode("utf-8")),
            "raw": {
                "header": req[0],
                "payload": req[1],
                "signature": req[2]}}

        def a(r):
            for t in range(len(r) - 1, -1, -1):
                if r[t] < len(x) - 1:
                    r[t] += 1
                    return True
                r[t] = 0
            return False

        def ix(r):
            t = ""
            for n in range(len(r)):
                t += x[r[n]]
            return t

        def o(r, e):
            n = e
            hashed = hashlib.sha1(e.encode())
            o = hashed.hexdigest()
            t = hashed.digest()
            e = None
            n = -1
            o = []
            for n in range(n + 1, 8 * len(t)):
                e = t[math.floor(n / 8)] >> n % 8 & 1
                o.append(e)
            a = o[:r]

            def index2(x, y):
                if y in x:
                    return x.index(y)
                return -1

            return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)

        def get():
            for e in range(25):
                n = [0 for i in range(e)]
                while a(n):
                    u = req["payload"]["d"] + "::" + ix(n)
                    if o(req["payload"]["s"], u):
                        return ix(n)

        result = get()
        hsl = ":".join([
            "1",
            str(req["payload"]["s"]),
            datetime.datetime.now().isoformat()[:19]
            .replace("T", "")
            .replace("-", "")
            .replace(":", ""),
            req["payload"]["d"],
            "",
            result
        ])
        return hsl

    def construct_data(self):
        c = self.get_c()
        c['type'] = 'hsl'
        data = {
            'sitekey': self.sitekey,
            'v': self.v,
            'host': self.host,
            'n': self.get_n(c['req']),
            'motiondata': '{"st":1628923867722,"mm":[[203,16,1628923874730],[155,42,1628923874753],[137,53,1628923874770],[122,62,1628923874793],[120,62,1628923875020],[107,62,1628923875042],[100,61,1628923875058],[93,60,1628923875074],[89,59,1628923875090],[88,59,1628923875106],[87,59,1628923875131],[87,59,1628923875155],[84,56,1628923875171],[76,51,1628923875187],[70,47,1628923875203],[65,44,1628923875219],[63,42,1628923875235],[62,41,1628923875251],[61,41,1628923875307],[58,39,1628923875324],[54,38,1628923875340],[49,36,1628923875363],[44,36,1628923875380],[41,35,1628923875396],[40,35,1628923875412],[38,35,1628923875428],[38,35,1628923875444],[37,35,1628923875460],[37,35,1628923875476],[37,35,1628923875492]],"mm-mp":13.05084745762712,"md":[[37,35,1628923875529]],"md-mp":0,"mu":[[37,35,1628923875586]],"mu-mp":0,"v":1,"topLevel":{"st":1628923867123,"sc":{"availWidth":1680,"availHeight":932,"width":1680,"height":1050,"colorDepth":30,"pixelDepth":30,"availLeft":0,"availTop":23},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"webkitTemporaryStorage":{},"webkitPersistentStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36","platform":"MacIntel","product":"Gecko","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36","language":"en-US","languages":["en-US","en"],"onLine":true,"webdriver":false,"serial":{},"scheduling":{},"xr":{},"mediaCapabilities":{},"permissions":{},"locks":{},"usb":{},"mediaSession":{},"clipboard":{},"credentials":{},"keyboard":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"wakeLock":{},"deviceMemory":8,"hid":{},"presentation":{},"userAgentData":{},"bluetooth":{},"managed":{},"plugins":["internal-pdf-viewer","mhjfbmdgcfjbbpaeojofohoefgiehjai","internal-nacl-plugin"]},"dr":"https://discord.com/","inv":false,"exec":false,"wn":[[1463,731,2,1628923867124],[733,731,2,1628923871704]],"wn-mp":4580,"xy":[[0,0,1,1628923867125]],"xy-mp":0,"mm":[[1108,233,1628923867644],[1110,230,1628923867660],[1125,212,1628923867678],[1140,195,1628923867694],[1158,173,1628923867711],[1179,152,1628923867727],[1199,133,1628923867744],[1221,114,1628923867768],[1257,90,1628923867795],[1272,82,1628923867811],[1287,76,1628923867827],[1299,71,1628923867844],[1309,68,1628923867861],[1315,66,1628923867877],[1326,64,1628923867894],[1331,62,1628923867911],[1336,60,1628923867927],[1339,58,1628923867944],[1343,56,1628923867961],[1345,54,1628923867978],[1347,53,1628923867994],[1348,52,1628923868011],[1350,51,1628923868028],[1354,49,1628923868045],[1366,44,1628923868077],[1374,41,1628923868094],[1388,36,1628923868110],[1399,31,1628923868127],[1413,25,1628923868144],[1424,18,1628923868161],[1436,10,1628923868178],[1445,3,1628923868195],[995,502,1628923871369],[722,324,1628923874673],[625,356,1628923874689],[523,397,1628923874705],[457,425,1628923874721]],"mm-mp":164.7674418604651},"session":[],"widgetList":["0a1l5c3yudk4"],"widgetId":"0a1l5c3yudk4","href":"https://discord.com/register","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}',
            'h1': 'en',
            'c': json.dumps(c)
        }
        return data

    def get_captcha(self):
        headers = {
            'authority': 'hcaptcha.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            # "Content-length": str(len(data)),
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://newassets.hcaptcha.com',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Chromium";v="110", "Google Chrome";v="110", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        data = self.construct_data()
        r = self.session.post(
            f'https://hcaptcha.com/getcaptcha/{self.sitekey}',
            headers=headers,
            data=data
        )
        #print(r.text)
        return r.json()

    def format_question(self, question):
        return question.replace('Please click each image containing an ', '').replace('Please click each image containing a ', '').replace('Please click each image containing ', '').replace(' ', '_').lower()

    def check_question(self, question):
        if question not in self.questions:
            os.mkdir(os.path.join(self.output_dir, question))
            os.mkdir(os.path.join(self.output_dir, question, 'yes'))
            os.mkdir(os.path.join(self.output_dir, question, 'bad'))

    def generate_hash(self, img):
        if isinstance(img, np.ndarray):
            resized_img = cv2.resize(img, (100, 100))
        else:
            # If img is not a numpy array, convert it to one
            img_array = np.array(img)
            resized_img = cv2.resize(img_array, (100, 100))
        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        hash_val = str(imagehash.phash(Image.fromarray(gray_img)))
        return hash_val

    def handle_centre_click_captcha(self, captcha_payload, question):
        image_urls = [uri['metadata']['original']['original_uri'] for uri in captcha_payload['tasklist']]
        for img_url in image_urls:
            downloaded_img = self.download_image(img_url, dont_rescale=True)
            img_hash = self.generate_hash(downloaded_img)
            if img_hash+'.png' not in os.listdir(os.path.join(self.output_dir, question)):
                print(f"Downloading | H: {img_hash} | Q: {question}")
                cv2.imwrite(os.path.join(self.output_dir, question, img_hash + '.png'), downloaded_img)
            else:
                print(f"Already downloaded | H: {img_hash} | Q: {question}")

    def download_image(self, uri, dont_rescale=False):
        r = requests.get(uri, stream=True).raw
        img = np.asarray(bytearray(r.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        if not dont_rescale:
            img = cv2.resize(img, (100, 100))
        return img

    def specific_query_handler(self, question):
        if self.specific_query is None:
            return True
        else:
            if self.specific_query == question:
                return True
        return False

    def download_captcha(self):
        self.questions = os.listdir(self.output_dir)
        self.session = tls_client.Session(client_identifier='chrome_110', random_tls_extension_order=True)

        captcha = self.get_captcha()
        question = self.format_question(captcha['requester_question']['en'])
        print(question)
        self.check_question(question)

        # avoid new center click captcha
        if 'please_click_the_center' in question:
            print(f"CENTRE CLICK CAPTCHA DETECTED | Q: {question}")
            self.handle_centre_click_captcha(captcha, question)
            return self.download_captcha()

        if not self.specific_query_handler(question):
            time.sleep(3)
            return self.download_captcha()

        image_urls = [
            *captcha['requester_question_example'],
            *[i['datapoint_uri'] for i in captcha['tasklist']]
        ]

        for img_url in image_urls:
            downloaded_img = self.download_image(img_url)
            img_hash = self.generate_hash(downloaded_img)
            if img_hash+'.png' not in [*os.listdir(os.path.join(self.output_dir, question, 'yes')), *os.listdir(os.path.join(self.output_dir, question, 'bad'))]:
                print(f"Downloading | H: {img_hash} | Q: {question}")
                self.scraped_queue.append((downloaded_img, img_hash, question))
            else:
                print(f"Already downloaded | H: {img_hash} | Q: {question}")

    # TKINTER GUI

    def show(self):
        self.root.mainloop()

    def set_image(self, image):
        # Convert the CV2 image to PIL format and resize it
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(np.uint8(image))
        image = image.resize((100, 100), Image.ANTIALIAS)

        # Update the image label
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def set_qlabel(self, question):
        question = f'Q: {question}'
        self.qlabel.config(text=question)

    def load_next_image(self):
        if len(self.scraped_queue) > 0:
            self.current = self.scraped_queue.pop()
            self.set_image(self.current[0])
            self.set_qlabel(self.current[2])
        else:
            self.download_captcha()
            self.load_next_image()

    def yes(self):
        cv2.imwrite(os.path.join(self.output_dir, self.current[2], 'yes', self.current[1] + '.png'), self.current[0])
        self.load_next_image()

    def no(self):
        cv2.imwrite(os.path.join(self.output_dir, self.current[2], 'bad', self.current[1] + '.png'), self.current[0])
        self.load_next_image()

    def scrape(self):
        #print('scraped')
        #self.load_next_image()
        #self.toggle_scrape_button()
        self.load_next_image()

    def toggle_scrape_button(self):
        if self.scrape_button['state'] == 'normal':
            self.scrape_button['state'] = 'disabled'
        else:
            self.scrape_button['state'] = 'normal'

    def scrape_func(self):
        self.toggle_scrape_button()
        self.scrape()


if __name__ == "__main__":
    #hcs = hCaptchaScraper('accounts.hcaptcha.com', 'a5f74b19-9e45-40e0-b45d-47ff91b7a6c2')
    hcs = hCaptchaScraper('discord.com', '4c672d35-0701-42b2-88c3-78380b0db560')
    hcs.set_image(cv2.imread('test.png'))
    hcs.show()