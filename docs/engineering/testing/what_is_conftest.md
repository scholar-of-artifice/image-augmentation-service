# What is `conftest.py`?
In this article, you will learn about `conftest.py`.
This article is aimed at those who are new to using `pytest`.
If you are new to making data-centric applications with Python, then you may find this article useful as well.

`conftest.py`, is a special file used by `pytest` to share fixtures across multiple test files.
Think of it as a central place to put testing setup and teardown logic.

## What are Fixtures?
A fixture is just a function that `pytest` runs before//after the actual test functions.
You use fixtures to set up a predictable state or provide data for the tests.

For example, a fixture could:
- Create a temporary database connection.
- Spin up a test-specific database and populate it with initial data.
- Create an instance of a class that the test needs.
- Create a Client for testing the API.

Please note that there are also common pytest plugins and libraries which can also fulfill some of these roles.

## Why is this useful for SQLModel?

When testing an application that uses SQLModel, you usually need a database to test against.
However, you don't want to use your real production database for testing because your tests might delete or change data.

There are a few ways around this.
But the most common thing to do is speak to a specific `test` database that is defined in the `docker-compose`.
In short, `conftest.py` is the key to creating reusable, clean setup code for your tests.
This helps keep database instances clean and ensures tests are hermetic.

## Fixtures Explained in Depth 

### `engine`

```python
@pytest.fixture(scope="session")
def engine():
    """
        Creates a SQLAlchemy engine instance
    """
    return create_engine(str(settings.DATABASE_URL))
```
#### Purpose

This fixture has one simple and important job: `to create the database engine`.

##### What is an `engine`?

The `engine` is the starting point for any SQLAlchemy/SQLModel application.
It is an object that manages the lower level details such as:
- connecting to a specific database (like `PostgreSQL`)
- using a connection string (the `DATABASE_URL`).

It does not establish a connection right away.
It prepares a pool of connections to be used when needed.

##### `@pytest.fixture(scope="session")`
The scope argument tells `pytest` how often to create and destroy the fixture.

- `scope="function"` (the default):
The fixture is created at the start of each test function and destroyed at the end.
This is great for total isolation but can be slow if the setup is expensive.

- `scope="session"`:
The fixture is created only once when `pytest` starts the entire test run (the "`session`") and is destroyed after all tests have finished.

By setting `scope="session"`, I am saying, "`I only need one database engine for all my tests, so create it once at the beginning and let all the tests share it.`"
This is efficient because creating an engine is a relatively lightweight operation, and you don't need a new one for every single test.

### `setup_database`

```python
@pytest.fixture(scope="session")
def setup_database(engine):
    """
        Create and drop all tables once for the entire test session.
    """
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
```

#### Purpose

This fixture manages the database schema (i.e., the tables) for the entire test run.
It ensures the tests start with a fresh set of tables and leaves the database clean when finished.

##### Fixture Dependency: (`engine`)

Notice that this fixture takes engine as an argument.
Pytest automatically detects this and knows it must run the engine fixture first and pass its return value (the SQLAlchemy engine) into this `setup_database` fixture.
This is how fixtures connect and build on each other.

##### Setup and Teardown with `yield`

This fixture uses `yield`, which turns it into a setup/teardown function.
```python
SQLModel.metadata.create_all(engine)
```
This line connects to the database using the provided engine and creates all the tables defined by your SQLModel classes.
Because the fixture has `scope="session"`, this happens only once at the very beginning of your test session.

The `yield` keyword pauses the fixture. At this point, `pytest` goes and runs all of the tests.
```python
SQLModel.metadata.drop_all(engine)
```
Once all the tests in the session are complete, the code after yield is executed.
This line connects to the database again and drops all the tables it created, ensuring a clean state.

### `db_session`

```python
@pytest.fixture(scope="function")
def db_session(engine, setup_database):
    """
        --- FIXTURE FOR TESTING DATABASE MODELS ---
        Provides a SQLAlchemy session to the test database.
        This fixture will be created once per test function.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        if transaction.is_active:
            transaction.rollback()
        session.close()
        connection.close()
```

#### Purpose 
This fixture provides a clean, isolated database session for each individual test function.
It Ensures that tests do not interfere with one another.

#### Setup (Before Each Test)
Because this fixture has `scope="function"`, the following steps run before every single test that uses it.

##### `connection = engine.connect()`

It takes a single connection from the database engine connection pool.

##### `transaction = connection.begin()`

It starts a new transaction on that connection.
Every database operation performed during the test will be part of this single transaction.

##### `session = Session(bind=connection)`

It creates a SQLModel/SQLAlchemy session that is bound to this specific connection.
Ensures all session work goes through the transaction.

#### Execution (During Each Test)

##### `yield session`

Pauses the setup process and "yields" (hands over) the session object to the test function.
The test code then runs, using this session to interact with the database.

#### Cleanup (After Each Test)
The `finally` block guarantees that this code will run after your test is finished, regardless of whether it passed, failed, or raised an error.

##### `if transaction.is_active:`

This is a crucial safety check.
It asks, `Does the transaction we started still exist?`
In a normal test, the answer is yes.
In a test that caused a database error (like an `IntegrityError`), SQLAlchemy automatically kills the transaction, so the answer is no.
A complete test suite will need to handle both so we need this check here.
Otherwise, the test logic will need to handle things on its own... in every test function.

##### `transaction.rollback()`

If the transaction is still active, this line rolls it back.
It undoes any changes (`inserts`, `updates`, `deletes`) made during the test.
This is what guarantees that each test starts with a completely clean slate.
If the transaction is not active, this step is skipped, preventing warnings.

##### `session.close()`
The session object is closed to release its resources.

##### `connection.close()`
The database connection is returned to the engine's pool, ready to be used by the next test.

### `client`

```python
@pytest.fixture(scope="function")
def client(db_session):
    """
        --- FIXTURE FOR TESTING API ---
        A fixture that provides a TestClient with a transactional database session.
    """
    def override_get_session():
        """
            A dependency override that provides a session for one test.
        """
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    return
```

#### Purpose

This fixture is the bridge between the database tests and the API tests.
It provides a TestClient instance that allows you to make HTTP requests (e.g., GET, POST) to the FastAPI application, while ensuring that all database operations within that request use the isolated, transactional session provided by the `db_session` fixture.

#### Fixture Dependency: (`db_session`)

This fixture depends on `db_session`.
This means that for every test using `client`, `pytest` will first run the entire `db_session` fixture setup (creating a new connection and transaction) and pass the resulting session object to this fixture.

#### Setup (Before Each API Test)

##### `def override_get_session()`:

Inside the fixture, a temporary function `override_get_session` is defined.
This function is designed to replace the application's real `get_session` dependency.
When FastAPI calls this function, it simply yields the `db_session` that was created for the current test.

```python
app.dependency_overrides[get_session] = override_get_session
```

This is telling FastAPI:

> For the duration of this test, whenever any of the path operations ask for the `get_session` dependency, don't run the real one.
> Instead, run the `override_get_session` function.

This effectively hijacks the database connection logic and injects the test session, ensuring the API endpoint talks to the test transaction and not the real database.

#### Execution (During Each API Test)

```python
yield TestClient(app)
```

The fixture yields a `TestClient` instance configured with the dependency override.
The test function receives this client and can use it to make requests like `client.get("/users/")`.
When the code for the `/users/` endpoint runs and asks for a database session, it gets the special overridden one.

#### Cleanup (After Each API Test)

```python
app.dependency_overrides.clear()
```

After the test is finished, this line removes the override.
This is critical for ensuring that tests do not interfere with each other.
It cleans up the testing environment, restoring the application to its original state so that other tests (perhaps ones that don't need a database override) behave as expected.
