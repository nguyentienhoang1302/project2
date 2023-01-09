from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import  time
import zipfile
import os
def init_driver(headless=False,proxy=''):
    options = Options()
    options.headless = headless
    # ko hien image
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option('prefs',prefs)
    options.add_argument("--window-size=1920,1200")
    # options.add_argument("--user-data-dir={}".format('C:\\Users\\cucun\\AppData\\Local\\Google\\Chrome\\User Data'))
    #
    # options.add_argument('--profile-directory=project1')
    # options.add_argument("--user-data-dir={}".format('C:\\Users\\cucun\\AppData\\Local\\Google\\Chrome\\User Data'))

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    driver = webdriver.Chrome(executable_path="F:\\chromedriver",options=options)
    return driver

def check_curent_ip(driver):
    driver.get('https://api6.ipify.org?format=json')
    text=driver.find_element(By.CSS_SELECTOR,'body').text
    # print(text)
    return text

def wait_element_can_click(driver,css_element):
    return WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_element)))

def upload_file(self, driver, file_path):
    driver.find_element_by_css_selector('input[type="file"]').send_keys(file_path)
def wait_element_can_located(driver,css_element):
    return WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, css_element)))

def login(driver, url, css_user, user, css_pass, password, css_submit):
    driver.get(url)
    time.sleep(5)

    # wait until element located
    driver.wait_element_can_located(driver, css_user)
    print('css_user', css_user)
    print('user', user)

    driver.find_element_by_css_selector(css_user).send_keys(user)
    time.sleep(1)
    driver.find_element_by_css_selector(css_pass).send_keys(password)
    time.sleep(1)
    driver.find_element_by_css_selector(css_submit).click()
    time.sleep(10)

    list_err = driver.find_elements_by_css_selector('#login_error')
    print(len(list_err))

    if len(list_err):
        driver.find_element_by_css_selector(css_user).send_keys(user)
        time.sleep(1)
        driver.find_element_by_css_selector(css_pass).send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector(css_submit).click()
        time.sleep(10)


def post_anhAll_wp(driver, url, list_image_locals):
    driver.get(url)
    time.sleep(5)
    dem = 0
    for filePath in list_image_locals:
        try:
            time.sleep(2)
            file_ip = WebDriverWait(driver, 10).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, "input[type=file]")))
            file_ip.send_keys(filePath)
            dem += 1
        except:
            print("err")

    # wait until all upload success
    eles = driver.find_elements_by_css_selector('.edit-attachment')
    demtimeout = 0
    timeout = 60
    while (len(eles) < dem):
        print('len(eles)', len(eles))
        eles = driver.find_elements_by_css_selector('.edit-attachment')
        time.sleep(2)

        demtimeout += 1
        if demtimeout > timeout:
            break

    print('dem', dem)
    time.sleep(10)
    print("upload done")


def get_list_link_after_upload_all_wp(driver1):
    list_link_image = driver1.find_elements_by_css_selector('.pinkynail')
    list_link_image = [link_image.get_attribute('src') for link_image in list_link_image]
    list_link_image = [driver1.remove_ext(link_image) for link_image in list_link_image]

    list_file_name = driver1.find_elements_by_css_selector('.title')
    list_file_name = [file_name.text for file_name in list_file_name]

    return list_link_image, list_file_name


def post_bai(driver, url, title, ndung, description='', id_wp=''):
    driver.get(url)
    time.sleep(0.5)
    driver.get(url)
    time.sleep(5)

    html_btn = driver.wait_element_can_click(driver, '#content-html')
    html_btn.click()

    ndung = ndung.replace("'", '')
    try:
        driver.execute_script("document.querySelector('#content').value=`" + ndung + "`")
    except:
        return 'err_post'

    title_input = driver.wait_element_can_located(driver, '#title')
    title_input.send_keys(title)

    if description:
        driver.find_element_by_css_selector('[name="aiosp_description"]').send_keys(description)
    if id_wp:
        js = "document.querySelector('#category-" + '%s' % id_wp + " label').click()"
        driver.execute_script(js)

    driver.find_element_by_css_selector('#set-post-thumbnail.thickbox').click()
    # chuyen tab chon anh
    # menu_item_browse = self.wait_element_can_click(driver, '#menu-item-browse')
    # menu_item_browse.click()

    thumbnail_btn = driver.wait_element_can_click(driver, '.thumbnail')
    thumbnail_btn.click()

    set_thumnail_btn = driver.wait_element_can_click(driver, '.search-form button')
    set_thumnail_btn.click()

    # public_btn = self.wait_element_can_click(driver, '#publish')
    # public_btn.click()
    time.sleep(10)
    driver.execute_script("document.querySelector('#publish').click()")

    link_post = driver.wait_element_can_located(driver, '#sample-permalink a')
    link_post = link_post.get_attribute('href')
    time.sleep(5)
    return link_post


def initDriverPrivateProxy(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS,headless=False, use_proxy=True, user_agent=None):

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    # path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(executable_path="F:\\chromedriver", options=chrome_options)
    # driver = webdriver.Chrome(
    #     os.path.join(path, 'chromedriver'),
    #     chrome_options=chrome_options)
    return driver


if __name__=='__main__':
    # PROXY_HOST = '45.142.157.41'  # rotating proxy
    # PROXY_PORT = 5017
    # PROXY_USER = 'autoproxy_tDujkSc3'
    # PROXY_PASS = 'VoHyBMjixU'
    # driver=initDriverPrivateProxy(PROXY_HOST=PROXY_HOST,PROXY_PORT=PROXY_PORT,PROXY_USER=PROXY_USER,PROXY_PASS=PROXY_PASS)
    pass





