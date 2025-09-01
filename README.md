# image-augmentation-service
This project is a microservice which can be used to produce augmented versions of image data. The basic idea is this:

![image](docs/assets/images/high_level_idea.png)

> A `client` sends a `request` to augment an `image`. This `image` is then processed `asychronously` by the `service`. The `service` sends back some information about how to retrieve the `augmented image`.

## What is `augmentation`?
`Augmentation` is the process of artificially expanding a dataset by creating modified versions of existing data. It is a technique used to increase the size and diversity of a dataset without collecting new data. This is often to improve generalization and robustness of a neural network or other statistical model.

## How can I learn more about this project?

I aim to write clear documentation. 
The documentation lives in `/docs`.

Here are some useful articles for gettings started:

- [How to try the application?](docs/how-to/try-the-application.md)
- [How to run tests?](docs/how-to/run-tests.md)

### 🧠 Want to know more about the `engineering`?
- [Storing Image Data](docs/engineering/image_storage/storing_images.md)
- [PostgreSQL Database Design](docs/engineering/transactions_database/transactions_database.md)
- [How tests are structured](docs/engineering/testing/_testing.md)
