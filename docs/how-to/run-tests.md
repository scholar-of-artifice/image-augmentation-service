# How to Run Tests
Tests in this project are written using `pytest`.

## run all `unit` and `integration` tests
From the root directory of this repository:
```terminaloutput
docker compose --profile test up --build --abort-on-container-exit
```

## run all `end-to-end` tests
From the root directory of this repository;
```terminaloutput
docker compose --profile endtoend up --build --abort-on-container-exit
```

## How can I get more detail?
link: https://docs.pytest.org/en/stable/how-to/output.html#verbosity
```terminaloutput
pytest --quiet          # quiet - less verbose - mode
pytest -q               # quiet - less verbose - mode (shortcut)
pytest -v               # increase verbosity, display individual test names
pytest -vv              # more verbose, display more details from the test output
pytest -vvv             # not a standard , but may be used for even more detail in certain setups
```


