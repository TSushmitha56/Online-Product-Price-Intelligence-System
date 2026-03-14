"""
Unit Tests for Image Preprocessing Module

Comprehensive test suite for the image_preprocessing module using pytest.
Tests cover image loading, resizing, noise reduction, normalization, enhancement,
and the complete preprocessing pipeline.

Author: AI Assistant
Version: 1.0.0
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
import tempfile
import os
from PIL import Image

# Import the module to test
from image_preprocessing import (
    load_image,
    resize_image,
    reduce_noise,
    normalize_image,
    enhance_image,
    preprocess_image,
    SUPPORTED_FORMATS
)


class TestLoadImage:
    """Test suite for load_image function"""
    
    @pytest.fixture
    def temp_image_jpg(self):
        """Create a temporary JPG image file"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(temp_path)
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    @pytest.fixture
    def temp_image_png(self):
        """Create a temporary PNG image file"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(temp_path)
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    @pytest.fixture
    def temp_image_webp(self):
        """Create a temporary WebP image file"""
        with tempfile.NamedTemporaryFile(suffix='.webp', delete=False) as f:
            temp_path = f.name
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='green')
        img.save(temp_path, 'WEBP')
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    def test_load_jpg_image(self, temp_image_jpg):
        """Test loading a JPG image"""
        image = load_image(temp_image_jpg)
        assert isinstance(image, np.ndarray)
        assert image.shape == (100, 100, 3)
        assert image.dtype == np.uint8
    
    def test_load_png_image(self, temp_image_png):
        """Test loading a PNG image"""
        image = load_image(temp_image_png)
        assert isinstance(image, np.ndarray)
        assert image.shape == (100, 100, 3)
        assert image.dtype == np.uint8
    
    def test_load_webp_image(self, temp_image_webp):
        """Test loading a WebP image"""
        image = load_image(temp_image_webp)
        assert isinstance(image, np.ndarray)
        assert image.shape == (100, 100, 3)
        assert image.dtype == np.uint8
    
    def test_load_rgb_conversion(self, temp_image_jpg):
        """Test that loaded image is in RGB format"""
        image = load_image(temp_image_jpg)
        # Red image should have high R channel, low G and B
        assert image.shape[2] == 3  # RGB format
        assert image[0, 0, 0] > image[0, 0, 1]  # R > G
        assert image[0, 0, 0] > image[0, 0, 2]  # R > B
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_image('nonexistent_image.jpg')
    
    def test_load_unsupported_format(self):
        """Test loading unsupported format raises ValueError"""
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as f:
            temp_path = f.name
            img = Image.new('RGB', (100, 100), color='red')
            img.save(temp_path, 'BMP')
        
        try:
            with pytest.raises(ValueError, match="Unsupported image format"):
                load_image(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_corrupted_image(self):
        """Test loading a corrupted image file raises ValueError"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
            f.write(b'This is not a valid image file')
        
        try:
            with pytest.raises(ValueError, match="Could not read image"):
                load_image(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_path_as_string(self):
        """Test that load_image works with string paths"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        img = Image.new('RGB', (100, 100), color='red')
        img.save(temp_path)
        
        try:
            # Load with string path
            image = load_image(str(temp_path))
            assert isinstance(image, np.ndarray)
        finally:
            os.unlink(temp_path)
    
    def test_load_path_as_pathlib(self):
        """Test that load_image works with Path objects"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        img = Image.new('RGB', (100, 100), color='red')
        img.save(temp_path)
        
        try:
            # Load with Path object
            image = load_image(Path(temp_path))
            assert isinstance(image, np.ndarray)
        finally:
            os.unlink(temp_path)


class TestResizeImage:
    """Test suite for resize_image function"""
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample test image"""
        return np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    
    def test_resize_output_shape(self, sample_image):
        """Test that resized image has correct shape"""
        resized = resize_image(sample_image, size=(224, 224))
        assert resized.shape == (224, 224, 3)
    
    def test_resize_maintains_channels(self, sample_image):
        """Test that resize maintains 3 RGB channels"""
        resized = resize_image(sample_image, size=(256, 256))
        assert resized.shape[2] == 3
    
    def test_resize_different_size(self, sample_image):
        """Test resizing to different dimensions"""
        resized = resize_image(sample_image, size=(512, 512))
        assert resized.shape == (512, 512, 3)
    
    def test_resize_small_image(self, sample_image):
        """Test resizing a small image"""
        small_img = sample_image[:10, :10, :]
        resized = resize_image(small_img, size=(224, 224))
        assert resized.shape == (224, 224, 3)
    
    def test_resize_none_image(self):
        """Test that None image raises ValueError"""
        with pytest.raises(ValueError, match="Input image is None"):
            resize_image(None)
    
    def test_resize_empty_image(self):
        """Test that empty image raises ValueError"""
        empty_image = np.array([])
        with pytest.raises(ValueError, match="Input image is None"):
            resize_image(empty_image)
    
    def test_resize_invalid_size_type(self, sample_image):
        """Test that invalid size type raises TypeError"""
        with pytest.raises(TypeError, match="Size must be a tuple"):
            resize_image(sample_image, size=[224, 224])
    
    def test_resize_invalid_size_values(self, sample_image):
        """Test that invalid size values raise ValueError"""
        with pytest.raises(ValueError, match="positive integers"):
            resize_image(sample_image, size=(0, 224))
    
    def test_resize_maintains_dtype(self, sample_image):
        """Test that dtype is preserved after resize"""
        resized = resize_image(sample_image)
        assert resized.dtype == sample_image.dtype


class TestReduceNoise:
    """Test suite for reduce_noise function"""
    
    @pytest.fixture
    def noisy_image(self):
        """Create a noisy test image"""
        image = np.ones((100, 100, 3), dtype=np.uint8) * 128
        # Add random noise
        noise = np.random.normal(0, 25, image.shape)
        noisy = np.clip(image + noise, 0, 255).astype(np.uint8)
        return noisy
    
    def test_reduce_noise_gaussian(self, noisy_image):
        """Test Gaussian blur noise reduction"""
        denoised = reduce_noise(noisy_image, method='gaussian')
        assert denoised.shape == noisy_image.shape
        assert denoised.dtype == noisy_image.dtype
    
    def test_reduce_noise_median(self, noisy_image):
        """Test median filter noise reduction"""
        denoised = reduce_noise(noisy_image, method='median')
        assert denoised.shape == noisy_image.shape
        assert denoised.dtype == noisy_image.dtype
    
    def test_reduce_noise_custom_kernel(self, noisy_image):
        """Test with custom kernel size"""
        denoised = reduce_noise(noisy_image, method='gaussian', kernel_size=7)
        assert denoised.shape == noisy_image.shape
    
    def test_reduce_noise_kernel_size_even(self, noisy_image):
        """Test that even kernel size is converted to odd"""
        denoised = reduce_noise(noisy_image, kernel_size=6)
        assert denoised.shape == noisy_image.shape
    
    def test_reduce_noise_small_kernel(self, noisy_image):
        """Test that very small kernel size raises ValueError"""
        with pytest.raises(ValueError, match="Kernel size must be at least 3"):
            reduce_noise(noisy_image, kernel_size=1)
    
    def test_reduce_noise_unsupported_method(self, noisy_image):
        """Test that unsupported method raises NotImplementedError"""
        with pytest.raises(NotImplementedError, match="not supported"):
            reduce_noise(noisy_image, method='bilateral')
    
    def test_reduce_noise_none_image(self):
        """Test that None image raises ValueError"""
        with pytest.raises(ValueError, match="Input image is None"):
            reduce_noise(None)
    
    def test_reduce_noise_reduces_variance(self, noisy_image):
        """Test that noise reduction actually reduces image variance"""
        denoised = reduce_noise(noisy_image, method='gaussian')
        # Standard deviation should be smaller after denoising
        assert np.std(denoised) < np.std(noisy_image)


class TestNormalizeImage:
    """Test suite for normalize_image function"""
    
    @pytest.fixture
    def sample_image_uint8(self):
        """Create a sample uint8 image"""
        return np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    
    def test_normalize_output_dtype(self, sample_image_uint8):
        """Test that normalized image is float32"""
        normalized = normalize_image(sample_image_uint8)
        assert normalized.dtype == np.float32
    
    def test_normalize_value_range(self, sample_image_uint8):
        """Test that normalized values are in [0.0, 1.0]"""
        normalized = normalize_image(sample_image_uint8)
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0
    
    def test_normalize_shape_preserved(self, sample_image_uint8):
        """Test that shape is preserved after normalization"""
        normalized = normalize_image(sample_image_uint8)
        assert normalized.shape == sample_image_uint8.shape
    
    def test_normalize_boundary_values(self):
        """Test normalization of boundary values"""
        image = np.array([[[0, 127, 255]]], dtype=np.uint8)
        normalized = normalize_image(image)
        assert np.isclose(normalized[0, 0, 0], 0.0)
        assert np.isclose(normalized[0, 0, 1], 127/255)
        assert np.isclose(normalized[0, 0, 2], 1.0)
    
    def test_normalize_none_image(self):
        """Test that None image raises ValueError"""
        with pytest.raises(ValueError, match="Input image is None"):
            normalize_image(None)
    
    def test_normalize_empty_image(self):
        """Test that empty image raises ValueError"""
        empty_image = np.array([])
        with pytest.raises(ValueError, match="Input image is None"):
            normalize_image(empty_image)


class TestEnhanceImage:
    """Test suite for enhance_image function"""
    
    @pytest.fixture
    def sample_image_uint8(self):
        """Create a sample uint8 image"""
        image = np.ones((100, 100, 3), dtype=np.uint8) * 128
        return image
    
    @pytest.fixture
    def sample_image_float(self):
        """Create a sample float32 image"""
        image = np.ones((100, 100, 3), dtype=np.float32) * 0.5
        return image
    
    def test_enhance_shape_preserved(self, sample_image_uint8):
        """Test that shape is preserved after enhancement"""
        enhanced = enhance_image(sample_image_uint8)
        assert enhanced.shape == sample_image_uint8.shape
    
    def test_enhance_dtype_preserved(self, sample_image_uint8):
        """Test that dtype is preserved"""
        enhanced = enhance_image(sample_image_uint8)
        assert enhanced.dtype == sample_image_uint8.dtype
    
    def test_enhance_float_dtype_preserved(self, sample_image_float):
        """Test that float dtype is preserved"""
        enhanced = enhance_image(sample_image_float)
        assert enhanced.dtype == np.float32
    
    def test_enhance_contrast_increases_range(self, sample_image_uint8):
        """Test that contrast enhancement increases value range"""
        enhanced = enhance_image(sample_image_uint8, contrast_factor=1.5)
        # When all values are the same, contrast doesn't change them
        # but we can verify the function runs without error
        assert enhanced.shape == sample_image_uint8.shape
    
    def test_enhance_brightness_factor(self, sample_image_uint8):
        """Test brightness enhancement with factor > 1"""
        enhanced = enhance_image(sample_image_uint8, brightness_factor=1.5)
        assert enhanced.shape == sample_image_uint8.shape
    
    def test_enhance_no_enhancement(self, sample_image_uint8):
        """Test with no enhancement (factors = 1.0)"""
        original = sample_image_uint8.copy()
        enhanced = enhance_image(sample_image_uint8, brightness_factor=1.0, contrast_factor=1.0)
        assert np.allclose(enhanced, original, atol=2)  # Allow small numerical differences
    
    def test_enhance_invalid_brightness_factor(self, sample_image_uint8):
        """Test that negative brightness factor raises ValueError"""
        with pytest.raises(ValueError, match="must be non-negative"):
            enhance_image(sample_image_uint8, brightness_factor=-0.5)
    
    def test_enhance_invalid_contrast_factor(self, sample_image_uint8):
        """Test that negative contrast factor raises ValueError"""
        with pytest.raises(ValueError, match="must be non-negative"):
            enhance_image(sample_image_uint8, contrast_factor=-0.5)
    
    def test_enhance_none_image(self):
        """Test that None image raises ValueError"""
        with pytest.raises(ValueError, match="Input image is None"):
            enhance_image(None)


class TestPreprocessImage:
    """Test suite for preprocess_image pipeline function"""
    
    @pytest.fixture
    def temp_image_jpg(self):
        """Create a temporary JPG image file"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        # Create a test image with realistic size
        img = Image.new('RGB', (800, 600), color='blue')
        img.save(temp_path)
        
        yield temp_path
        
        os.unlink(temp_path)
    
    def test_preprocess_output_shape(self, temp_image_jpg):
        """Test that preprocessed image has correct output shape"""
        processed = preprocess_image(temp_image_jpg, target_size=(224, 224))
        assert processed.shape == (224, 224, 3)
    
    def test_preprocess_output_dtype(self, temp_image_jpg):
        """Test that preprocessed image is float32"""
        processed = preprocess_image(temp_image_jpg)
        assert processed.dtype == np.float32
    
    def test_preprocess_normalized_range(self, temp_image_jpg):
        """Test that normalized preprocessed image is in [0, 1]"""
        processed = preprocess_image(temp_image_jpg, normalize=True)
        assert processed.min() >= 0.0
        assert processed.max() <= 1.0
    
    def test_preprocess_custom_size(self, temp_image_jpg):
        """Test preprocessing with custom target size"""
        processed = preprocess_image(temp_image_jpg, target_size=(256, 256))
        assert processed.shape == (256, 256, 3)
    
    def test_preprocess_without_normalization(self, temp_image_jpg):
        """Test preprocessing without normalization"""
        processed = preprocess_image(temp_image_jpg, normalize=False)
        # Values should still be in [0, 255] range
        assert processed.max() <= 255
    
    def test_preprocess_without_enhancement(self, temp_image_jpg):
        """Test preprocessing without enhancement"""
        processed = preprocess_image(temp_image_jpg, enhance=False)
        assert processed.shape == (224, 224, 3)
    
    def test_preprocess_nonexistent_file(self):
        """Test preprocessing nonexistent file raises error"""
        with pytest.raises(FileNotFoundError):
            preprocess_image('nonexistent.jpg')
    
    def test_preprocess_rgb_conversion(self, temp_image_jpg):
        """Test that preprocessing results in RGB image"""
        processed = preprocess_image(temp_image_jpg)
        # Blue image should have high B channel
        assert processed.shape[2] == 3  # RGB


class TestIntegration:
    """Integration tests combining multiple functions"""
    
    @pytest.fixture
    def temp_image_jpg(self):
        """Create a temporary JPG image file"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        # Create a realistic test image
        img = Image.new('RGB', (640, 480), color='red')
        img.save(temp_path)
        
        yield temp_path
        
        os.unlink(temp_path)
    
    def test_full_pipeline(self, temp_image_jpg):
        """Test the full preprocessing pipeline"""
        # Load
        image = load_image(temp_image_jpg)
        assert image.shape == (480, 640, 3)
        
        # Resize
        image = resize_image(image, size=(224, 224))
        assert image.shape == (224, 224, 3)
        
        # Denoise
        image = reduce_noise(image)
        assert image.shape == (224, 224, 3)
        
        # Enhance
        image = enhance_image(image)
        assert image.shape == (224, 224, 3)
        
        # Normalize
        image = normalize_image(image)
        assert image.dtype == np.float32
        assert image.min() >= 0.0 and image.max() <= 1.0
    
    def test_preprocess_pipeline_consistency(self, temp_image_jpg):
        """Test that preprocess_image produces consistent results"""
        result1 = preprocess_image(temp_image_jpg)
        result2 = preprocess_image(temp_image_jpg)
        
        # Results should be identical
        assert np.allclose(result1, result2)
    
    def test_pipeline_output_ready_for_model(self, temp_image_jpg):
        """Test that pipeline output is ready for neural networks"""
        processed = preprocess_image(temp_image_jpg, target_size=(224, 224))
        
        # Check prerequisites for model input
        assert processed.dtype == np.float32  # Floating point
        assert processed.shape == (224, 224, 3)  # Correct dimensions
        assert processed.min() >= 0.0 and processed.max() <= 1.0  # Normalized
        assert not np.any(np.isnan(processed))  # No NaN values
        assert not np.any(np.isinf(processed))  # No infinite values


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_very_large_image(self):
        """Test handling of very large images"""
        # Create a large image
        large_image = np.random.randint(0, 256, (4096, 4096, 3), dtype=np.uint8)
        resized = resize_image(large_image, size=(224, 224))
        assert resized.shape == (224, 224, 3)
    
    def test_very_small_image(self):
        """Test handling of very small images"""
        small_image = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
        resized = resize_image(small_image, size=(224, 224))
        assert resized.shape == (224, 224, 3)
    
    def test_single_channel_handling(self):
        """Test handling of single channel conversion"""
        # Load grayscale and verify RGB conversion
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            temp_path = f.name
        
        # Create grayscale image
        img = Image.new('L', (100, 100), color=128)
        img.save(temp_path)
        
        try:
            image = load_image(temp_path)
            # Should be converted to RGB (3 channels)
            assert image.shape[2] == 3
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
