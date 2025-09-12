# System Design
In this article, you will learn how this system is designed in order to meet its intended goals and fulfill its purpose.

It is worth stating the overall aims of the project here:

#### Purpose
`image-augmentation-service` is a micro-service which allows a client (human or machine) to send an image along with a request to process that image.
The client then receives information about where to get the newly processed image.

Here is the `high-level` view of how the system works.

![image](../../docs/assets/images/high_level_idea.png)

This simple architecture can work as a basic starting point.
However, there are important questions that a curious person will immediately ask such as:
- Where do the images go?
- How do I get my processed image?

Given a sufficiently small number of concurrent requests, any modest computer can potentially process 100 images/second.
But there is more to this system which will allow it to handle many more users.
This is *why* this document exists.

## What does the image processing?

## What are we storing?


