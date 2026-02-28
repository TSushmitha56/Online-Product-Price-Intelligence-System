/**
 * ImageUpload Component
 * Handles file selection via drag-and-drop or click-to-browse
 * Displays image preview and uploads to backend API
 * Responsive design with hover and active states for better UX
 */
import { useState, useRef } from 'react';

export default function ImageUpload() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragActive, setIsDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploadedData, setUploadedData] = useState(null);
  const [isRecognizing, setIsRecognizing] = useState(false);
  const [recognitionData, setRecognitionData] = useState(null);
  const fileInputRef = useRef(null);

  /**
   * Handles file selection - accepts image files only
   * Creates a preview URL for the selected image
   */
  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      // Create a preview URL for the image
      const reader = new FileReader();
      reader.onload = (event) => {
        setPreview(event.target.result);
      };
      reader.readAsDataURL(file);
      setUploadStatus(null);
      setUploadedData(null);
      setRecognitionData(null);
    } else {
      setUploadStatus({
        type: 'error',
        message: 'Please select a valid image file (JPEG, PNG, WebP)'
      });
    }
  };

  /**
   * Handles drag over event
   * Adds visual feedback when dragging files over the upload area
   */
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  /**
   * Handles drag leave event
   * Removes visual feedback when dragging away
   */
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  /**
   * Handles drop event
   * Processes dropped files and validates them as images
   */
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  /**
   * Handles click on upload area
   * Triggers file input click to open file browser
   */
  const handleClick = () => {
    fileInputRef.current?.click();
  };

  /**
   * Handles file input change event
   * Triggered when user selects file from browser
   */
  const handleInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  /**
   * Uploads the selected image to the backend API
   * Sends the file to /api/upload-image/ endpoint
   * Displays upload status and success/error messages
   */
  const handleUpload = async () => {
    if (!selectedImage) return;

    setIsUploading(true);
    setUploadStatus(null);

    try {
      // Create FormData for multipart/form-data submission
      const formData = new FormData();
      formData.append('file', selectedImage);

      // Send POST request to backend API
      const response = await fetch('http://localhost:8000/api/upload-image/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        // Success response
        setUploadStatus({
          type: 'success',
          message: data.message || 'Image uploaded successfully!'
        });
        setUploadedData({
          image_id: data.image_id,
          original_filename: data.original_filename,
          file_size_mb: data.file_size_mb,
          timestamp: new Date(data.timestamp).toLocaleString()
        });
      } else {
        // Error response from server
        setUploadStatus({
          type: 'error',
          message: data.message || 'Failed to upload image'
        });
      }
    } catch (error) {
      // Network or other errors
      setUploadStatus({
        type: 'error',
        message: `Upload failed: ${error.message}. Make sure the backend is running at http://localhost:8000`
      });
    } finally {
      setIsUploading(false);
    }
  };

  /**
   * Calls the Product Recognition backend API.
   * Sends the image_id of the uploaded image to be analyzed by the CNN.
   */
  const handleRecognize = async () => {
    if (!uploadedData || !uploadedData.image_id) return;
    
    setIsRecognizing(true);
    setUploadStatus(null);
    setRecognitionData(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/recognize-product/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_id: uploadedData.image_id }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setRecognitionData(data.recognition);
      } else {
        setUploadStatus({
          type: 'error',
          message: data.message || 'Failed to recognize product'
        });
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: `Recognition failed: ${error.message}`
      });
    } finally {
      setIsRecognizing(false);
    }
  };

  /**
   * Resets the upload state
   * Clears selected file and preview
   */
  const handleClear = () => {
    setSelectedImage(null);
    setPreview(null);
    setUploadStatus(null);
    setUploadedData(null);
    setRecognitionData(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Upload Your Image</h2>

      {/* Upload Area - Drag & Drop or Click */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`relative border-4 border-dashed rounded-lg p-12 text-center cursor-pointer transition duration-300 ${
          isDragActive
            ? 'border-blue-600 bg-blue-50'
            : 'border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-blue-25'
        }`}
        role="button"
        tabIndex={0}
        aria-label="Drag and drop area for uploading images"
      >
        {/* Upload Icon and Text */}
        <div className="flex flex-col items-center justify-center">
          <span className="text-6xl mb-4">📸</span>
          <p className="text-xl font-semibold text-gray-700 mb-2">
            Drag and drop your image here
          </p>
          <p className="text-gray-500 mb-4">or</p>
          <button
            onClick={handleClick}
            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
            aria-label="Click to browse and select an image file"
          >
            Browse Files
          </button>
          <p className="text-sm text-gray-500 mt-4">
            Supported formats: JPG, PNG, WebP (Maximum 10MB)
          </p>
        </div>

        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleInputChange}
          className="hidden"
          aria-hidden="true"
        />
      </div>

      {/* Status Messages */}
      {uploadStatus && (
        <div
          className={`mt-6 p-4 rounded-lg ${
            uploadStatus.type === 'success'
              ? 'bg-green-50 border border-green-200'
              : 'bg-red-50 border border-red-200'
          }`}
        >
          <p
            className={`font-semibold ${
              uploadStatus.type === 'success'
                ? 'text-green-800'
                : 'text-red-800'
            }`}
          >
            {uploadStatus.type === 'success' ? '✅' : '❌'} {uploadStatus.message}
          </p>
        </div>
      )}

      {/* Image Preview Section */}
      {preview && (
        <div className="mt-12">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">Preview</h3>

          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Preview Image */}
            <div className="flex justify-center bg-gray-100 p-4">
              <img
                src={preview}
                alt="Preview of uploaded image"
                className="max-w-full max-h-96 object-contain rounded"
              />
            </div>

            {/* File Information */}
            {selectedImage && (
              <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <p className="text-sm font-semibold text-gray-600">File Name</p>
                    <p className="text-gray-800 break-words text-sm">
                      {selectedImage.name}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-600">File Size</p>
                    <p className="text-gray-800">
                      {(selectedImage.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-600">File Type</p>
                    <p className="text-gray-800">{selectedImage.type}</p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4">
                  <button
                    onClick={handleClear}
                    disabled={isUploading}
                    className="flex-1 px-4 py-3 bg-gray-300 text-gray-800 font-semibold rounded-lg hover:bg-gray-400 transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Clear
                  </button>
                  <button
                    onClick={handleUpload}
                    disabled={isUploading}
                    className="flex-1 px-4 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isUploading ? '⏳ Uploading...' : '📤 Upload'}
                  </button>
                </div>
              </div>
            )}

            {/* Uploaded Details */}
            {uploadedData && (
              <div className="bg-blue-50 px-6 py-4 border-t border-blue-200">
                <p className="text-sm font-semibold text-blue-900 mb-3">
                  ✅ Upload successful! Here are your image details:
                </p>
                <div className="space-y-2 text-sm text-blue-800">
                  <div>
                    <span className="font-semibold">Image ID:</span>{' '}
                    <code className="bg-white px-2 py-1 rounded font-mono text-xs">
                      {uploadedData.image_id}
                    </code>
                  </div>
                  <div>
                    <span className="font-semibold">Original Name:</span>{' '}
                    {uploadedData.original_filename}
                  </div>
                  <div>
                    <span className="font-semibold">Size:</span>{' '}
                    {uploadedData.file_size_mb} MB
                  </div>
                  <div>
                    <span className="font-semibold">Uploaded:</span>{' '}
                    {uploadedData.timestamp}
                  </div>
                </div>

                {/* Recognition Action */}
                {!recognitionData && (
                  <div className="mt-4 pt-4 border-t border-blue-200">
                    <button
                      onClick={handleRecognize}
                      disabled={isRecognizing}
                      className="w-full px-4 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 disabled:opacity-50 flex justify-center items-center"
                    >
                      {isRecognizing ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Analyzing Image...
                        </>
                      ) : (
                        '🔍 Recognize Product'
                      )}
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Recognition Results */}
            {recognitionData && (
              <div className="bg-indigo-50 px-6 py-6 border-t border-indigo-200">
                <div className="flex justify-between items-center mb-4">
                  <h4 className="text-xl font-bold text-indigo-900 flex items-center">
                    <span className="mr-2">🤖</span> AI Analysis Results
                  </h4>
                  <span className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-semibold border border-indigo-200">
                    Confidence: {(recognitionData.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                
                <div className="space-y-4">
                  {/* Primary Category */}
                  <div>
                    <p className="text-sm font-semibold text-indigo-800 mb-1">Detected Category</p>
                    <p className="text-lg font-bold text-gray-900 capitalize border-b pb-2">
                      {recognitionData.category.replace(/_/g, ' ')}
                    </p>
                  </div>
                  
                  {/* Keywords */}
                  {recognitionData.keywords && recognitionData.keywords.length > 0 && (
                    <div>
                      <p className="text-sm font-semibold text-indigo-800 mb-2">Relevant Keywords</p>
                      <div className="flex flex-wrap gap-2">
                        {recognitionData.keywords.map((keyword, idx) => (
                          <span key={idx} className="px-3 py-1 bg-white shadow-sm border border-indigo-100 text-indigo-700 text-sm rounded-full capitalize">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Alternative Predictions */}
                  {recognitionData.top_predictions && recognitionData.top_predictions.length > 1 && (
                    <div className="mt-4 pt-4 border-t border-indigo-200 border-dashed">
                      <p className="text-sm font-semibold text-indigo-800 mb-2">Alternative Predictions</p>
                      <ul className="space-y-1 text-sm text-gray-700 grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {recognitionData.top_predictions.slice(1).map((pred, idx) => (
                          <li key={idx} className="flex justify-between items-center bg-white/50 px-3 py-2 rounded">
                            <span className="capitalize text-gray-800 truncate pr-2" title={pred.label}>
                              {pred.label.replace(/_/g, ' ')}
                            </span>
                            <span className="text-indigo-600 font-medium whitespace-nowrap">
                              {(pred.score * 100).toFixed(1)}%
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Empty State Message */}
      {!preview && (
        <p className="text-center text-gray-500 mt-8 text-sm">
          No image selected yet. Try dragging an image or clicking "Browse Files"
        </p>
      )}
    </div>
  );
}
