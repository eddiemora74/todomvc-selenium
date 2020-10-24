from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        """
        Gets a locator type and returns the correct "By" type.
        :param locator_type: The type of locator
        :type locator_type: string
        :return: the correct "By" type
        """
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "linktext":
            return By.LINK_TEXT
        elif locator_type == "class":
            return By.CLASS_NAME
        else:
            print(
                f"Locator type {locator_type} does not exist or is not supported.")
        return False

    def get_element(self, locator_type, locator):
        """
        Gets an element object by a specified locator and locator type.
        :param str locator: Locator of an element
        :param str locator_type: Locator type of an element
        :return: Element object
        """
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{locator} could not be found.")
        finally:
            return element

    def get_elements(self, locator_type, locator):
        """
        Gets a list of element objects by a specified locator and locator type.
        :param str locator: Locator of elements
        :param str locator_type: Locator type of elements
        :return: List of Element object
        """
        elements = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            elements = self.driver.find_elements(by_type, locator)
        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{locator} could not be found")
        finally:
            return elements

    def click_element(self, locator_type, locator):
        """
        Clicks an element by a specified locator and locator type.
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            element.click()
        except:
            print(f"Element {locator_type}: {locator} could not be clicked")

    def double_click_element(self, locator_type, locator):
        """
        Doubleclicks an element by a specified locator and locator type.
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
        except:
            print(f"Could not doubleclick element {locator_type}: {locator}")

    def type_into_element(self, text, locator_type, locator):
        """
        Types a text into an element by a specified locator and locator type.
        :param str text: Text to be typed into element
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            element.send_keys(text)
        except:
            print(f"Could not type into element {locator_type}: {locator}")

    def type_into_element_and_press_enter(self, text, locator_type, locator):
        """
        Types a text into an element by a specified locator and locator type and presses the ENTER key.
        :param str text: Text to be typed into element
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            element.send_keys(text)
            element.send_keys(Keys.ENTER)
        except:
            print(f"Could not type into element {locator_type}: {locator}")

    def type_backspace_into_element(self, locator_type, locator, num=1):
        """
        Types the BACKSPACE key into an element by a specified locator and locator type for a specified amount of times
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :param int num: Number of times to backspace
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            for i in range(0, num):
                element.send_keys(Keys.BACKSPACE)
        except:
            print(
                f"Could not send backspace key into element {locator_type}: {locator}")

    def hover_over_element(self, locator_type, locator, wait=0.5):
        """
        Hovers over an element by a specified locator and locator type. A default  sleep of half-second is appended to the end of the action.
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :param float wait: Amount of time to sleep after action
        :return: None
        """
        try:
            element = self.get_element(locator_type, locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            sleep(wait)
        except:
            print(f"Could not hover over element {locator_type}: {locator}")

    def is_element_present(self, locator_type, locator):
        """
        Determines if an element by a specified locator and locator type is present in the DOM.
        :param str locator: Locator of element
        :param str locator_type: Locator type of element
        :return: Boolean
        """
        try:
            element = self.get_element(locator_type, locator)
            if element is not None:
                return True
            else:
                return False
        except:
            return False
