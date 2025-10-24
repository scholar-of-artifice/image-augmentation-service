# Augmentations Illustrated

This article aims to provide an illustration for all of the basic transformations that can be done by this application.

Here are the original images used in these illustrations.
<figure>
    <img src="tests/data/colour-scribbles-256x256.png"/>
    <figcaption>The original image.</figcaption>
</figure>

TODO: might upload another image

## `brighten`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/brighten.png"/>
    <figcaption>A brightened version of the image.</figcaption>
</figure>

## `channel_swap`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/channel-swap.png"/>
    <figcaption>A version of the image with `R` and `B` channels swapped.</figcaption>
</figure>

## `cutout`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/cutout.png"/>
    <figcaption>A version with a region cutout (or obscured) with noise.</figcaption>
</figure>

## `darken`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/darken.png"/>
    <figcaption>A darkened version of the image.</figcaption>
</figure>

## `edge-enhanced`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/edge-enhanced.png"/>
    <figcaption>An edge enhanced version of the image.</figcaption>
</figure>

## `flip`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/flip.png"/>
    <figcaption>A version of the image that has been flipped along the `y-axis`.</figcaption>
</figure>

## `gaussian_blur`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/gaussian-blur.png"/>
    <figcaption>A blurred version of the image using Gaussian Blur.</figcaption>
</figure>

## `invert`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/invert.png"/>
    <figcaption>A colour/channel inverted version of the image.</figcaption>
</figure>

## `max_filter`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/max-filter.png"/>
    <figcaption>A lowered quality version of the image which uses the maximum values in a specific area.</figcaption>
</figure>

## `min_filter`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/min-filter.png"/>
    <figcaption>A lowered quality version of the image which uses the minimum values in a specific area.</figcaption>
</figure>

## `mute_channel`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/mute-channel.png"/>
    <figcaption>A version of the image with the `G` channel muted.</figcaption>
</figure>

## `pepper_noise`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/pepper-noise.png"/>
    <figcaption>A noised version of the image with random black pixel replacements.</figcaption>
</figure>

## `percentile_filter`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/percentile-filter.png"/>
    <figcaption>A lowered quality version of the image which uses a percentile value in a specific area.</figcaption>
</figure>

## `rainbow_noise`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/rainbow-noise.png"/>
    <figcaption>A noised version of the image with random pixel replacements.</figcaption>
</figure>

## `rotate`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/rotate.png"/>
    <figcaption>A rotated version of the image.</figcaption>
</figure>

## `salt_noise`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/salt-noise.png"/>
    <figcaption>A noised version of the image with random white pixel replacements.</figcaption>
</figure>

## `shift`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/shift.png"/>
    <figcaption>A shifted/translated version of the image.</figcaption>
</figure>

## `tint`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/tint.png"/>
    <figcaption>A blue tinted version of the image.</figcaption>
</figure>

## `uniform_blur`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/uniform-blur.png"/>
    <figcaption>A blurred version of the image using uniform blur.</figcaption>
</figure>

## `zoom`
### Model
### Example
<figure>
    <img src="docs/assets/images/examples/zoom.png"/>
    <figcaption>A random zoom into the image.</figcaption>
</figure>