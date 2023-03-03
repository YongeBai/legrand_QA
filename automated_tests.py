
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

import unittest

from typing import Set, List, Tuple



class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        website = "https://www.demoblaze.com/"
        self.website = website
        self.driver = webdriver.Chrome()
        self.driver.get(self.website)
        self.driver.maximize_window()

    def wait_for_element(self, locator, timeout=2):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_elements(self, locator, timeout=2):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))


    def wait_for_alert(self, timeout=2):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.alert_is_present())

    def tearDown(self) -> None:
        self.driver.quit()


class TestNewAccount(TestBase):
    def test_new_account(self):
        sign_in = self.wait_for_element((By.ID, "signin2"))
        sign_in.click()
        
        assert self.wait_for_element((By.ID, "sign-username"), timeout=1)
        
        username = self.wait_for_element((By.ID, "sign-username"))
        username.send_keys("hey mama")
        
        password = self.wait_for_element((By.ID, "sign-password"))
        password.send_keys("123")

        sign_up = self.wait_for_element((By.XPATH, "//button[@onclick='register()']"))
        sign_up.click()

        alert = self.wait_for_alert()
        assert "Sign up successful." in alert.text
        alert.accept()

        
        close_sign_in = self.wait_for_element((By.XPATH, "//*[@id='signInModal']/div/div/div[3]/button[1]"))
        close_sign_in.click()

        assert EC.invisibility_of_element_located((By.ID, "signin2"))

class TestExistingAccount(TestBase):
    def test_existing_account(self):
        sign_in = self.wait_for_element((By.ID, "signin2"))
        sign_in.click()
        
        assert self.wait_for_element((By.ID, "sign-username"), timeout=1)
        
        username = self.wait_for_element((By.ID, "sign-username"))
        username.send_keys("hi mom")
        
        password = self.wait_for_element((By.ID, "sign-password"))
        password.send_keys("123")

        sign_up = self.wait_for_element((By.XPATH, "//button[@onclick='register()']"))
        sign_up.click()

        alert = self.wait_for_alert()
        assert "This user already exist." in alert.text
        alert.accept()

        
        close_sign_in = self.wait_for_element((By.XPATH, "//*[@id='signInModal']/div/div/div[3]/button[1]"))
        close_sign_in.click()

        assert EC.invisibility_of_element_located((By.ID, "signin2"))


class TestSuccessfulLogin(TestBase):
    def test_successful_login(self):
        log_in = self.wait_for_element((By.ID, "login2"))
        log_in.click()
        
        assert self.wait_for_element((By.ID, "loginusername"), timeout=1)
        
        username = self.wait_for_element((By.ID, "loginusername"))
        username.send_keys("hi mom")
        
        password = self.wait_for_element((By.ID, "loginpassword"))
        password.send_keys("123")

        log_in = self.wait_for_element((By.XPATH, "//button[@onclick='logIn()']"))
        log_in.click()

        assert EC.visibility_of_element_located((By.ID, "nameofuser"))


class TestUnsuccessfulLogin(TestBase):
    def test_unsuccessful_login(self):
        log_in = self.wait_for_element((By.ID, "login2"))
        log_in.click()
        
        assert self.wait_for_element((By.ID, "loginusername"), timeout=1)
        
        username = self.wait_for_element((By.ID, "loginusername"))
        username.send_keys("hi mom")
        
        password = self.wait_for_element((By.ID, "loginpassword"))
        password.send_keys("1")

        log_in = self.wait_for_element((By.XPATH, "//button[@onclick='logIn()']"))
        log_in.click()

        alert = self.wait_for_alert()
        assert "Wrong password." in alert.text
        alert.accept()

        close_sign_in = self.wait_for_element((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[1]"))
        close_sign_in.click()

        assert EC.visibility_of_element_located((By.ID, "nameofuser"))


class TestNonExistentLogin(TestBase):
    def test_nonexistent_login(self):
        log_in = self.wait_for_element((By.ID, "login2"))
        log_in.click()
        
        assert self.wait_for_element((By.ID, "loginusername"), timeout=1)
        
        username = self.wait_for_element((By.ID, "loginusername"))
        username.send_keys("dakhblakdsjf")
        
        password = self.wait_for_element((By.ID, "loginpassword"))
        password.send_keys("1")

        log_in = self.wait_for_element((By.XPATH, "//button[@onclick='logIn()']"))
        log_in.click()

        alert = self.wait_for_alert()
        assert "User does not exist." in alert.text
        alert.accept()

        close_sign_in = self.wait_for_element((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[1]"))
        close_sign_in.click()

        assert EC.visibility_of_element_located((By.ID, "nameofuser"))


class TestLogout(TestSuccessfulLogin):
    def __call__(self, *args, **kwargs):
        super(TestLogout, self).__call__(*args, **kwargs)

    def test_logout(self):
        self.test_successful_login()
        log_out = self.wait_for_element((By.XPATH, "//*[@onclick='logOut()']"))
        log_out.click()
        
        assert EC.visibility_of_element_located((By.ID, "signin2"))


class TestAddingItem(TestBase):
    def __init__(self, item_names: List[str]):
        super().__init__()
        self.item_names = item_names

    def find_item(self, item_name: str) -> None:
        element = self.wait_for_element((By.LINK_TEXT, item_name))
        element.click()

    def add_item(self) -> None:
            
        add_to_card= self.wait_for_element((By.LINK_TEXT, "Add to cart"))
        add_to_card.click()

        alert = self.wait_for_alert()
        assert "Product added" in alert.text
        alert.accept()
    
    def extract_item_info(self, item_info) -> Tuple[str, int]:
        item_info = item_info.split()
        item_name = " ".join(item_info[:-2])
        item_price = int(item_info[-2])
        return item_name, item_price

    def check_cart(self) -> None:
        cart_items = self.wait_for_elements((By.XPATH, "//tbody[@id='tbodyid']/tr[@class='success']"))
        cart_names_set = set()

        excepted_price = self.wait_for_element((By.ID, "totalp"))
        excepted_price = int(excepted_price.text)

        total_price = 0

        for item in cart_items:
            item_name, item_price = self.extract_item_info(item.text)
            cart_names_set.add(item_name)
            total_price += item_price

        assert total_price == excepted_price

        for item in self.item_names:
            if item in cart_names_set:
                cart_names_set.remove(item)
        assert len(cart_names_set) == 0

class TestAddingSameItem(TestAddingItem):
    def __init__(self, test_name: str):
        self.item_names = ["Samsung galaxy s6", "Samsung galaxy s6"]

    def __call__(self, *args, **kwargs):
        self.test_add_same_items()

    def test_add_same_items(self) -> None:
        item_name = self.item_names[0]
        self.find_item(item_name)
        for _ in range(2):
            self.add_item()

        cart = self.wait_for_element((By.ID, "cartur"))
        cart.click()
            
        assert self.wait_for_element((By.XPATH, "//*[@id='page-wrapper']/div/div[2]/button"), timeout=1)

        self.check_cart()

class TestAddingUniqueItem(TestAddingItem):
    def __init__(self, test_name: str):
        self.item_names = ["Samsung galaxy s6", "Nokia lumia 1520"]

    def __call__(self, *args, **kwargs):
        self.test_add_unique_items()

    def test_add_unique_items(self) -> None:
        
        for item in self.item_names:
            self.find_item(item)
            self.add_item()
            
            home = self.wait_for_element((By.XPATH, "//*[@href='index.html']"))
            home.click()

        cart = self.wait_for_element((By.ID, "cartur"))
        cart.click()
            
        assert self.wait_for_element((By.XPATH, "//*[@id='page-wrapper']/div/div[2]/button"), timeout=1)

        self.check_cart()

class TestCheckoutSuccessful(TestAddingUniqueItem):
    def __init__(self, test_name: str):
        self.item_names = ["Samsung galaxy s6", "Nokia lumia 1520"]

    def test_checkout_items(self) -> None:

        self.test_add_unique_items()

        checkout = self.wait_for_element((By.XPATH, "//*[@id='page-wrapper']/div/div[2]/button"))
        checkout.click()

        assert EC.visibility_of_element_located((By.XPATH, "//button[@onclick='purchaseOrder()']"))

        name = self.wait_for_element((By.ID, "name"))
        name.send_keys("1")

        country = self.wait_for_element((By.ID, "country"))
        country.send_keys("1")

        city = self.wait_for_element((By.ID, "city"))
        city.send_keys("1")

        credit_card = self.wait_for_element((By.ID, "card"))
        credit_card.send_keys("1")

        month = self.wait_for_element((By.ID, "month"))
        month.send_keys("1")

        year = self.wait_for_element((By.ID, "year"))
        year.send_keys("1")
        
        purchase = self.wait_for_element((By.XPATH, "//button[@onclick='purchaseOrder()']"))
        purchase.click()

        assert EC.visibility_of_element_located((By.XPATH, "//*[@class='confirm btn btn-lg btn-primary']"))

        confirm_purchase = self.wait_for_element((By.XPATH, "//*[@class='confirm btn btn-lg btn-primary']"))
        confirm_purchase.click()



class TestCheckoutUnsuccessful(TestAddingUniqueItem):

    def __init__(self, test_name: str):
        self.item_names = ["Samsung galaxy s6", "Nokia lumia 1520"]
        
    def test_checkout_items(self) -> None:
        
        self.test_add_unique_items()
        
        checkout = self.wait_for_element((By.XPATH, "//*[@id='page-wrapper']/div/div[2]/button"))
        checkout.click()

        assert EC.visibility_of_element_located((By.XPATH, "//button[@onclick='purchaseOrder()']"))

        name = self.wait_for_element((By.ID, "name"))
        name.send_keys("1")

        country = self.wait_for_element((By.ID, "country"))
        country.send_keys("1")

        city = self.wait_for_element((By.ID, "city"))
        city.send_keys("1")

        credit_card = self.wait_for_element((By.ID, "card"))
        credit_card.send_keys("1")
        
        purchase = self.wait_for_element((By.XPATH, "//button[@onclick='purchaseOrder()']"))
        purchase.click()

        alert = self.wait_for_alert()
        assert "Please fill out required fields" in alert.text
        alert.accept()


class TestDeletingItem(TestAddingUniqueItem):
    def delete_item(self, item_name: str) -> None:
        cart_items = self.driver.find_elements(By.XPATH, "//tbody[@id='tbodyid']/tr[@class='success']")

        for item in cart_items:
            name, _ = self.extract_item_info(item.text)
            if name == item_name:
                delete_link = item.find_element(By.XPATH, f"//tr[td[text()='{item_name}']]//a[text()='Delete']")
                delete_link.click()
                break

class TestDeleteTwoItems(TestDeletingItem):
    def test_delete_two_items(self) -> None:
        self.test_add_unique_items()
        self.delete_item(self.item_names[0])
        self.delete_item(self.item_names[1])


class TestDeleteOneItem(TestDeletingItem):
    def test_delete_one_items(self) -> None:
        self.test_add_unique_items()
        self.delete_item(self.item_names[1])


class NavigationTest(TestBase):
    def nagivate_to(self, catagory: str) -> None:
        catagory = self.wait_for_element((By.XPATH, f'//a[@onclick="byCat(\'{catagory}\')"]'))
        catagory.click()
        time.sleep(1)

    def nagivate_next(self) -> None:
        next_button = self.wait_for_element((By.ID, 'next2'))
        next_button.click()
        time.sleep(1)
    
    def nagivate_previous(self) -> None:
        previous_button = self.wait_for_element((By.ID, 'prev2'))
        previous_button.click()
        time.sleep(1)

    def take_catalogue(self) -> Set[str]:
        catalogue = self.wait_for_element((By.ID, 'tbodyid'))
        full_catalogue = catalogue.text.splitlines()
        
        items_catalogue = set(full_catalogue[::3])
        return items_catalogue
    
    def verify_catalogue(self, cataloguePrev: Set[str], catalogueNext: Set[str]) -> bool:
        return cataloguePrev.intersection(catalogueNext) == set()
    
class TestLaptopNavigation(NavigationTest):
    def test_laptop_navigation(self) -> None:
        self.nagivate_to("notebook")
        
        cataloguePrev = self.take_catalogue()
        self.nagivate_next()

        catalogueNext = self.take_catalogue()
        self.nagivate_previous()

        assert self.verify_catalogue(cataloguePrev, catalogueNext)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestNewAccount("test_new_account"))
    suite.addTest(TestExistingAccount("test_existing_account"))
    suite.addTest(TestSuccessfulLogin("test_successful_login"))
    suite.addTest(TestUnsuccessfulLogin("test_unsuccessful_login"))
    suite.addTest(TestNonExistentLogin("test_nonexistent_login"))
    suite.addTest(TestLogout("test_logout"))
    # suite.addTest(TestAddingSameItem("test_add_same_item"))
    # suite.addTest(TestAddingUniqueItem("test_add_unique_items"))
    # suite.addTest(TestCheckoutSuccessful("test_checkout_items"))
    # suite.addTest(TestCheckoutUnsuccessful("test_checkout_items"))
    # suite.addTest(TestDeleteTwoItems("test_delete_two_items"))
    # suite.addTest(TestDeleteOneItem("test_delete_one_items"))
    suite.addTest(TestLaptopNavigation("test_laptop_navigation"))
    unittest.TextTestRunner(verbosity=2).run(suite)
