`# Unprocessed Image

This article is about the `UnprocessedImage` table in the `transactions_db`.
In this article, you will learn:
- how the `UnprocessedImage` table is structured
- the purpose of the different fields
- the `normal form` of this table

## Fields

This section describes each field and its purpose.

### `id`

This field is the primary key for the table, defined as a universally unique identifier (`UUID`).

#### Constraints:

- `Primary Key`: Uniquely identifies each unprocessed image record.
- `Not Nullable`: Every image record must have an ID.
- `Indexed`: Speeds up direct lookups and joins from related tables.

#### Justification:
A UUID is used to provide a unique, non-sequential identifier for each image, preventing enumeration and making it easier to manage records across different systems.

### `original_filename`

This field is a string that stores the original filename of the image as it was uploaded by the user (e.g., "my-vacation-photo.png").

#### Constraints:

- `Not Nullable`: The original filename must be recorded.
- `Length`: Must be between 1 and 255 characters.

#### Justification:
This provides a human-readable reference to the file and preserves the original context of the upload for display or tracking purposes.

### `storage_filename`

This field is a string containing the new, unique filename assigned to the image when it is saved in the backend storage system (like a cloud bucket).

#### Constraints:
- `Unique`: Guarantees that no two images in the storage system can have the same filename, preventing collisions. 🪨
- `Not Nullable`: Every image record must have a corresponding file in storage.

#### Justification:
Using a system-generated unique filename is a critical security and design practice. It avoids issues with special characters, path traversal attacks, and overwriting files that might arise from using user-supplied filenames directly.

### `created_at`

This field is a timezone-aware datetime that automatically records when the image record was created.

#### Constraints:

- `Not Nullable`: Every record must have a creation timestamp.
- `Default Value`: The application automatically sets this value to the current time in UTC upon insertion.
- `Justification`: This timestamp is essential for auditing, tracking upload volume, and implementing data lifecycle policies (e.g., deleting unprocessed images after a certain time).

### `user_id`

This field is a foreign key (`UUID`) that links the image to the user who uploaded it.

#### Constraints:

- `Foreign Key`: It must correspond to a valid id in the User table.
- `Not Nullable`: An image cannot exist without being associated with a user.
- `Indexed`: The database creates an index to significantly speed up queries that fetch all images belonging to a specific user.

#### Justification:
This creates the fundamental relationship between a user and their data, ensuring data ownership and enabling user-specific data retrieval.

## Table Form Normalization
The `UnprocessedImage` table is in `Boyce-Codd Normal Form` (BCNF).
Read ahead if you want to know more.
reference: https://en.wikipedia.org/wiki/Boyce–Codd_normal_form

### Analysis

Here is a quick analysis of the table and its normal form.

#### First Normal Form (1NF)

A table is in 1NF if it has a primary key and all attributes are atomic.

- `Primary Key`: The table has a primary key, id.
- `Atomicity`: Each column (id, original_filename, storage_filename, created_at, user_id) holds a single, indivisible value.

#### Second Normal Form (2NF)

A table is in 2NF if it is in 1NF and all non-key attributes depend on the entire primary key.

Since the primary key (`id`) is a single column (not composite), there can be no partial dependencies. The table is therefore automatically in 2NF.

#### Third Normal Form (3NF)

A table is in 3NF if it is in 2NF and has no transitive dependencies (where a non-key attribute depends on another non-key attribute).

All non-key attributes (`original_filename`, `storage_filename`, `created_at`, `user_id`) depend directly and only on the primary key id. No non-key attribute depends on another. Therefore, the table is in `3NF`.

#### Boyce-Codd Normal Form (BCNF)

A table is in `BCNF` if for every functional dependency `X → Y, X` is a superkey.

This table has two candidate keys (and therefore superkeys):

- `id` (the primary key)
- `storage_filename` (due to its unique constraint)

The functional dependencies are:

- `id → (original_filename, storage_filename, created_at, user_id)`
- `storage_filename → (id, original_filename, created_at, user_id)`

In both cases, the determinant of the dependency (`id` and `storage_filename`) is a superkey. Therefore, the table satisfies `BCNF`.