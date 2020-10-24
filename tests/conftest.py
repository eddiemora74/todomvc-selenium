import pytest
from selenium import webdriver


@pytest.yield_fixture(scope="class")
def oneTimeSetup(request, browser):
    """
    Sets base parameters and driver instance.
    """
    app_url = "http://todomvc.com/examples/react/#/"
    driver = webdriver.Firefox() if browser == "firefox" else webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()
    driver.get(app_url)

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()


def pytest_addoption(parser):
    """
    Creates the browser flag option when running pytest in command line.
    """
    parser.addoption("--browser")


@pytest.fixture(scope="class")
def browser(request):
    """
    Gets the browser option value from the command line.
    """
    return request.config.getoption("--browser")
