"""
Usage Examples for Image Preprocessing Module

This file demonstrates various ways to use the image_preprocessing module
for preparing images for deep learning models.
"""

from image_preprocessing import (
    load_image,
    resize_image,
    reduce_noise,
    normalize_image,
    enhance_image,
    preprocess_image
)
import numpy as np


def example_1_basic_preprocessing():
    """
    Example 1: Basic preprocessing with default settings
    
    This is the simplest way to preprocess an image for a neural network.
    Perfect for quick prototyping.
    """
    print("=" * 60)
    print("Example 1: Basic Preprocessing (One-Line Solution)")
    print("=" * 60)
    
    # Single line preprocessing - suitable for models like ResNet, VGG
    image = preprocess_image('path/to/image.jpg')
    
    print(f"Output shape: {image.shape}")
    print(f"Output dtype: {image.dtype}")
    print(f"Value range: [{image.min():.4f}, {image.max():.4f}]")
    print()


def example_2_custom_preprocessing():
    """
    Example 2: Custom preprocessing with specific parameters
    
    Use this when you need more control over the preprocessing steps.
    """
    print("=" * 60)
    print("Example 2: Custom Preprocessing with Specific Sizes")
    print("=" * 60)
    
    # Preprocess for EfficientNet model (requires different input size)
    image = preprocess_image(
        'path/to/image.jpg',
        target_size=(256, 256),  # EfficientNet requires larger input
        normalize=True,
        enhance=True
    )
    
    print(f"Output shape: {image.shape}")
    print(f"Ready for EfficientNet: {image.shape == (256, 256, 3)}")
    print()


def example_3_step_by_step():
    """
    Example 3: Step-by-step preprocessing with custom options
    
    Use this for maximum control and debugging each step.
    """
    print("=" * 60)
    print("Example 3: Step-by-Step Preprocessing")
    print("=" * 60)
    
    # Step 1: Load image
    image = load_image('path/to/image.jpg')
    print(f"Step 1 - Loaded: {image.shape}, dtype: {image.dtype}")
    
    # Step 2: Resize
    image = resize_image(image, size=(224, 224))
    print(f"Step 2 - Resized: {image.shape}")
    
    # Step 3: Denoise (using median filter for stronger denoising)
    image = reduce_noise(image, method='median', kernel_size=5)
    print(f"Step 3 - Denoised: {image.shape}")
    
    # Step 4: Enhance contrast significantly
    image = enhance_image(image, brightness_factor=1.0, contrast_factor=1.5)
    print(f"Step 4 - Enhanced: {image.shape}")
    
    # Step 5: Normalize
    image = normalize_image(image)
    print(f"Step 5 - Normalized: {image.dtype}, range: [{image.min():.4f}, {image.max():.4f}]")
    
    print()


def example_4_batch_processing():
    """
    Example 4: Batch processing multiple images
    
    Process multiple images for training a neural network.
    """
    print("=" * 60)
    print("Example 4: Batch Processing Multiple Images")
    print("=" * 60)
    
    image_paths = [
        'path/to/image1.jpg',
        'path/to/image2.jpg',
        'path/to/image3.jpg',
    ]
    
    batch = []
    for img_path in image_paths:
        # Note: Wrap in try-except for production code
        processed_image = preprocess_image(img_path, target_size=(224, 224))
        batch.append(processed_image)
    
    # Convert to numpy array for model input
    batch_array = np.array(batch)
    
    print(f"Batch shape: {batch_array.shape}")  # (num_images, 224, 224, 3)
    print(f"Batch dtype: {batch_array.dtype}")  # float32
    print()


def example_5_different_model_sizes():
    """
    Example 5: Preprocess for different model architectures
    
    Different neural network architectures may require different input sizes.
    """
    print("=" * 60)
    print("Example 5: Preprocessing for Different Models")
    print("=" * 60)
    
    image_path = 'path/to/image.jpg'
    
    # ResNet (224x224)
    resnet_input = preprocess_image(image_path, target_size=(224, 224))
    print(f"ResNet input shape: {resnet_input.shape}")
    
    # Inception/EfficientNet (256x256 or 299x299)
    inception_input = preprocess_image(image_path, target_size=(299, 299))
    print(f"Inception input shape: {inception_input.shape}")
    
    # VGG (224x224 or 256x256)
    vgg_input = preprocess_image(image_path, target_size=(224, 224))
    print(f"VGG input shape: {vgg_input.shape}")
    
    print()


def example_6_with_error_handling():
    """
    Example 6: Production-ready preprocessing with error handling
    
    Use this template for real applications.
    """
    print("=" * 60)
    print("Example 6: Error Handling for Production")
    print("=" * 60)
    
    def safe_preprocess(image_path, target_size=(224, 224)):
        """Safely preprocess an image with error handling"""
        try:
            print(f"Processing: {image_path}")
            image = preprocess_image(image_path, target_size=target_size)
            print(f"✓ Successfully processed: {image.shape}")
            return image
        except FileNotFoundError:
            print(f"✗ File not found: {image_path}")
            return None
        except ValueError as e:
            print(f"✗ Invalid image: {str(e)}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
            return None
    
    # Usage
    result = safe_preprocess('path/to/image.jpg')
    if result is not None:
        print(f"Ready for model: Yes")
    else:
        print(f"Ready for model: No")
    
    print()


def example_7_tensorflow_integration():
    """
    Example 7: Integration with TensorFlow/Keras
    
    Demonstrates how to use preprocessed images with TensorFlow models.
    """
    print("=" * 60)
    print("Example 7: TensorFlow Integration (Pseudo-code)")
    print("=" * 60)
    
    print("""
    import tensorflow as tf
    from image_preprocessing import preprocess_image
    
    # Load and preprocess image
    image = preprocess_image('image.jpg', target_size=(224, 224))
    
    # Expand dimensions for batch (add batch dimension)
    image = np.expand_dims(image, axis=0)
    
    # Load pre-trained model
    model = tf.keras.applications.ResNet50(weights='imagenet')
    
    # Make prediction
    predictions = model.predict(image)
    
    # Get top prediction
    top_prediction = tf.keras.applications.resnet50.decode_predictions(
        predictions, 
        top=1
    )
    """)
    print()


def example_8_pytorch_integration():
    """
    Example 8: Integration with PyTorch
    
    Demonstrates how to use preprocessed images with PyTorch models.
    """
    print("=" * 60)
    print("Example 8: PyTorch Integration (Pseudo-code)")
    print("=" * 60)
    
    print("""
    import torch
    from torchvision import models, transforms
    from image_preprocessing import preprocess_image
    
    # Load and preprocess image
    image = preprocess_image('image.jpg', target_size=(224, 224))
    
    # Convert to tensor and add batch dimension
    image_tensor = torch.from_numpy(image).unsqueeze(0)
    
    # Ensure correct shape: (batch_size, channels, height, width)
    image_tensor = image_tensor.permute(0, 3, 1, 2)
    
    # Load pre-trained model
    model = models.resnet50(pretrained=True)
    model.eval()
    
    # Make prediction
    with torch.no_grad():
        output = model(image_tensor)
        predictions = torch.nn.functional.softmax(output, dim=1)
    """)
    print()


def main():
    """Run all examples (note: requires actual image files)"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  IMAGE PREPROCESSING MODULE - USAGE EXAMPLES".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Note: The following examples show pseudo-code and would require
    # actual image files to run. They demonstrate API usage patterns.
    
    print("Note: These example codes demonstrate API usage.")
    print("      Replace 'path/to/image.jpg' with actual file paths to run.\n")
    
    example_1_basic_preprocessing()
    example_2_custom_preprocessing()
    example_3_step_by_step()
    example_4_batch_processing()
    example_5_different_model_sizes()
    example_6_with_error_handling()
    example_7_tensorflow_integration()
    example_8_pytorch_integration()
    
    print("=" * 60)
    print("For more information, see the module docstrings:")
    print("  - from image_preprocessing import load_image")
    print("  - help(load_image)")
    print("=" * 60)


if __name__ == '__main__':
    main()
