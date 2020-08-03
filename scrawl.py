import argparse, os, sys
import logging
# 导入 webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

seconds_to_wait = 10


def generate_parser():
    parser = argparse.ArgumentParser(
        description="This is a scrawler to get history price from gwdang.com")
    parser.add_argument(
        "--days",
        "-d",
        action="store",
        help="how many days you want to query the price history ")
    parser.add_argument(
        "-s",
        "--show",
        action="append",
        help=
        "show properties of the product: lowest -- the lowest price during these days.    highest -- the highest price these days    current -- the price now  make_up_lowest -- the lowest price with make up.    price_url -- the url who shows the price history. title -- product title "
    )
    parser.add_argument("product_url",
                        help="the url of the jingdong/taobao/tmall product")
    return parser


def scrawl(args):
    res = {}
    # 创建chrome启动选项
    chrome_options = webdriver.ChromeOptions()
    # 指定chrome启动类型为headless 并且禁用gpu
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--proxy-server=%s"%"localhost:1090")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    )
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        'permissions.default.stylesheet': 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # enter home page
    gwdang_url_1 = "http://www.gwdang.com"
    driver.get(gwdang_url_1)
    logging.debug("successfully entered gwdang.com")
    # input product url and search
    try:
        element = WebDriverWait(driver, seconds_to_wait).until(
            EC.presence_of_element_located((By.ID, "header_search_input")))

        element = WebDriverWait(driver, seconds_to_wait).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='搜  索']")))
    except:
        logging.error("can't find input box or submit button")
        raise
    else:
        driver.find_element_by_id('header_search_input').send_keys(
            args.product_url)

        driver.find_element_by_class_name('search_topbtn1').send_keys(
            Keys.RETURN)
    logging.debug("successfully submitted product_url")

    # get the prices
    try:
        element = WebDriverWait(driver, seconds_to_wait).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@id='ymj-max']")))

        element = WebDriverWait(driver, seconds_to_wait).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@id='ymj-min']")))

        element = WebDriverWait(driver, seconds_to_wait).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='product-info']/div[@class='right fl']/a")))
    except:
        logging.error("can't find price")
        raise
    else:
        res['current'] = driver.find_element_by_xpath(
            "//span[@class='current-price']").text[1:]
        res['highest'] = driver.find_element_by_xpath(
            "//span[@id='ymj-max']//span[@class='price']").text[1:]
        res['lowest'] = driver.find_element_by_xpath(
            "//span[@id='ymj-min']//span[@class='price']").text[1:]
        res['title'] = driver.find_element_by_xpath(
            "//div[@class='product-info']/div[@class='right fl']/a").text
        res['price_url'] = driver.current_url
        try:
            res['make_up_lowest'] = driver.find_element_by_xpath(
                "//div[@id='cddsj']//span[@class='price']").text[1:]
        except:
            logging.info(
                "can't find make up price. replacing it with lowest price")
            res['make_up_lowest'] = res['lowest']
    logging.debug("successfully got price")
    return res


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = generate_parser()
    logging.debug(parser)
    # for debug
    sys.argv.append(
        "https://detail.tmall.com/item.htm?id=587778512054&ali_refid=a3_430673_1006:1103773051:N:ySb/+7HKDOf3iN7qa6dVF8xOZWNd6hJj:bd1587d80b6d0e4b9c91495d07442ab4&ali_trackid=1_bd1587d80b6d0e4b9c91495d07442ab4&spm=a2e15.8261149.07626516002.1"
    )
    args = parser.parse_args(sys.argv[1:])

    res = scrawl(args)
    # print wanted prices
    for key in args.show:
        try:
            res += (locals()[key] + '  ')
        except:
            logging.error("can't print wanted price")
            raise
    '''
    https://detail.tmall.com/item.htm?id=587778512054&ali_refid=a3_430673_1006:1103773051:N:ySb/+7HKDOf3iN7qa6dVF8xOZWNd6hJj:bd1587d80b6d0e4b9c91495d07442ab4&ali_trackid=1_bd1587d80b6d0e4b9c91495d07442ab4&spm=a2e15.8261149.07626516002.1

    '''
