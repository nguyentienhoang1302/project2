from utils_selenium import *
from utils_class import *
def create_driver():
    driver = init_driver()
    return driver
def get_links(driver):
    # B1
    driver.get("https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567")
    # B2
    wait_element_can_located(driver=driver,css_element="footer")
    footer = driver.find_element(By.CSS_SELECTOR, "footer")
    driver.execute_script("arguments[0].scrollIntoView();", footer)
    time.sleep(5)
    elems = []
    print(1)
    while len(elems) < 59:
        print(len(elems))
        time.sleep(2)
        elems = driver.find_elements(By.CSS_SELECTOR, "a[data-sqe='link'")
        driver.execute_script("arguments[0].scrollIntoView();", elems[len(elems) - 10])
    links = [elem.get_attribute('href') for elem in elems]
    print(3)

    print(len(links))
    file = File_Interact('links.txt')
    file.write_file_from_list(links)

def save_rating(driver,index_link,link,star_rating):
    rating_elems = driver.find_elements(By.CSS_SELECTOR, "._280jKz")
    L_rating=[]
    # L_rating = [f"{index_link},{link},{star_rating},{rating.text}" for rating in rating_elems]
    for rating in rating_elems:
        text=rating.text.replace("\n","  ")
        L_rating.append(f"{index_link},{link},{star_rating},{text}")
    if L_rating:
        file = File_Interact('rating1.csv')
        file.write_file_from_list(L_rating)
        return 1
    else:
        print("break")
        print(L_rating)
        return 0

def get_rating(driver):
    # lay link
    file = File_Interact('links.txt')
    links=file.read_file_list()
    for i in range(9,11):
        index_link=i
        link=links[index_link]
        print(index_link)
        print(link)
        driver.get(link)

        # Chon tu 1 sao den 5 sao
        wait_element_can_click(driver,".product-rating-overview__filter")
        start_click=driver.find_elements(By.CSS_SELECTOR,".product-rating-overview__filter")
        for i in range(1,6):
            start_click[i].click()
            time.sleep(2)
            print(f"star {6-i}")
        # lay rating
            while (True):
                if(save_rating(driver,index_link=index_link,link=link,star_rating=i)==0):
                    break
                time.sleep(2)
                click_button_next = driver.find_element(By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right ").click()
                time.sleep(2)
            print("Break")

if __name__=="__main__":
    driver=create_driver()
    get_links(driver)













