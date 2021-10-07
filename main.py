from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random


class InstagramBot:
    def __init__(self, username, password):
        self.driver = webdriver.Edge(executable_path='C:\msedgedriver.exe')
        self.followers_list = []
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        user_form = self.driver.find_element_by_name('username')
        user_form.send_keys(username)
        pass_form = self.driver.find_element_by_name('password')
        pass_form.send_keys(password)
        pass_form.send_keys(Keys.ENTER)
        time.sleep(5)

    def get_followers_list(self, account: str):
        self.driver.get(f'https://instagram.com/{account}')

        time.sleep(3)

        following_count = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section'
                                                               '/ul/li[3]/a/span').text)

        following_button = self.driver.find_element_by_partial_link_text('following')
        following_button.click()

        time.sleep(3)

        popup = self.driver.find_element_by_xpath('//div[@class="isgrP"]')

        for i in range(following_count//4+1):
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                       popup)
            time.sleep(0.75)

        accounts = self.driver.find_elements_by_css_selector('.FPmhX')

        for account in accounts:
            self.followers_list.append(account.text)

    def follow_everyone(self):
        for account in self.followers_list:
            while True:
                try:
                    time.sleep(random.randint(1, 3))
                    self.driver.get(f'https://instagram.com/{account}')
                    break

                except:
                    continue

            try:
                follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header'
                                                                  '/section/div[1]/div[1]/div/div/div/span/span['
                                           
                                                                  '1]/button')
                if follow_button.text in 'Follow Back':
                    follow_button.click()

            except NoSuchElementException:
                try:
                    follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header'
                                                                      '/section/div[1]/div/div/div/a/button')
                    follow_button.click()

                except NoSuchElementException:
                    continue


if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        data = file.readlines()
        print(data)

    USERNAME = data[0].split(': ')[1]
    PASSWORD = data[1].split(': ')[1]
    TO_COPY = data[2].split(': ')[1]

    insta_bot = InstagramBot(username=USERNAME, password=PASSWORD)
    insta_bot.get_followers_list(account=TO_COPY)
    insta_bot.follow_everyone()
