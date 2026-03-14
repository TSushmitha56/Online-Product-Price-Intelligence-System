"""
Image Preprocessing Module for AI-based Product Recognition System

This module provides a comprehensive pipeline for preprocessing images to prepare them
for deep learning models (TensorFlow/PyTorch). It handles image loading, resizing,
noise reduction, enhancement, and normalization.

Author: AI Assistant
Version: 1.0.0
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
from typing import Union, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported image formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp'}


def load_image(image_path: Union[str, Path]) -> np.ndarray:
    """
    Load image from disk and convert to RGB format.
    
    Supports JPG, PNG, and WebP formats. Images are automatically converted
    to RGB to ensure consistent color channel handling across all formats.
    
    Args:
        image_path (Union[str, Path]): Path to the image file
        
    Returns:
        np.ndarray: Image array in RGB format with shape (height, width, 3)
        
    Raises:
        FileNotFoundError: If the image file does not exist
        ValueError: If the file format is not supported or image is corrupted
        
    Example:
        >>> image = load_image('product.jpg')
        >>> image.shape
        (960, 1280, 3)
    """
    image_path = Path(image_path)
    
    # Validate file exists
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Validate file format
    file_ext = image_path.suffix.lower()
    if file_ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {file_ext}. Supported: {SUPPORTED_FORMATS}")
    
    try:
        # Load image using OpenCV (loads as BGR)
        image_bgr = cv2.imread(str(image_path))
        
        # Check if image was loaded successfully
        if image_bgr is None:
            raise ValueError(f"Could not read image. File may be corrupted: {image_path}")
        
        # Convert BGR to RGB (OpenCV loads images in BGR format)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        logger.info(f"Successfully loaded image from {image_path} | Shape: {image_rgb.shape}")
        return image_rgb
        
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {str(e)}")
        raise ValueError(f"Failed to load image: {str(e)}")


def resize_image(image: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Resize image to fixed dimensions for CNN model input.
    
    Uses bilinear interpolation for high-quality resizing. The output size
    is suitable for most pre-trained models like ResNet, VGG, and EfficientNet.
    
    Args:
        image (np.ndarray): Input image array in RGB format
        size (Tuple[int, int]): Target size as (height, width). Default: (224, 224)
        
    Returns:
        np.ndarray: Resized image array with shape (height, width, 3)
        
    Raises:
        ValueError: If image is None or has invalid shape
        TypeError: If size parameter is not a tuple of integers
        
    Example:
        >>> resized = resize_image(image, size=(256, 256))
        >>> resized.shape
        (256, 256, 3)
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    if not isinstance(size, tuple) or len(size) != 2:
        raise TypeError("Size must be a tuple of (height, width)")
    
    if not all(isinstance(s, int) and s > 0 for s in size):
        raise ValueError("Size dimensions must be positive integers")
    
    try:
        # Use cv2.resize with bilinear interpolation for quality
        resized = cv2.resize(image, (size[1], size[0]), interpolation=cv2.INTER_LINEAR)
        
        logger.info(f"Image resized to {size}")
        return resized
        
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        raise


def reduce_noise(image: np.ndarray, method: str = 'gaussian', kernel_size: int = 5) -> np.ndarray:
    """
    Apply noise reduction using Gaussian blur or median filtering.
    
    Gaussian blur is faster and suitable for mild noise reduction, while
    median filtering is better for salt-and-pepper noise.
    
    Args:
        image (np.ndarray): Input image array in RGB format
        method (str): Noise reduction method - 'gaussian' or 'median'. Default: 'gaussian'
        kernel_size (int): Kernel size (must be odd). Default: 5
        
    Returns:
        np.ndarray: Denoised image array with same shape as input
        
    Raises:
        ValueError: If image is None or kernel_size is invalid
        NotImplementedError: If method is not supported
        
    Example:
        >>> denoised = reduce_noise(image, method='gaussian', kernel_size=5)
        >>> denoised.shape == image.shape
        True
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    if kernel_size < 3:
        raise ValueError("Kernel size must be at least 3")
    
    try:
        if method.lower() == 'gaussian':
            # Apply Gaussian blur (fast, suitable for general noise)
            denoised = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            logger.info(f"Gaussian blur applied with kernel size {kernel_size}")
            
        elif method.lower() == 'median':
            # Apply median filtering (better for salt-and-pepper noise)
            denoised = cv2.medianBlur(image, kernel_size)
            logger.info(f"Median blur applied with kernel size {kernel_size}")
            
        else:
            raise NotImplementedError(f"Noise reduction method '{method}' not supported. "
                                    "Supported: 'gaussian', 'median'")
        
        return denoised
        
    except Exception as e:
        logger.error(f"Error reducing noise: {str(e)}")
        raise


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image by scaling pixel values to [0, 1] range.
    
    Converts uint8 pixel values (0-255) to float32 values (0.0-1.0).
    This normalization is essential for neural network training and inference
    as it helps with convergence and numerical stability.
    
    Args:
        image (np.ndarray): Input image array with values in [0, 255]
        
    Returns:
        np.ndarray: Normalized image as float32 with values in [0.0, 1.0]
        
    Raises:
        ValueError: If image is None
        
    Example:
        >>> normalized = normalize_image(image)
        >>> normalized.dtype
        dtype('float32')
        >>> normalized.min(), normalized.max()
        (0.0, 1.0)
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    try:
        # Convert to float32 and normalize to [0, 1]
        normalized = image.astype(np.float32) / 255.0
        
        logger.info(f"Image normalized to range [0.0, 1.0] | dtype: {normalized.dtype}")
        return normalized
        
    except Exception as e:
        logger.error(f"Error normalizing image: {str(e)}")
        raise


def enhance_image(image: np.ndarray, brightness_factor: float = 1.0,
                 contrast_factor: float = 1.2) -> np.ndarray:
    """
    Apply contrast enhancement and brightness correction to image.
    
    Uses PIL's ImageEnhance for robust enhancement. Default settings
    slightly increase contrast while maintaining original brightness.
    
    Args:
        image (np.ndarray): Input image array (can be uint8 or float32)
        brightness_factor (float): Brightness adjustment factor. 
                                  1.0 = no change, >1.0 = brighter. Default: 1.0
        contrast_factor (float): Contrast adjustment factor.
                                1.0 = no change, >1.0 = more contrast. Default: 1.2
        
    Returns:
        np.ndarray: Enhanced image with same dtype as input
        
    Raises:
        ValueError: If image is None or enhancement factors are invalid
        
    Example:
        >>> enhanced = enhance_image(image, brightness_factor=1.1, contrast_factor=1.3)
        >>> enhanced.shape == image.shape
        True
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is None or empty")
    
    if brightness_factor < 0 or contrast_factor < 0:
        raise ValueError("Brightness and contrast factors must be non-negative")
    
    try:
        # Preserve original dtype
        original_dtype = image.dtype
        
        # Convert to uint8 if necessary (for PIL compatibility)
        if original_dtype == np.float32 or original_dtype == np.float64:
            image_uint8 = (np.clip(image, 0, 1) * 255).astype(np.uint8)
        else:
            image_uint8 = image.astype(np.uint8)
        
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(image_uint8)
        
        # Apply brightness enhancement
        if brightness_factor != 1.0:
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(brightness_factor)
        
        # Apply contrast enhancement
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(contrast_factor)
        
        # Convert back to numpy array
        enhanced = np.array(pil_image)
        
        # Restore original dtype if it was float
        if original_dtype == np.float32 or original_dtype == np.float64:
            enhanced = enhanced.astype(original_dtype) / 255.0
        
        logger.info(f"Image enhanced | Brightness: {brightness_factor}, Contrast: {contrast_factor}")
        return enhanced
        
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        raise


def preprocess_image(image_path: Union[str, Path],
                    target_size: Tuple[int, int] = (224, 224),
                    normalize: bool = True,
                    enhance: bool = True,
                    output_path: Optional[Union[str, Path]] = None) -> Union[np.ndarray, str]:
    """
    Complete preprocessing pipeline for image data.
    
    This is the main function that orchestrates all preprocessing steps:
    1. Load image from disk
    2. Convert to RGB
    3. Resize to target dimensions
    4. Reduce noise
    5. Enhance (contrast/brightness)
    6. Normalize to [0, 1]
    
    The output is directly compatible with TensorFlow/PyTorch models.
    
    Args:
        image_path (Union[str, Path]): Path to the image file
        target_size (Tuple[int, int]): Target size as (height, width). Default: (224, 224)
        normalize (bool): Whether to normalize to [0, 1]. Default: True
        enhance (bool): Whether to apply enhancement. Default: True
        
        output_path (Optional[Union[str, Path]]): Path to save the processed image
        
    Returns:
        Union[np.ndarray, str]: Preprocessed image as float32 array if output_path is None,
                               else returns the output_path string.
                   Array Shape: (height, width, 3)
                   Array Values: [0.0, 1.0] if normalize=True, else [0, 255]
        
    Raises:
        Various exceptions from individual preprocessing functions
        
    Example:
        >>> processed = preprocess_image('product.jpg', target_size=(256, 256))
        >>> processed.shape
        (256, 256, 3)
        >>> processed.dtype
        dtype('float32')
        >>> processed.min(), processed.max()
        (0.0, 1.0)
    """
    try:
        logger.info(f"Starting image preprocessing pipeline for {image_path}")
        
        # Step 1: Load image
        image = load_image(image_path)
        logger.info(f"Step 1/6: Loaded image | Original shape: {image.shape}")
        
        # Step 2: Resize image
        image = resize_image(image, size=target_size)
        logger.info(f"Step 2/6: Resized to {target_size}")
        
        # Step 3: Reduce noise
        image = reduce_noise(image, method='gaussian', kernel_size=5)
        logger.info("Step 3/6: Noise reduction applied")
        
        # Step 4: Enhance (optional)
        if enhance:
            image = enhance_image(image, brightness_factor=1.0, contrast_factor=1.2)
            logger.info("Step 4/6: Image enhancement applied")
        else:
            logger.info("Step 4/6: Image enhancement skipped")
        
        # Step 5: Normalize
        if normalize:
            image = normalize_image(image)
            logger.info("Step 5/6: Image normalized to [0, 1]")
        else:
            logger.info("Step 5/6: Normalization skipped")
        
        logger.info(f"Step 6/6: Pipeline complete | Final shape: {image.shape} | dtype: {image.dtype}")
        logger.info("✓ Preprocessing pipeline completed successfully")
        
        # Step 7: Save to disk (optional)
        if output_path:
            save_image = image
            if normalize:
                save_image = (np.clip(save_image, 0, 1) * 255).astype(np.uint8)
            else:
                save_image = np.clip(save_image, 0, 255).astype(np.uint8)
                
            pil_img = Image.fromarray(save_image)
            pil_img.save(str(output_path))
            logger.info(f"Step 7/7: Saved preprocessed image to {output_path}")
            return str(output_path)
            
        return image
        
    except Exception as e:
        logger.error(f"Preprocessing pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    """
    Example usage of the image preprocessing module
    """
    # Example: Preprocess an image
    # image = preprocess_image('path/to/image.jpg')
    # print(f"Preprocessed image shape: {image.shape}")
    # print(f"Data type: {image.dtype}")
    # print(f"Value range: [{image.min():.4f}, {image.max():.4f}]")
    pass
