# Transactions Database

The Transactions Database exists so that the system can track the status of a request to process an image.
It helps us figure out where the user's `original` image is and where the `processed` version is stored.
Essentially, it is a way of tracking our jobs and recovering rather than relying on processes to always finish (like a stateless system).

## Key Articles
- [User](user.md)
- [UnprocessedImage](unprocessed_image.md)
- [ProcessedImage](processed_image.md)
- [ProcessingJob](processing_job.md)

