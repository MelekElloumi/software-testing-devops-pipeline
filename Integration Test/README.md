# Integration Testing 

- I wrote 20 test cases for 10 url routes of App4Test, from the Flask app in app4test.py.
- With the 17 unit tests, it becomes 37 tests in total.
- I used one fixture of session scope to create a test database for all the tests.
- I used one fixture of module scope to create the app and get its context.
- Each test contains 3 steps: 
    1. Given
    2. When
    3. Then
- I mainly tested the status code, title and alert messages of the directed response page.

### Test Execution:

![Imgur](https://i.imgur.com/YNp3wzk.png)

- The 37 tests have passed.

### Test Coverage:

![Imgur](https://i.imgur.com/qhMntzB.png)

- The test coverage is 99%.
- The uncovered code is the main function of app4test.py that isn't called when creating the app.
