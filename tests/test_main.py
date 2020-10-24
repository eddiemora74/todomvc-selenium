from pages.main import MainApp
import unittest
import pytest
from time import sleep


@pytest.mark.usefixtures("oneTimeSetup")
class TestToDo(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetup):
        self.todos = ["Clean room", "Make coffee",
                      "Exercise", "Walk dog", "Go grocery shopping"]
        self.app = MainApp(self.driver)

    @pytest.mark.run(order=1)
    def test_todo_list_not_visible(self):
        assert self.app.todo_list_is_present() == False
        sleep(1)

    @pytest.mark.run(order=2)
    def test_add_one_todo(self):
        self.app.add_todo(self.todos[0])
        assert self.app.todo_list_is_present() == True
        assert self.app.get_todo_text(1) == self.todos[0]
        assert self.app.get_item_count() == 1

    @pytest.mark.run(order=3)
    def test_add_second_todo(self):
        self.app.add_todo(self.todos[1])
        assert self.app.get_todo_text(2) == self.todos[1]
        assert self.app.get_item_count() == 2

    @pytest.mark.run(order=4)
    def test_complete_first_todo(self):
        self.app.click_complete_todo(1)
        assert self.app.get_item_count() == 1
        assert self.app.clear_completed_button_is_present() == True

    @pytest.mark.run(order=5)
    def test_uncheck_first_todo(self):
        self.app.click_complete_todo(1)
        assert self.app.get_item_count() == 2
        assert self.app.clear_completed_button_is_present() == False

    @pytest.mark.run(order=6)
    def test_complete_all_todos(self):
        self.app.click_complete_all()
        assert self.app.get_item_count() == 0
        assert self.app.get_list_size() == 2
        assert self.app.clear_completed_button_is_present() == True

    @pytest.mark.run(order=7)
    def test_add_third_todo(self):
        self.app.add_todo(self.todos[2])
        assert self.app.get_todo_text(3) == self.todos[2]
        assert self.app.get_item_count() == 1
        assert self.app.get_list_size() == 3

    @pytest.mark.run(order=8)
    def test_delete_first_todo(self):
        self.app.click_delete_todo(1)
        assert self.app.get_item_count() == 1
        assert self.app.get_todo_text(1) != self.todos[0]

    @pytest.mark.run(order=9)
    def test_view_active_filter(self):
        self.app.click_filter("Active")
        assert self.app.get_item_count() == 1
        assert self.app.get_list_size() == 1
        assert self.app.get_todo_text(1) == self.todos[2]

    @pytest.mark.run(order=10)
    def test_view_completed_filter(self):
        self.app.click_filter("Completed")
        assert self.app.get_item_count() == 1
        assert self.app.get_list_size() == 1
        assert self.app.get_todo_text(1) == self.todos[1]

    @pytest.mark.run(order=11)
    def test_add_fourth_todo(self):
        self.app.add_todo(self.todos[3])
        assert self.app.get_item_count() == 2
        assert self.app.get_list_size() == 1
        assert self.app.get_todo_text(1) == self.todos[1]

    @pytest.mark.run(order=12)
    def test_clear_completed_todos(self):
        self.app.click_clear_completed()
        assert self.app.todo_list_is_present() == True
        assert self.app.get_list_size() == 0
        assert self.app.get_item_count() == 2

    @pytest.mark.run(order=13)
    def test_edit_first_active_todo(self):
        self.app.click_filter("All")
        self.app.edit_todo(1, self.todos[4])
        assert self.app.get_todo_text(1) == self.todos[4]
        assert self.app.get_list_size() == 2
        assert self.app.get_item_count() == 2

    @pytest.mark.run(order=14)
    def test_refresh_page(self):
        self.driver.refresh()
        assert self.app.get_list_size() == 2
        assert self.app.get_item_count() == 2

    @pytest.mark.run(order=15)
    def test_complete_and_clear_all(self):
        self.app.click_complete_all()
        self.app.click_clear_completed()
        assert self.app.todo_list_is_present() == False


if __name__ == '__main__':
    unittest.main()
