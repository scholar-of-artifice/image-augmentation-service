# User

This article is about the `User` table in the `transactions_db`.
In this article, you will learn:
- how the `User` table is structured
- the purpose of the different fields
- the `normal form` of this table

## Fields

This section describes each field and its purpose.

## `id`

This field is the primary key for the table, defined as a universally unique identifier (UUID).

### Constraints

- `Primary Key`: Uniquely identifies each row in the table.
- `Not Nullable`: Every user record must have an ID.
- `Indexed`: The database creates an index on this column to speed up lookups and joins from other tables that reference `user_id`.

### Justification
Using a UUID instead of a sequential integer is a security best practice.
It prevents bad actors from guessing user IDs and enumerating users.
It also simplifies merging data across different environments (e.g., development and production).

## `external_id`

This field is a string that stores the unique identifier from an external authentication provider (e.g., the sub claim in a JWT).

### Constraints

- `Unique`: Enforces a one-to-one relationship between an external identity and an internal user record. No two users can share the same `external_id`.
- `Not Nullable`: Every user must be linked to an external identity.
- `Indexed`: This is crucial for performance, as users will typically be looked up by this ID after authenticating.

### Justification
This field decouples the application's internal user management from the external authentication system, providing a stable link between the two.

## `created_at`

This field is a timezone-aware datetime that automatically records when a user record is first created.

### Constraints

- `Not Nullable`: A record must have a creation timestamp.
- `Default Value`: The application automatically sets this value to the current time in UTC `(datetime.now(timezone.utc)) `when a new user is inserted.

### Justification
Storing a creation timestamp is essential for auditing, tracking user sign-up metrics, and debugging.
Using a timezone-aware datetime stored in UTC is a best practice that prevents ambiguity.

## `updated_at`

This field is a timezone-aware datetime that automatically records when a user record was last modified.

### Constraints

- `Database-Managed Updates`: This field uses a database-level trigger `(onupdate=func.now())` to automatically update its value to the current timestamp whenever the row is changed.

### Justification
This provides a reliable and efficient way to track changes to user data for auditing, cache invalidation, and debugging purposes.
Offloading this logic to the database is more robust than handling it in the application code.

## Table Form Normalization
The User table is in `Boyce-Codd Normal Form` (BCNF).
Read ahead if you want to know more.
reference: https://en.wikipedia.org/wiki/Boyce–Codd_normal_form

### Analysis

Here is a quick analysis of the table and its normal form.

#### First Normal Form
A table is in 1NF if all its attributes are `atomic` and it has a `primary key`.

- Primary Key: The table has a primary key, `id`.
- Atomicity: Each column (`id`, `external_id`, `created_at`, `updated_at`) holds a single, indivisible value.
- There are no repeating groups or lists within a column.

#### Second Normal Form
A table is in 2NF if it is in 1NF and all non-key attributes are fully dependent on the entire primary key.
The primary key is `id`, which is a single column (not a composite key).

- When the primary key is a single column, there can be no partial dependencies.
- All non-key attributes (`external_id`, `created_at`, `updated_at`) are automatically fully dependent on the primary key id.

#### Third Normal Form
A table is in 3NF if it is in 2NF and has no transitive dependencies (where a non-key attribute depends on another non-key attribute).

Let's examine the non-key attributes:
- `external_id`: Depends only on id.
- `created_at`: Depends only on id.
- `updated_at`: Depends only on id.

No non-key attribute depends on another non-key attribute.
For example, `created_at` does not depend on `external_id`.
All attributes depend directly on the primary key.

#### Boyce-Codd Normal Form
A table is in BCNF if, for every functional dependency `X → Y`, `X` is a superkey (a set of attributes that can uniquely identify a row).

This table has two candidate keys (and therefore superkeys):
- `id` (the primary key).
- `external_id` (because it is marked as `unique=True`).

The functional dependencies are:
- `id → (external_id, created_at, updated_at)`. The determinant (`id`) is a superkey.
- `external_id → (id, created_at, updated_at)`. The determinant (`external_id`) is also a superkey.