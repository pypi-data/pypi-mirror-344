# FastAugment 🚀

One-command image augmentation for computer vision pipelines. Apply transformations with a single function call.

![PyPI version](https://img.shields.io/badge/pypi-v0.1.2-blue)
![Python versions](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)


## Features

- 🛠️ **Preset-based augmentations** - Choose between "simple" or "advanced" augmentation strategies
- 🖼️ **Supports multiple input types** - Works with image paths, numpy arrays, and PyTorch datasets
- ⚡ **Efficient processing** - Optimized OpenCV backend
- 📁 **Automatic saving** - Optionally save augmented images to directory

## Installation

```bash
pip install fast_augment
```

## Quick Start

### Basic Usage

```python
from fast_augment import FastAugment
import cv2

# Load an image
from fast_augment import FastAugment
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# Load an image black image
pixels = 255 * np.ones((512, 512, 3), dtype=np.uint8)
image = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize augmenter
augmenter = FastAugment(preset="advanced")

# Augment single image
augmented_image = augmenter.augment_image(image, n = 10)
for i in range(len(augmented_image)):
  cv2_imshow(augmented_image[i])

```

### Dataset Augmentation

```python
from torchvision.datasets import CIFAR10

# Load dataset
dataset = CIFAR10(root="./data", train=True)

# Augment entire dataset
augmenter = FastAugment(preset="advanced")
augmented_data = augmenter.augment_dataset(
    dataset=dataset,
    output_dir="./augmented_data",
    target_size=10000
)
```

## Presets

| Preset     | Transformations                          |
|------------|-----------------------------------------|
| `simple`   | Horizontal flips, rotations             |
| `advanced` | Adds cutout and brightness/contrast     |

## Advanced Configuration

Customize individual augmentation probabilities:

```python
# Coming in v1.1 (create feature request!)
```

## Documentation

Full API reference available at [fastaugment.readthedocs.io](https://fastaugment.readthedocs.io)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Aryan Patil - aryanator01@gmail.com
```

