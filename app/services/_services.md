# `/services`
By the end of this article, you will learn:
- What a `service layer` is
- Why the `service layer` exists
- How to reason about a `service layer`

## What is a `Services Layer`?

The `service layer` contains the core business logic.
It serves a distinct role which is outlined in the following headers.

### The `Services Layer` orchestrates operations

A `service layer` function uses internal library/application code in order to do some work.
For example, a `send_welcome_email_service` is a service function.
Theoretically it would :
- call a function to `fetch a user's details` from the `database`
- call a function to `create an email`
- call a function to `send the email`

These component functions would live in the `repository layer`.
The functions may even live in distinct `modules`.
However, the service layer uses them in order to accomplish the intended task.

### The `Services Layer` translates work into application logic

A service layer function is invoked by a web endpoint as an implementation detail.

The endpoint responds with `json` data and HTTP Error Codes (e.g. `200`, `404`, etc.).
In contrast, the service layer may raise errors or exceptions as its own internal types for the endpoint to reinterpret.

#### Example

```python
# endpoint.py

@router.get(
    path="/user/{user_id}",
    response_model=ResponseGetUser,
    status_code=status.HTTP_200_OK,
)
async def get_user_endpoint(
        user_id: uuid.UUID
) -> ResponseGetUser:
    try:
        # go get the data
        return get_user_service(
            user_id= user_id
        )
    except UserNotFound as e:
        # we got this specific custom error...
        # ... reinterpret as a 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
        

```

```python
# service.py

async def get_user_service(
        user_id: uuid.UUID
) -> ResponseGetUser:
    user_entry = get_user_from_database(user_id)
    # ...
    if not user_entry:
        # raise our own custom error for this condition
        raise UserNotFound(
            f"User with id '{user_id_to_delete}' not found."
        )
    # ...
    return ResponseGetUser(
        username: user_entry.username
    )

```


## Why this layer exists

### Testability 🧪

Easily test business logic without need for a real database.
Just mock the `repository layer` functions to return fake data.

### Reusability ♻️

The service layer functions are distinctly tied to the endpoints they serve.
However, the `repository layers` are reusable and open to be imported to other modules.

### Maintainability 🔧

If you decide to change your database from `PostgreSQL` to `Cassandra` (or indeed support more than one database),
you only need to change the code in the `repository` layer.

### Clarity 🧊

**(Personal opinion here)** The flow of data is much more clear.
A `request` goes into a `router`.
The `router` calls a `service`.
The `service` calls one or more `repository` layer functions.

### Ease of Debugging 🐛

A call stack is easier to reason about when the endpoint has a thin layer of abstraction to the backend logic.
The `service layer` makes an identifiable place to start debugging.
Internal functions can be treated as distinct stages of an algorithm.