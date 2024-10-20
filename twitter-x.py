from playwright.sync_api import sync_playwright
import random,logging,time,zmail

logging.basicConfig(filename='logs/self_media.log',encoding='utf-8',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

class X():
    def __init__(self,XstateFile):
        self.XstateFile = XstateFile
        self.homeUrl = 'https://x.com/home'
        try:
            with sync_playwright() as p:
                browserType = random.choice([p.chromium,p.firefox])
                browser = browserType.launch(headless=True,slow_mo=1000,args=['--start-maximized'])
                self.context = browser.new_context(storage_state=self.XstateFile,viewport={'width': 1920, 'height': 1080})
                page = self.context.new_page()
                page.goto(self.homeUrl)
                #page.wait_for_load_state('networkidle')
                time.sleep(30)
                if page.url == self.homeUrl:
                    logging.info(f'twitter正常登录，截图见 twitter-01.jpg,正常更新{self.XstateFile}')
                    page.screenshot(path='logs/twitter-01.jpg',full_page=True)
                    self.context.storage_state(path=self.XstateFile)
                else:
                    logging.info(f'twitter未能正常登录，截图见 twitter-02.jpg,请手工更新{self.XstateFile}')
                    page.screenshot(path='logs/twitter-02.jpg',full_page=True)
        except Exception as error:
            logging.info(f'twitter类初始化失败，报错如下：\n{error}')

    def get_timeline(self,mailTo,mailU,mailP):
        try:
            with sync_playwright() as p:
                browserType = random.choice([p.chromium,p.firefox])
                browser = browserType.launch(headless=True,slow_mo=1000,args=['--start-maximized'])
                context = browser.new_context(storage_state=self.XstateFile,viewport={'width': 1920, 'height': 1080})
                page = context.new_page()
                tweets = page.get_by_test_id("tweetText")
                for i in range(0,5):
                    page.goto(self.homeUrl)
                    time.sleep(10)
                    #page.wait_for_load_state('networkidle')
                    tweets.nth(i).click()
                    time.sleep(10)
                    logging.info(f'获取第{i}条tweet截图，tweet{i}.png')
                    page.screenshot(path=f'logs/tweet{i}.png',full_page=True)
                    zmailserver = zmail.server(mailU, mailP)
                    zmailserver.send_mail(mailTo,{'subject':f'Tweet--{i}','attachments': [f'tweet{i}.png',]})
        except Exception as error:
            logging.info(f'获取tweet失败，报错如下：\n{error}')

def main():
    mailU = 'clong_abchina@hotmail.com'
    mailPass = 'abc_clong'
    mailAddr1 = 'clong1688@hotmail.com'
    mailAddr2 = 'clong_abchina@hotmail.com'
    while True:
        try:
            twitter = X('stateFiles/X.json')
            twitter.get_timeline(mailAddr1,mailU,mailPass)
            time.sleep(300)
        except Exception as error:
            logging.info(f'本轮自动运行X失败，报错如下：\n{error}')

if __name__ == "__main__":
    main()