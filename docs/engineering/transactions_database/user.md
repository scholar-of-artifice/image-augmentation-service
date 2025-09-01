# User

This article is about the `User` table in the `transactions_db`.
In this article, you will learn:
- how the `User` table is structured
- the purpose of the different fields
- the `normal form` of this table

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