# Testing
In this article you will get a brief glimpse into how this project is tested.

## Types of Tests
All tests are located in `image-augmentation-service/tests`.
The following types of tests are encapsulated within their own subdirectories.
- `./tests/unit`
- `./tests/integration`
- `./tests/fuzz`
- `./tests/end-to-end`

Here is a brief description of the purpose of each.

### `./tests/unit`

Unit tests focus on the smallest, most isolated pieces of code, such as individual functions or methods.
They ensure that each component works correctly on its own, without relying on other parts of the system.
These tests are fast, simple, and form the foundation of our testing strategy. 

### `./tests/integration`

Integration tests verify that different parts of the application work together as intended.
For example, an integration test might check if the image processing module correctly communicates with the file storage service.
These tests are crucial for finding errors that occur at the interfaces between components.

### `./tests/fuzz`

Fuzz tests (or fuzzing) are a type of automated security testing where we bombard the application with invalid, unexpected, or random data as input.
The goal is to uncover bugs, crashes, or security vulnerabilities that might otherwise be missed.

### `./tests/end-to-end`
End-to-end (E2E) tests simulate a real user's workflow from start to finish.
For this service, an E2E test would involve uploading an image through the API, waiting for it to be augmented, and then verifying the final output.
These tests provide the highest confidence that the entire system is functioning correctly in a production-like environment.

## `/tests` Structure

Tests are structured using the project-parallel test structure.
This means the test directory mirrors the structure of the source code directory (image-augmentation-service/src).
This approach makes it easy to locate the tests corresponding to a specific piece of code.

Let us assume that the project has the following directory structure:
```terminaloutput
image-augmentation-service/
├── app/
│   ├── foo/
│   │   ├── __init__.py
│   │   └── wow.py
│   ├── bar/
│   │   ├── __init__.py
│   │   ├── golly.py
│   │   └── totally.py
│   └── main.py
└── tests/
```
Following the project-parallel structure, the tests directory would be organized like this:
```terminaloutput
tests/
├── unit/
│   ├── foo/
│   │   └── test_wow.py
│   └── bar/
│       ├── test_golly.py
│       └── test_totally.py
├── integration/
│   └── test_foo_makes_network_calls.py
└── end-to-end/
    └── test_full_user_signup_flow.py
```
This clear and predictable organization simplifies navigation and maintenance.


