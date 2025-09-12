# Processing Job

This article is about the `ProcessingJob` table in the `transactions_db`. In this article, you will learn:
- how the `ProcessingJob` table is structured
- the purpose of the different fields
- the `normal form` of this table

***
## Fields

This section describes each field and its purpose.

### `id`

This field is the `primary key` for the table, defined as a universally unique identifier (`UUID`).

#### Constraints:
 - `Primary Key`: Uniquely identifies each processing job record.
 - `Not Nullable`: Every record must have an ID.
 - `Indexed`: Speeds up direct lookups and joins.

#### Justification:
A `UUID` provides a unique, non-sequential identifier, which is a best practice for security and data management, especially for referencing jobs asynchronously.

### `upload_request_body`

This field stores the original request parameters for the job as a `JSONB` object.

#### Constraints:
 - `JSONB` data type: Allows for storing complex, nested JSON data efficiently.
 - `Not Nullable`: A job must have a defined set of processing instructions.

#### Justification:
This field provides a complete record of what was requested, which is essential for auditing, debugging failed jobs, and re-running tasks with the exact same parameters.

### `job_status`

This field is an `Enum` that tracks the current state of the processing job (e.g., PENDING, SUCCESS, FAILED).

#### Constraints:
 - `Enum`: The value must be one of the predefined members of the `JobStatus` enum.
 - `Not Nullable`: A job must always have a status.
 - `Default Value`: Automatically set to `PENDING` when a new job is created.

#### Justification:
This acts as a state machine for the job, allowing workers and clients to monitor its progress and determine the outcome.

### `requested_at`

This is a timezone-aware `datetime` that automatically records when the job was created.

#### Constraints:
 - `Not Nullable`: Every job must have a request timestamp.
 - `Default Value`: The application automatically sets this to the current time in UTC upon insertion.

#### Justification:
This timestamp marks the beginning of the job's lifecycle and is used for tracking queue times and overall job duration.

### `started_at`

This is a nullable, timezone-aware `datetime` that records when the job's execution began.

#### Constraints:
 - `Nullable`: This field is `NULL` until a worker process picks up the job and begins execution.

#### Justification:
This allows for precise measurement of the job's processing time, separate from the time it spent waiting in the queue.

### `completed_at`

This is a nullable, timezone-aware `datetime` that records when the job's execution finished.

#### Constraints:
 - `Nullable`: This field is `NULL` until the job has finished, either successfully or with an error.

#### Justification:
This timestamp marks the end of the job's active processing, completing the data needed to calculate total execution time and throughput.

### `unprocessed_image_id`

This field is a `foreign key` (`UUID`) that links the job to its source image.

#### Constraints:
 - `Foreign Key`: Must correspond to a valid `id` in the `UnprocessedImage` table.
 - `Not Nullable`: A processing job must always have a source image to work on.

#### Justification:
This creates the mandatory link between the processing task and its input data.

### `processed_image_id`

This is a nullable `foreign key` (`UUID`) that links the job to its resulting output image.

#### Constraints:
 - `Foreign Key`: If not `NULL`, it must correspond to a valid `id` in the `ProcessedImage` table.
 - `Nullable`: The field remains `NULL` while the job is pending or running. It is only populated upon successful completion.

#### Justification:
This creates an optional link between the job and its output. Keeping it nullable correctly models the reality that a job may not have a result yet, or may have failed and will never have one.

***
## Table Form Normalization
The `ProcessingJob` table is in `First Normal Form (1NF)` but given the constraints of use may be considered `BCNF`.

It is important to recognize the design trade-off made by using the `JSONB` column for `upload_request_body`.
While the table itself is normalized, the data within the `JSON` field is inherently `denormalized`.
If the request body had a consistent, complex structure that needed to be queried or updated frequently, a more normalized approach would be to break it out into separate, related tables.
For storing a flexible, unstructured request payload, `JSONB` is an excellent and practical choice.

For the purposes of this application, we need to store `upload_request_body` because we want to know (with fidelity) what the request was.
We could just as easily handle it as a `string` but it is more correct and practical to handle it as JSON.
If we ignore this or believed it to be a string, we would find this table conforms to `BCNF`.

The following explains why.

### Analysis

Here is a quick analysis of the table and its normal form.
This table is in `1NF`.

In a purely academic and traditional sense, the presence of the `JSONB` column means the table is only in First Normal Form (1NF).

#### First Normal Form (1NF)
The table is in 1NF because it has a primary key (`id`) and all its attributes (including `JSONB`) are atomic from the database's perspective.

#### Second Normal Form (2NF)
The table is in 2NF because it is in 1NF and has no partial dependencies, as its primary key (`id`) is a single column.

#### Third Normal Form (3NF)
The table is in 3NF because it has no transitive dependencies. All non-key attributes describe the job itself and depend directly and only on the primary key `id`. For example, `completed_at` does not depend on `started_at`; they are both independent facts about the job.

#### Boyce-Codd Normal Form (BCNF)
A table is in BCNF if for every functional dependency, the determinant is a superkey.

- The only candidate key (and therefore superkey) in this table is `id`.
- All functional dependencies (e.g., `id → job_status`) have `id` as the determinant.
- Since the determinant is always a superkey, the table satisfies BCNF.

The table adheres to 3NF and BCNF (a stricter version of 3NF, which this table also satisfies as its only key is the primary key).
