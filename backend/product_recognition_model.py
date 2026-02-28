"""
Product Recognition Model Module

Implements a TensorFlow-based product recognition and classification module
that integrates with the existing `image_preprocessing.py` pipeline. The module
is production-ready with clear separation of concerns, GPU/CPU compatibility,
batch prediction support, and evaluation utilities.

Functions:
- load_model
- build_classifier
- preprocess_for_model
- predict_product
- generate_keywords
- fine_tune_model
- evaluate_model

Notes:
- If TensorFlow is not available, `load_model` will raise an informative error.
- For unit tests and lightweight runs you can call `load_model(..., weights=None)`
  to avoid downloading ImageNet weights.

"""

from typing import Optional, List, Tuple, Dict, Any
import numpy as np
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Lazy import TensorFlow to keep module import lightweight for static checks
try:
    import tensorflow as tf
    from tensorflow.keras import Model
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.models import Sequential
    TF_AVAILABLE = True
except Exception:  # pragma: no cover - handled at runtime
    tf = None
    Model = None
    TF_AVAILABLE = False


def _ensure_tf_available():
    if not TF_AVAILABLE:
        raise ImportError(
            "TensorFlow is required for product_recognition_model. "
            "Install it with `pip install tensorflow` or use a Python environment with TF."
        )


def build_classifier(num_classes: int, dropout_rate: float = 0.4) -> Sequential:
    """
    Build a lightweight classification head for transfer learning.

    Args:
        num_classes (int): Number of output classes.
        dropout_rate (float): Dropout rate between dense layers.

    Returns:
        keras.Sequential: A small classifier head that accepts a pooled feature
                          vector and returns class probabilities.
    """
    _ensure_tf_available()

    if num_classes <= 0:
        raise ValueError("num_classes must be a positive integer")

    head = Sequential([
        Dense(256, activation="relu", name="cls_dense_1"),
        Dropout(dropout_rate, name="cls_dropout_1"),
        Dense(128, activation="relu", name="cls_dense_2"),
        Dropout(dropout_rate / 2.0, name="cls_dropout_2"),
        Dense(num_classes, activation="softmax", name="cls_logits"),
    ], name="classifier_head")

    return head


def load_model(
    num_classes: int,
    model_name: str = "MobileNetV2",
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    weights: Optional[str] = "imagenet",
    freeze_base: bool = True,
) -> tf.keras.Model:
    """
    Load a pretrained base model and attach a custom classification head.

    Args:
        num_classes (int): Number of product categories for the classifier.
        model_name (str): One of 'MobileNetV2', 'EfficientNetB0', optionally 'ResNet50'.
        input_shape (tuple): Input shape (H, W, C). Default (224,224,3).
        weights (str|None): Weights to load for the base. Use None to avoid downloads.
        freeze_base (bool): Whether to freeze base model layers.

    Returns:
        tf.keras.Model: Compiled model (untrained classifier head).

    Raises:
        ImportError: If TensorFlow is not installed.
        ValueError: If model_name is not supported.
    """
    _ensure_tf_available()

    model_name = model_name.lower()
    base = None

    try:
        if model_name == "mobilenetv2":
            base = tf.keras.applications.MobileNetV2(
                include_top=False, weights=weights, input_shape=input_shape, pooling="avg"
            )
        elif model_name == "efficientnetb0":
            # EfficientNetB0 is available as EfficientNetB0 in tf.keras.applications
            base = tf.keras.applications.EfficientNetB0(
                include_top=False, weights=weights, input_shape=input_shape, pooling="avg"
            )
        elif model_name == "resnet50":
            base = tf.keras.applications.ResNet50(
                include_top=False, weights=weights, input_shape=input_shape, pooling="avg"
            )
        else:
            raise ValueError("Unsupported model_name. Choose 'MobileNetV2', 'EfficientNetB0', or 'ResNet50'.")

        # Build classification head
        classifier_head = build_classifier(num_classes)

        # Attach head to base
        inputs = base.input
        features = base.output
        outputs = classifier_head(features)
        model = Model(inputs=inputs, outputs=outputs, name=f"{model_name}_product_recognizer")

        # Freeze base if requested
        if freeze_base:
            for layer in base.layers:
                layer.trainable = False

        # Compile with a common optimizer and loss for classification
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                      loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])

        logger.info("Model loaded and compiled: %s", model.name)
        return model

    except Exception as e:
        logger.error("Failed to load model: %s", e)
        raise


def preprocess_for_model(image_array: np.ndarray, model_name: str = "MobileNetV2") -> np.ndarray:
    """
    Convert a preprocessed NumPy image into the tensor expected by the selected model.

    This function expects `image_array` to be a NumPy array in RGB format with
    values in [0.0, 1.0] (as returned by the `preprocess_image` pipeline). It will
    convert values and apply the model-specific `preprocess_input` function.

    Args:
        image_array (np.ndarray): Image array of shape (H, W, 3) with values [0,1].
        model_name (str): Model name used to select preprocessing function.

    Returns:
        np.ndarray: Batch tensor ready for model.predict with shape (1, H, W, 3).
    """
    _ensure_tf_available()

    if image_array is None:
        raise ValueError("image_array must not be None")
    if not isinstance(image_array, np.ndarray):
        raise TypeError("image_array must be a numpy.ndarray")
    if image_array.ndim != 3 or image_array.shape[2] != 3:
        raise ValueError("image_array must have shape (H, W, 3)")

    # Convert back to [0,255] because Keras preprocess_input expects that
    arr = np.clip(image_array, 0.0, 1.0).astype(np.float32) * 255.0

    model_name = model_name.lower()
    if model_name == "mobilenetv2":
        arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    elif model_name == "efficientnetb0":
        arr = tf.keras.applications.efficientnet.preprocess_input(arr)
    elif model_name == "resnet50":
        arr = tf.keras.applications.resnet.preprocess_input(arr)
    else:
        # Default: no extra preprocessing
        logger.debug("No specific preprocess_input for %s", model_name)

    # Add batch dimension
    batch = np.expand_dims(arr, axis=0)
    return batch


def _to_serializable(obj: Any) -> Any:
    """
    Convert numpy or tf values to native Python types for JSON serialization.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    return obj


def generate_keywords(prediction_probs: List[Tuple[str, float]], class_labels: Optional[List[str]] = None, top_k: int = 3) -> List[str]:
    """
    Generate simple descriptive keywords for the top predictions.

    This is intentionally lightweight and intended to be a placeholder for
    more advanced NLP-based keyword extraction in production.

    Args:
        prediction_probs (List[Tuple[str, float]]): List of (label, prob) tuples.
        class_labels (List[str], optional): All class labels (optional).
        top_k (int): How many top keywords to return.

    Returns:
        List[str]: Short list of keywords (strings).
    """
    keywords = []
    for label, prob in prediction_probs[:top_k]:
        # Split label by common separators and select tokens
        tokens = [t.strip() for t in label.replace("_", " ").split() if len(t) > 1]
        # Add tokens while avoiding duplicates
        for t in tokens:
            if t.lower() not in [k.lower() for k in keywords]:
                keywords.append(t.lower())
            if len(keywords) >= top_k:
                break
        if len(keywords) >= top_k:
            break

    return keywords


def predict_product(
    model: tf.keras.Model,
    image_array: np.ndarray,
    class_labels: Optional[List[str]] = None,
    model_name: str = "MobileNetV2",
    return_embedding: bool = True,
) -> Dict[str, Any]:
    """
    Run inference on one preprocessed image and return structured results.

    Args:
        model (tf.keras.Model): Loaded Keras model (from `load_model`).
        image_array (np.ndarray): Preprocessed image array (H, W, 3) values [0,1].
        class_labels (List[str], optional): Class label names. If not provided,
                                            labels will be generated as `class_0`, ...
        model_name (str): The base model name used for preprocessing.
        return_embedding (bool): Whether to return the embedding vector.

    Returns:
        Dict[str, Any]: JSON-serializable dictionary containing prediction info.
    """
    _ensure_tf_available()

    if model is None:
        raise ValueError("`model` must be provided")

    # Prepare input
    batch = preprocess_for_model(image_array, model_name=model_name)

    # Run inference
    preds = model.predict(batch)

    # Handle batch predictions - we accept single-image batches only here
    if preds.ndim == 2:
        probs = preds[0]
    else:
        probs = np.ravel(preds)

    # Prepare labels
    num_classes = probs.shape[-1]
    if class_labels is None:
        class_labels = [f"class_{i}" for i in range(num_classes)]

    # Top predictions
    top_idx = np.argsort(probs)[::-1]
    top_3_idx = top_idx[:3]
    top_3 = [(class_labels[i], float(probs[i])) for i in top_3_idx]

    predicted_idx = int(top_idx[0])
    predicted_label = class_labels[predicted_idx]
    confidence = float(probs[predicted_idx])

    # Embedding: model's penultimate layer is assumed to be the pooling output
    # We create a sub-model to extract the pooled features (before classifier head)
    embedding_vector = None
    if return_embedding:
        try:
            # Find a layer that looks like a pooling layer (global average pooling)
            pool_layer = None
            for lyr in model.layers[::-1]:
                if 'pool' in lyr.name or 'global' in lyr.name or lyr.output_shape[-1] > 0:
                    pool_layer = lyr
                    break

            if pool_layer is not None:
                embedding_extractor = tf.keras.Model(inputs=model.input, outputs=pool_layer.output)
                emb = embedding_extractor.predict(batch)
                # If embedding is multidimensional, flatten
                emb = emb.reshape(emb.shape[0], -1)[0]
                embedding_vector = emb.tolist()
            else:
                embedding_vector = None
        except Exception:
            # Best-effort: return None instead of failing prediction
            embedding_vector = None

    # Generate keywords from top_3
    keywords = generate_keywords(top_3, class_labels=class_labels, top_k=5)

    result = {
        "product_name": predicted_label,
        "category": predicted_label,
        "confidence": confidence,
        "top_3_predictions": top_3,
        "keywords": keywords,
        "embedding_vector": embedding_vector,
    }

    # Ensure serializability
    serializable_result = {k: _to_serializable(v) for k, v in result.items()}
    return serializable_result


def fine_tune_model(
    model: tf.keras.Model,
    dataset_path: str,
    num_classes: int,
    epochs: int = 5,
    batch_size: int = 32,
    learning_rate: float = 1e-4,
    unfreeze_from: Optional[int] = None,
    save_path: Optional[str] = None,
) -> tf.keras.Model:
    """
    Fine-tune the provided model on a dataset located at `dataset_path`.

    Args:
        model (tf.keras.Model): Model returned from `load_model`.
        dataset_path (str): Directory with subfolders for each class (ImageNet-like).
        num_classes (int): Number of classes in dataset.
        epochs (int): Number of training epochs.
        batch_size (int): Training batch size.
        learning_rate (float): Learning rate for fine-tuning.
        unfreeze_from (int): If provided, unfreeze base model layers from this
                              index onward for fine-tuning.
        save_path (str): Optional path to save the fine-tuned model.

    Returns:
        tf.keras.Model: The fine-tuned model.
    """
    _ensure_tf_available()

    # Prepare datasets using image_dataset_from_directory (handles augmentation)
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        labels='inferred',
        label_mode='int',
        batch_size=batch_size,
        image_size=(224, 224),
        shuffle=True,
        validation_split=0.2,
        subset='training',
        seed=123,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        labels='inferred',
        label_mode='int',
        batch_size=batch_size,
        image_size=(224, 224),
        shuffle=True,
        validation_split=0.2,
        subset='validation',
        seed=123,
    )

    # Data augmentation pipeline
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.05),
        tf.keras.layers.RandomZoom(0.05),
    ], name='data_augmentation')

    AUTOTUNE = tf.data.AUTOTUNE
    def prepare(ds, training=False):
        ds = ds.map(lambda x, y: (data_augmentation(x, training=training) if training else x, y),
                    num_parallel_calls=AUTOTUNE)
        return ds.prefetch(buffer_size=AUTOTUNE)

    train_ds = prepare(train_ds, training=True)
    val_ds = prepare(val_ds, training=False)

    # Optionally unfreeze layers
    if unfreeze_from is not None:
        for i, layer in enumerate(model.layers):
            if i >= unfreeze_from:
                layer.trainable = True

    # Recompile with lower learning rate for fine-tuning
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Training loop
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

    if save_path is not None:
        try:
            model.save(save_path)
            logger.info("Saved fine-tuned model to %s", save_path)
        except Exception as e:
            logger.warning("Failed to save model: %s", e)

    return model


def evaluate_model(model: tf.keras.Model, test_dataset_path: str, batch_size: int = 32) -> Dict[str, Any]:
    """
    Evaluate the model on a test dataset and compute standard metrics.

    Args:
        model (tf.keras.Model): Trained model.
        test_dataset_path (str): Directory with subfolders per class.
        batch_size (int): Batch size for evaluation.

    Returns:
        Dict[str, Any]: Dictionary containing accuracy, precision, recall, f1, confusion matrix, avg_inference_time.
    """
    _ensure_tf_available()

    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_dataset_path,
        labels='inferred',
        label_mode='int',
        batch_size=batch_size,
        image_size=(224, 224),
        shuffle=False,
    )

    y_true = []
    y_pred = []
    total_time = 0.0
    total_examples = 0

    for batch_x, batch_y in test_ds:
        start = time.time()
        preds = model.predict(batch_x)
        end = time.time()
        total_time += (end - start)
        total_examples += batch_x.shape[0]

        preds_idx = np.argmax(preds, axis=1)
        y_true.extend(batch_y.numpy().tolist())
        y_pred.extend(preds_idx.tolist())

    # Compute metrics using sklearn if available, else compute manually
    metrics: Dict[str, Any] = {}
    try:
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

        metrics['accuracy'] = float(accuracy_score(y_true, y_pred))
        metrics['precision_macro'] = float(precision_score(y_true, y_pred, average='macro', zero_division=0))
        metrics['recall_macro'] = float(recall_score(y_true, y_pred, average='macro', zero_division=0))
        metrics['f1_macro'] = float(f1_score(y_true, y_pred, average='macro', zero_division=0))
        metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()
    except Exception:
        # Fallback simple accuracy calculation
        correct = sum(int(a == b) for a, b in zip(y_true, y_pred))
        metrics['accuracy'] = float(correct / len(y_true)) if len(y_true) > 0 else 0.0
        metrics['precision_macro'] = None
        metrics['recall_macro'] = None
        metrics['f1_macro'] = None
        metrics['confusion_matrix'] = None

    metrics['avg_inference_time_seconds'] = float(total_time / total_examples) if total_examples > 0 else None
    return metrics


# Module-level small demo helper (not executed on import)
if __name__ == '__main__':
    print("This module provides model utilities for product recognition. Import and use its functions in your application.")
