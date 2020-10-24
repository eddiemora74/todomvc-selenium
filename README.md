# ToDoMVC + Vanilla Selenium

There are three main sections to the project:
1. Base
2. Pages
3. Test

## Base
This includes the base driver configurations.

## Pages
This is where the page logic lives (locators, actions methods, etc).

## Tests
This is where the test suite lives.

To run the example test, you would run the following from the root folder:
```bash
py.test -v tests/test_main.py --browser firefox --html=report.html
```
The -v flag is Verbose mode so you can see the output of the tests in the console.

The --browser flag is a custom flag added to choose which browser to run (currently only Firefox and Chrome)

The --html flag is the report generated from the results.
