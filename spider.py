import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_url_list(root_url):
    driver = webdriver.Edge()
    driver.get(root_url + 'list_119446')
    driver.implicitly_wait(10)
    height = 0
    while True:
        new_height = driver.execute_script('return document.body.scrollHeight;')
        if new_height > height:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            height = new_height
            time.sleep(2)
        else:
            driver.execute_script('window.scrollTo(0, 0)')
            break

    wrapper = driver.find_element(By.CLASS_NAME, 'index_container__ytvOZ')
    a_lis = wrapper.find_elements(By.CSS_SELECTOR, '[href^="/newsDetail_forward_"]')
    href_lis = []
    for a_tag in a_lis:
        href = a_tag.get_attribute('href')
        if '?' not in href:
            href_lis.append(href)
    driver.quit()
    return href_lis


def get_news(url):
    response = requests.get(url=url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    news = ''
    try:
        wrapper = soup.find(attrs={'class': 'index_wrapper__L_zqV'})
        p_lis = wrapper.findAll('p')
        for p_tag in p_lis:
            news += p_tag.text.strip('·').replace('\n', '')
        print(news)
    except:
        print('出错！！！')
        pass
    return news


def run():
    root_url = 'https://www.thepaper.cn/'
    url_list = get_url_list(root_url)
    print(url_list)
    news = ''
    for url in url_list:
        print(url)
        news += get_news(url)
        print('========================================')
        time.sleep(1)
    print(news)
    try:
        with open('../results/news.txt', 'w') as f:
            f.write(news)
            f.close()
            print('写入成功！')
    except IOError as error:
        print(error)
