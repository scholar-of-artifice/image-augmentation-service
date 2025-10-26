# Augmentations Illustrated

This article aims to provide an illustration for all of the basic transformations that can be done by this application.

Here are the original images used in these illustrations.
<figure>
    <img src="tests/data/colour-scribbles-256x256.png"/>
    <figcaption>The original image.</figcaption>
</figure>

TODO: might upload another image

## `brighten`

### Example

<pre>
BrightenArguments(
    processing='brighten',
    amount=30
)
</pre>
<figure>
    <img src="https://github.com/scholar-of-artifice/image-augmentation-service/blob/6fa4311e88517b76f2958e6fcbddc1e739a6cd1c/docs/assets/images/examples/brighten.png"/>
    <figcaption>A brightened version of the image.</figcaption>
</figure>

## `channel_swap`

### Example

<pre>
ChannelSwapArguments(
    processing='channel_swap',
    a='r',
    b='b'
)
</pre>
<figure>
    <img src="docs/assets/images/examples/channel-swap.png"/>
    <figcaption>A version of the image with `R` and `B` channels swapped.</figcaption>
</figure>

## `cutout`

### Example
<pre>
CutoutArguments(
    processing='cutout',
    amount=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/cutout.png"/>
    <figcaption>A version with a region cutout (or obscured) with noise.</figcaption>
</figure>

## `darken`

### Example
<pre>
DarkenArguments(
    processing='darken',
    amount=30
)
</pre>
<figure>
    <img src="docs/assets/images/examples/darken.png"/>
    <figcaption>A darkened version of the image.</figcaption>
</figure>

## `edge-enhanced`

### Example
<pre>
EdgeFilterArguments(
    processing='edge_filter',
    image_type='edge_enhanced'
)
</pre>
<figure>
    <img src="docs/assets/images/examples/edge-enhanced.png"/>
    <figcaption>An edge enhanced version of the image.</figcaption>
</figure>

## `flip`

### Example
<pre>
FlipArguments(
    processing='flip',
    axis='y'
)
</pre>
<figure>
    <img src="docs/assets/images/examples/flip.png"/>
    <figcaption>A version of the image that has been flipped along the `y-axis`.</figcaption>
</figure>

## `gaussian_blur`

### Example
<pre>
GaussianBlurArguments(
    processing='gaussian_blur',
    amount=100
)
</pre>
<figure>
    <img src="docs/assets/images/examples/gaussian-blur.png"/>
    <figcaption>A blurred version of the image using Gaussian Blur.</figcaption>
</figure>

## `invert`

### Example
<pre>
InvertArguments(
    processing='invert'
)
</pre>
<figure>
    <img src="docs/assets/images/examples/invert.png"/>
    <figcaption>A colour/channel inverted version of the image.</figcaption>
</figure>

## `max_filter`

### Example
<pre>
MaxFilterArguments(
    processing='max_filter',
    size=5
)
</pre>
<figure>
    <img src="docs/assets/images/examples/max-filter.png"/>
    <figcaption>A lowered quality version of the image which uses the maximum values in a specific area.</figcaption>
</figure>

## `min_filter`

### Example
<pre>
MinFilterArguments(
    processing='min_filter',
    size=5
)
</pre>
<figure>
    <img src="docs/assets/images/examples/min-filter.png"/>
    <figcaption>A lowered quality version of the image which uses the minimum values in a specific area.</figcaption>
</figure>

## `mute_channel`

### Example
<pre>
MuteChannelArguments(
    processing='mute_channel',
    channel='g'
)
</pre>
<figure>
    <img src="docs/assets/images/examples/mute-channel.png"/>
    <figcaption>A version of the image with the `G` channel muted.</figcaption>
</figure>

## `pepper_noise`

### Example
<pre>
PepperNoiseArguments(
    processing='pepper_noise',
    amount=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/pepper-noise.png"/>
    <figcaption>A noised version of the image with random black pixel replacements.</figcaption>
</figure>

## `percentile_filter`

### Example
<pre>
PercentileFilterArguments(
    processing='percentile_filter',
    percentile=50,
    size=5
)
</pre>
<figure>
    <img src="docs/assets/images/examples/percentile-filter.png"/>
    <figcaption>A lowered quality version of the image which uses a percentile value in a specific area.</figcaption>
</figure>

## `rainbow_noise`

### Example

<pre>
RainbowNoiseArguments(
    processing='rainbow_noise',
    amount=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/rainbow-noise.png"/>
    <figcaption>A noised version of the image with random pixel replacements.</figcaption>
</figure>

## `rotate`

### Example
<pre>
RotateArguments(
    processing='rotate',
    angle=30
)
</pre>
<figure>
    <img src="docs/assets/images/examples/rotate.png"/>
    <figcaption>A rotated version of the image.</figcaption>
</figure>

## `salt_noise`

### Example
<pre>
SaltNoiseArguments(
    processing='salt_noise',
    amount=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/salt-noise.png"/>
    <figcaption>A noised version of the image with random white pixel replacements.</figcaption>
</figure>

## `shift`

### Example
<pre>
ShiftArguments(
    processing='shift',
    direction='left',
    distance=128
)
</pre>
<figure>
    <img src="docs/assets/images/examples/shift.png"/>
    <figcaption>A shifted/translated version of the image.</figcaption>
</figure>

## `tint`

### Example
<pre>
TintArguments(
    processing='tint',
    channel='b',
    amount=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/tint.png"/>
    <figcaption>A blue tinted version of the image.</figcaption>
</figure>

## `uniform_blur`

### Example
<pre>
UniformBlurArguments(
    processing='uniform_blur',
    size=33
)
</pre>
<figure>
    <img src="docs/assets/images/examples/uniform-blur.png"/>
    <figcaption>A blurred version of the image using uniform blur.</figcaption>
</figure>

## `zoom`

### Example
<pre> 
ZoomArguments(
    processing='zoom',
    amount=50
)
</pre>
<figure>
    <img src="docs/assets/images/examples/zoom.png"/>
    <figcaption>A random zoom into the image.</figcaption>
</figure>
