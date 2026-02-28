# Image Preprocessing Module Documentation

## Overview

The `image_preprocessing.py` module provides a production-ready pipeline for preprocessing images for AI-based product recognition systems. It's designed to work seamlessly with deep learning frameworks like TensorFlow, PyTorch, and Keras.

## Features

✅ **Multi-Format Support**: JPG, PNG, WebP  
✅ **Automatic RGB Conversion**: Handles color space conversions automatically  
✅ **Noise Reduction**: Gaussian blur and median filtering options  
✅ **Image Enhancement**: Contrast and brightness adjustments  
✅ **Normalization**: Scales pixel values to [0, 1] range for neural networks  
✅ **Comprehensive Error Handling**: Detailed logging and exception handling  
✅ **Production-Ready**: Fully typed, documented, and tested  
✅ **Model Compatible**: Outputs compatible with ResNet, VGG, EfficientNet, etc.  

## Installation

### Prerequisites

```bash
pip install opencv-python pillow numpy pytest
```

### Add to your project

```bash
# Copy the module to your project
cp image_preprocessing.py your_project/
```

## Quick Start

### Basic Usage (One-liner)

```python
from image_preprocessing import preprocess_image

# Preprocess image for neural network
image = preprocess_image('path/to/image.jpg')
# Returns: numpy array with shape (224, 224, 3), dtype float32, values [0, 1]
```

### Step-by-Step Pipeline

```python
from image_preprocessing import (
    load_image,
    resize_image,
    reduce_noise,
    enhance_image,
    normalize_image
)

# Step 1: Load image
image = load_image('image.jpg')

# Step 2: Resize for model input
image = resize_image(image, size=(224, 224))

# Step 3: Reduce noise
image = reduce_noise(image, method='gaussian')

# Step 4: Enhance contrast
image = enhance_image(image, contrast_factor=1.2)

# Step 5: Normalize for neural network
image = normalize_image(image)
```

## API Reference

### 1. `load_image(image_path: Union[str, Path]) -> np.ndarray`

Load an image from disk and convert to RGB format.

**Parameters:**
- `image_path` (str or Path): Path to image file (JPG, PNG, or WebP)

**Returns:**
- `np.ndarray`: Image array with shape (height, width, 3), dtype uint8

**Supported Formats:** `.jpg`, `.jpeg`, `.png`, `.webp`

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If format unsupported or image corrupted

**Example:**
```python
>>> image = load_image('product.jpg')
>>> image.shape
(960, 1280, 3)
```

---

### 2. `resize_image(image: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray`

Resize image to fixed dimensions suitable for CNN models.

**Parameters:**
- `image`: Input RGB image array
- `size`: Target size as (height, width). Default: (224, 224)

**Returns:**
- `np.ndarray`: Resized image with specified dimensions

**Details:**
- Uses bilinear interpolation for quality
- Common sizes: 224x224 (ResNet/VGG), 256x256 (Inception), 299x299 (EfficientNet)

**Example:**
```python
>>> resized = resize_image(image, size=(256, 256))
>>> resized.shape
(256, 256, 3)
```

---

### 3. `reduce_noise(image: np.ndarray, method: str = 'gaussian', kernel_size: int = 5) -> np.ndarray`

Apply noise reduction using Gaussian blur or median filtering.

**Parameters:**
- `image`: Input RGB image
- `method`: 'gaussian' or 'median'. Default: 'gaussian'
- `kernel_size`: Kernel size (must be odd). Default: 5

**Returns:**
- `np.ndarray`: Denoised image

**Method Comparison:**
| Method | Speed | Use Case |
|--------|-------|----------|
| Gaussian | Fast | General noise, mild smoothing |
| Median | Slower | Salt-and-pepper noise |

**Example:**
```python
# Fast noise reduction
>>> denoised = reduce_noise(image, method='gaussian', kernel_size=5)

# Strong noise reduction
>>> denoised_strong = reduce_noise(image, method='median', kernel_size=7)
```

---

### 4. `normalize_image(image: np.ndarray) -> np.ndarray`

Normalize pixel values to [0.0, 1.0] range for neural network input.

**Parameters:**
- `image`: Input image with values [0, 255]

**Returns:**
- `np.ndarray`: Normalized image as float32 with values [0.0, 1.0]

**Details:**
- Converts uint8 → float32
- Essential for neural network convergence
- Improves numerical stability

**Example:**
```python
>>> normalized = normalize_image(image)
>>> normalized.dtype
dtype('float32')
>>> normalized.min(), normalized.max()
(0.0, 1.0)
```

---

### 5. `enhance_image(image: np.ndarray, brightness_factor: float = 1.0, contrast_factor: float = 1.2) -> np.ndarray`

Apply contrast enhancement and brightness correction.

**Parameters:**
- `image`: Input image (uint8 or float32)
- `brightness_factor`: Brightness adjustment. 1.0 = no change. Default: 1.0
- `contrast_factor`: Contrast adjustment. 1.0 = no change. Default: 1.2

**Returns:**
- `np.ndarray`: Enhanced image (same dtype as input)

**Factor Guide:**
- `factor = 1.0`: No change
- `factor > 1.0`: Increase effect
- `0 < factor < 1.0`: Decrease effect

**Example:**
```python
# Increase contrast
>>> enhanced = enhance_image(image, contrast_factor=1.5)

# Increase brightness and contrast
>>> enhanced = enhance_image(image, brightness_factor=1.1, contrast_factor=1.3)
```

---

### 6. `preprocess_image(image_path: Union[str, Path], target_size: Tuple[int, int] = (224, 224), normalize: bool = True, enhance: bool = True) -> np.ndarray`

Complete preprocessing pipeline. Main function for most use cases.

**Parameters:**
- `image_path`: Path to image file
- `target_size`: Target dimensions as (height, width). Default: (224, 224)
- `normalize`: Whether to normalize to [0, 1]. Default: True
- `enhance`: Whether to apply enhancement. Default: True

**Returns:**
- `np.ndarray`: Preprocessed float32 image ready for model input

**Pipeline Steps:**
1. Load image (JPG/PNG/WebP → RGB)
2. Resize to target dimensions
3. Reduce noise (Gaussian blur)
4. Enhance (improve contrast)
5. Normalize to [0, 1]

**Output Guarantees:**
- Shape: (height, width, 3)
- dtype: float32 (if normalize=True)
- Values: [0.0, 1.0] (if normalize=True)
- No NaN or Inf values

**Example:**
```python
# Default preprocessing for ResNet
>>> image = preprocess_image('image.jpg')

# Custom size for EfficientNet
>>> image = preprocess_image('image.jpg', target_size=(256, 256))

# Without enhancement
>>> image = preprocess_image('image.jpg', enhance=False)
```

---

## Real-World Usage Examples

### TensorFlow/Keras Integration

```python
import tensorflow as tf
import numpy as np
from image_preprocessing import preprocess_image

# Preprocess single image
image = preprocess_image('product.jpg', target_size=(224, 224))

# Add batch dimension
image_batch = np.expand_dims(image, axis=0)

# Load pre-trained model
model = tf.keras.applications.ResNet50(weights='imagenet')

# Make prediction
predictions = model.predict(image_batch)
labels = tf.keras.applications.resnet50.decode_predictions(predictions)
```

### PyTorch Integration

```python
import torch
from torchvision import models
from image_preprocessing import preprocess_image

# Preprocess image
image = preprocess_image('product.jpg', target_size=(224, 224))

# Convert to tensor and reshape (batch_size, channels, height, width)
image_tensor = torch.from_numpy(image).unsqueeze(0).permute(0, 3, 1, 2)

# Load model
model = models.resnet50(pretrained=True)
model.eval()

# Inference
with torch.no_grad():
    output = model(image_tensor)
```

### Batch Processing

```python
import numpy as np
from image_preprocessing import preprocess_image

def preprocess_batch(image_paths, batch_size=32):
    """Preprocess multiple images into batches"""
    batch = []
    
    for img_path in image_paths:
        try:
            image = preprocess_image(img_path)
            batch.append(image)
            
            # Process in chunks
            if len(batch) == batch_size:
                yield np.array(batch)
                batch = []
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    # Yield remaining images
    if batch:
        yield np.array(batch)

# Usage
for batch in preprocess_batch(image_paths, batch_size=32):
    # batch shape: (32, 224, 224, 3)
    predictions = model.predict(batch)
```

### Production-Ready Error Handling

```python
from image_preprocessing import preprocess_image
import logging

logger = logging.getLogger(__name__)

def safe_preprocess(image_path, target_size=(224, 224)):
    """Preprocess with comprehensive error handling"""
    try:
        logger.info(f"Processing: {image_path}")
        image = preprocess_image(image_path, target_size=target_size)
        logger.info(f"Successfully processed image: {image.shape}")
        return image
    
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return None
    
    except ValueError as e:
        logger.error(f"Invalid image format or corrupted: {e}")
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

---

## Testing

The module includes 55 comprehensive unit tests using pytest.

### Run Tests

```bash
pytest test_image_preprocessing.py -v
```

### Test Coverage

- ✅ Valid image formats (JPG, PNG, WebP)
- ✅ Invalid file handling
- ✅ Resize output shape verification
- ✅ Normalization range validation
- ✅ RGB conversion verification
- ✅ Corrupted image handling
- ✅ Edge cases (very large/small images)
- ✅ Integration tests
- ✅ Error handling

### Example: Running Specific Test

```bash
# Run only TestLoadImage tests
pytest test_image_preprocessing.py::TestLoadImage -v

# Run with coverage
pytest test_image_preprocessing.py --cov=image_preprocessing
```

---

## Performance Considerations

### Default Settings
- **Resize Method**: Bilinear interpolation (fast, good quality)
- **Noise Reduction**: Gaussian blur with kernel size 5
- **Target Size**: 224x224 (ResNet standard)
- **Processing Time**: ~50-100ms per image (CPU)

### Optimization Tips

```python
# For speed: Skip enhancement
image = preprocess_image(path, enhance=False)

# For quality: Use median denoising
from image_preprocessing import load_image, resize_image, reduce_noise, normalize_image
image = load_image(path)
image = resize_image(image)
image = reduce_noise(image, method='median', kernel_size=7)  # Slower but better
image = normalize_image(image)

# For GPU acceleration: Use OpenCV's GPU functions (requires CUDA)
# (Note: Current implementation uses CPU-only OpenCV)
```

---

## Troubleshooting

### Common Issues

**Q: "Unsupported image format" error**
```python
# Solution: Convert image to supported format
# Supported: JPG, PNG, WebP
# Use PIL to convert
from PIL import Image
img = Image.open('image.bmp')
img.save('image.jpg')
```

**Q: Output values not in [0, 1] range**
```python
# Solution: Ensure normalize=True
image = preprocess_image(path, normalize=True)
```

**Q: Image looks distorted after resize**
```python
# Solution: Adjust target size to match your model
# Check model's expected input size
image = preprocess_image(path, target_size=(256, 256))
```

---

## Requirements

- Python 3.7+
- opencv-python>=4.5.0
- Pillow>=8.0
- NumPy>=1.19.0
- pytest>=7.0 (for testing)

## Files

- `image_preprocessing.py` - Main module
- `test_image_preprocessing.py` - Test suite (55 tests)
- `example_usage.py` - Usage examples
- `IMAGE_PREPROCESSING_README.md` - This file

## License

Production-ready implementation for AI product recognition systems.

## Support

For issues or questions:
1. Check module docstrings: `help(function_name)`
2. Review test cases in `test_image_preprocessing.py`
3. See examples in `example_usage.py`
