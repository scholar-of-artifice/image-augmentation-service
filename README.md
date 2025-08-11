# image-augmentation-service
This project is a microservice which can be used to produce augmented versions of image data. The basic idea is this:

> A `client` sends an `image` along with a `request` to augment the image. This `image` is then processed `asychronously`.

## What is `augmentation`?
`Augmentation` is the process of artificially expanding a dataset by creating modified versions of existing data. It is a technique used to increase the size and diversity of a dataset without collecting new data. This is often to improve generalization and robustness of a neural network or other statistical model.