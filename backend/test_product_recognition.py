"""
Unit tests for product_recognition_model.py

These tests use lightweight configurations (weights=None) where applicable to
avoid large downloads in CI and local runs. They validate model loading,
prediction output format, confidence range, and integration with the
`image_preprocessing.preprocess_image` function.
"""

import pytest
# Skip these tests if TensorFlow is not installed in the environment.
# This avoids failing the CI/workspace when TF wheels are unavailable
# for the current Python version (e.g., Python 3.14).
pytest.importorskip("tensorflow")
import numpy as np
from pathlib import Path

from product_recognition_model import (
    load_model,
    preprocess_for_model,
    predict_product,
    build_classifier,
)

# Import preprocessing pipeline from existing module
from image_preprocessing import preprocess_image


def test_build_classifier_invalid():
    with pytest.raises(ValueError):
        build_classifier(0)


def test_load_model_lightweight():
    # Use weights=None to avoid Imagenet downloads during tests
    model = load_model(num_classes=5, model_name='MobileNetV2', weights=None, freeze_base=True)
    assert model is not None
    # The classifier head should have output shape matching num_classes
    assert model.output_shape[-1] == 5


def test_preprocess_for_model_and_predict_dummy():
    # Create a dummy image with shape (224,224,3) values in [0,1]
    img = np.random.rand(224, 224, 3).astype(np.float32)

    # Build a lightweight model without pretrained weights
    model = load_model(num_classes=4, model_name='MobileNetV2', weights=None, freeze_base=True)

    # Preprocess for model
    batch = preprocess_for_model(img, model_name='MobileNetV2')
    assert batch.shape[0] == 1
    assert batch.shape[1:] == (224, 224, 3)

    # Predict
    result = predict_product(model, img, class_labels=['a', 'b', 'c', 'd'], model_name='MobileNetV2')

    # Validate keys and types
    assert 'product_name' in result
    assert 'category' in result
    assert 'confidence' in result
    assert 'top_3_predictions' in result
    assert 'keywords' in result
    assert 'embedding_vector' in result

    # Confidence in [0,1]
    assert 0.0 <= float(result['confidence']) <= 1.0


def test_integration_with_preprocessing(tmp_path):
    # Create a small temporary image file and run through preprocess_image -> model -> predict
    img_path = tmp_path / "temp_test.jpg"
    # Create a simple RGB image
    from PIL import Image
    im = Image.new('RGB', (300, 200), color=(120, 80, 200))
    im.save(img_path)

    # Use the existing preprocessing pipeline
    proc = preprocess_image(str(img_path), target_size=(224, 224))
    assert proc.shape == (224, 224, 3)

    # Load lightweight model
    model = load_model(num_classes=3, model_name='MobileNetV2', weights=None, freeze_base=True)
    res = predict_product(model, proc, class_labels=['x', 'y', 'z'], model_name='MobileNetV2')
    assert isinstance(res['product_name'], str)
    assert 0.0 <= float(res['confidence']) <= 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-q'])
