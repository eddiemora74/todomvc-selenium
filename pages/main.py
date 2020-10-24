from base.selenium_driver import BaseDriver
from time import sleep
from selenium.webdriver.common.keys import Keys


class MainApp(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    new_todo_field = ".//header[@class='header']/input[@class='new-todo']"

    complete_all_checkbox = ".//section[@class='main']/label[@for='toggle-all']"
    todo_list = ".//section[@class='main']/ul[@class='todo-list']"
    nth_todo_item_view = "div[@class='view']"
    nth_todo_item_edit = "input[@class='edit']"

    items_left_count = ".//footer[@class='footer']/span[@class='todo-count']/strong"
    clear_completed_button = ".//footer[@class='footer']/button[@class='clear-completed']"
    filter_links = ".//footer[@class='footer']/ul[@class='filters']"

    # Helpers
    def nth_todo_item(self, num, elem_type=None):
        """
        Returns an XPATH locator to return the n-th todo item.
        :param int num: The order number of the ToDo item in question (starts at 1)
        :param str elem_type: The type of element of the ToDo item in question
            label = The display label of the item
            toggle = The checkbox of the item
            destroy = The delete button of the item
        :return: String
        """
        if elem_type is None:
            return f"{self.todo_list}/li[@class='editing']/{self.nth_todo_item_edit}"

        item_type = None
        if elem_type == "label":
            item_type = f"{self.nth_todo_item_view}/label"
        elif elem_type == "toggle":
            item_type = f"{self.nth_todo_item_view}/input[@class='toggle']"
        elif elem_type == "destroy":
            item_type = f"{self.nth_todo_item_view}/button[@class='destroy']"
        return f"{self.todo_list}/li[{num}]/{item_type}"

    def get_filter_link(self, name):
        """
        Returns the locator of a filter item.
        :param str name: The display name/text on the filter link
        :return: String
        """
        return f"{self.filter_links}/li/a[text()='{name}']"

    # Action Methods
    def add_todo(self, todo):
        """
        Adds a todo item via todo field.
        :param str todo: The text of the todo to be added.
        :return: None
        """
        self.type_into_element_and_press_enter(
            todo, "xpath", self.new_todo_field)

    def get_todo_text(self, num):
        """
        Gets the text of a ToDo item based on item order.
        :param int num: The number of the ToDo item in question (starts at 1)
        :return: String
        """
        return self.get_element("xpath", self.nth_todo_item(num, "label")).text

    def get_item_count(self):
        """
        Gets the count displayed in the footer.
        :return: Integer
        """
        return int(self.get_element("xpath", self.items_left_count).text)

    def get_list_size(self):
        """
        Gets the number of items listed in the current ToDo list view. This changes based on the filter selected.
        :return: Integer
        """
        return len(self.get_elements("xpath", f"{self.todo_list}/li"))

    def click_complete_todo(self, num):
        """
        Clicks on the "Complete" checkbox for a ToDo item.
        :param int num: The number of the ToDo item in question (starts at 1)
        :return: None
        """
        self.click_element("xpath", self.nth_todo_item(num, "toggle"))

    def click_delete_todo(self, num):
        """
        Deletes a ToDo item. Must first hover over the label and then click on the "Destroy" button.
        :param int num: The number of the ToDo item in question (starts at 1)
        :return: None
        """
        self.hover_over_element("xpath", self.nth_todo_item(num, "label"))
        self.click_element("xpath", self.nth_todo_item(num, "destroy"))

    def click_complete_all(self):
        """
        Clicks on the "Complete All" link that marks all ToDos as complete.
        :return: None
        """
        self.click_element("xpath", self.complete_all_checkbox)

    def click_clear_completed(self):
        """
        Clicks on the "Clear Completed" link that destroys all ToDos marked as "Complete"
        :return: None
        """
        self.click_element("xpath", self.clear_completed_button)

    def click_filter(self, name):
        """
        Clicks on a filter based on the display name specified.
        :param str name: String of display name/text of filter.
        :return: None
        """
        self.click_element("xpath", self.get_filter_link(name))

    def edit_todo(self, num, new_text):
        """
        Edits a ToDo item. Due to how the application handles the edit state, we must double click on a label and then type into an input.
        :param int num: The number of the ToDo item in question (starts at 1)
        :param str new_text: The text to replace the old text.
        :return: None
        """
        char_length = len(self.get_todo_text(1))
        self.double_click_element("xpath", self.nth_todo_item(1, "label"))
        self.type_backspace_into_element(
            "xpath", self.nth_todo_item(1), char_length)
        self.type_into_element_and_press_enter(
            new_text, "xpath", self.nth_todo_item(1))

    # Assertions
    def todo_list_is_present(self):
        """
        Determines if the ToDo list itself is present. This does not include the search box.
        :return" Boolean
        """
        return self.is_element_present("xpath", self.todo_list)

    def clear_completed_button_is_present(self):
        """
        Determines if the "Clear Completed" button is present in the DOM.
        :return: Boolean
        """
        return self.is_element_present("xpath", self.clear_completed_button)
