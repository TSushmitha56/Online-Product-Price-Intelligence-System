import { useState, useRef } from 'react';
import api from '../api/axios';

export default function ImageUpload({ onProductRecognized }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragActive, setIsDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploadedData, setUploadedData] = useState(null);
  const [isRecognizing, setIsRecognizing] = useState(false);
  const [recognitionData, setRecognitionData] = useState(null);
  const fileInputRef = useRef(null);

  // ... (Keep existing logic functions: handleFileSelect, handleDragOver, etc. exactly the same) ...
  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (event) => setPreview(event.target.result);
      reader.readAsDataURL(file);
      setUploadStatus(null);
      setUploadedData(null);
      setRecognitionData(null);
    } else {
      setUploadStatus({ type: 'error', message: 'Please select a valid image file (JPEG, PNG, WebP)' });
    }
  };

  const handleDragOver = (e) => { e.preventDefault(); e.stopPropagation(); setIsDragActive(true); };
  const handleDragLeave = (e) => { e.preventDefault(); e.stopPropagation(); setIsDragActive(false); };
  const handleDrop = (e) => {
    e.preventDefault(); e.stopPropagation(); setIsDragActive(false);
    if (e.dataTransfer.files?.length > 0) handleFileSelect(e.dataTransfer.files[0]);
  };
  const handleClick = () => fileInputRef.current?.click();
  const handleInputChange = (e) => { if (e.target.files?.[0]) handleFileSelect(e.target.files[0]); };

  const handleUpload = async () => {
    if (!selectedImage) return;
    setIsUploading(true); setUploadStatus(null);
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      const response = await api.post('/upload-image/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const data = response.data;
      
      setUploadStatus({ type: 'success', message: 'Image uploaded successfully!' });
      setUploadedData({
        image_id: data.image_id,
        original_filename: data.original_filename,
        file_size_mb: data.file_size_mb,
        timestamp: new Date(data.timestamp).toLocaleString()
      });
    } catch (error) {
      const msg = error.response?.data?.message || error.response?.data?.detail || `Upload failed: ${error.message}`;
      setUploadStatus({ type: 'error', message: msg });
    } finally { setIsUploading(false); }
  };

  const handleRecognize = async () => {
    if (!uploadedData?.image_id) return;
    setIsRecognizing(true); setUploadStatus(null); setRecognitionData(null);
    try {
      const response = await api.post('/recognize-product/', { image_id: uploadedData.image_id });
      const data = response.data;
      
      setRecognitionData(data.recognition);
      if (onProductRecognized) {
        const query = data.recognition.keywords?.[0] || data.recognition.category?.replace(/_/g, ' ');
        if (query) onProductRecognized(query);
      }
    } catch (error) {
      const msg = error.response?.data?.message || error.response?.data?.detail || `Recognition failed: ${error.message}`;
      setUploadStatus({ type: 'error', message: msg });
    } finally { setIsRecognizing(false); }
  };

  const handleClear = () => {
    setSelectedImage(null); setPreview(null); setUploadStatus(null);
    setUploadedData(null); setRecognitionData(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4">

      {/* Header */}
      <div className="text-center mb-10">
        <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
          Visual Product Search
        </h2>
        <p className="text-lg text-gray-500">
          Upload an image to find the best deals across the web instantly.
        </p>
      </div>

      {/* Main Card */}
      <div className="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 overflow-hidden transition-all">

        {/* Upload Area */}
        {!preview ? (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={handleClick}
            className={`
              relative flex flex-col items-center justify-center p-16 text-center cursor-pointer transition-all duration-300 group
              ${isDragActive
                ? 'bg-indigo-50/50 border-2 border-dashed border-indigo-400'
                : 'bg-white border-2 border-dashed border-gray-200 hover:border-indigo-300 hover:bg-gray-50/50'
              }
            `}
          >
            <div className={`w-20 h-20 rounded-full flex items-center justify-center mb-6 transition-transform group-hover:scale-110 duration-300 ${isDragActive ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-50 text-gray-400'}`}>
              <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>

            <h3 className="text-xl font-bold text-gray-900 mb-2">Drop your image here</h3>
            <p className="text-gray-500 mb-6 max-w-xs mx-auto">
              Support for JPG, PNG and WebP. Max file size 10MB.
            </p>

            <button className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-full shadow-lg shadow-indigo-200 transition-all hover:-translate-y-0.5">
              Browse Files
            </button>

            <input ref={fileInputRef} type="file" accept="image/*" onChange={handleInputChange} className="hidden" />
          </div>
        ) : (
          /* Preview & Actions Area */
          <div className="flex flex-col md:flex-row">

            {/* Left: Image Preview */}
            <div className="w-full md:w-1/2 bg-gray-50 p-6 flex flex-col justify-center items-center relative border-b md:border-b-0 md:border-r border-gray-100">
              <div className="relative group w-full h-64 md:h-full flex items-center justify-center rounded-2xl overflow-hidden bg-white shadow-sm border border-gray-200">
                <img src={preview} alt="Preview" className="max-w-full max-h-full object-contain" />

                {/* Remove Button (Hover) */}
                <button
                  onClick={(e) => { e.stopPropagation(); handleClear(); }}
                  className="absolute top-3 right-3 p-2 bg-white/90 backdrop-blur-sm rounded-full text-gray-500 hover:text-red-500 shadow-sm opacity-0 group-hover:opacity-100 transition-all transform hover:scale-110"
                  title="Remove Image"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              {/* File Info Pill */}
              <div className="mt-4 flex gap-4 text-xs text-gray-500 font-medium">
                <span className="bg-white px-3 py-1 rounded-full border border-gray-200 shadow-sm">
                  {selectedImage.size < 1024 * 1024
                    ? `${(selectedImage.size / 1024).toFixed(0)} KB`
                    : `${(selectedImage.size / 1024 / 1024).toFixed(2)} MB`}
                </span>
                <span className="bg-white px-3 py-1 rounded-full border border-gray-200 shadow-sm uppercase">
                  {selectedImage.type.split('/')[1]}
                </span>
              </div>
            </div>

            {/* Right: Actions & Results */}
            <div className="w-full md:w-1/2 p-8 flex flex-col">

              {/* Step 1: Upload Status */}
              <div className="mb-6">
                {!uploadedData ? (
                  <div className="text-center md:text-left">
                    <h4 className="text-lg font-bold text-gray-900 mb-2">1. Upload Image</h4>
                    <p className="text-sm text-gray-500 mb-4">Send this image to our secure server to begin analysis.</p>
                    <button
                      onClick={handleUpload}
                      disabled={isUploading}
                      className={`w-full py-3 rounded-xl font-bold text-sm shadow-md transition-all ${isUploading
                        ? 'bg-gray-100 text-gray-400 cursor-wait'
                        : 'bg-gray-900 text-white hover:bg-black hover:shadow-lg hover:-translate-y-0.5'
                        }`}
                    >
                      {isUploading ? (
                        <span className="flex items-center justify-center gap-2">
                          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                          Uploading...
                        </span>
                      ) : 'Upload Image'}
                    </button>
                  </div>
                ) : (
                  <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100 flex items-center gap-3">
                    <div className="bg-emerald-100 p-2 rounded-full text-emerald-600">
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-emerald-800">Upload Complete</h4>
                      <p className="text-xs text-emerald-600">ID: {uploadedData.image_id.substring(0, 12)}...</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Step 2: Recognition */}
              {uploadedData && (
                <div className="flex-grow animate-fade-in-up">
                  {!recognitionData ? (
                    <div className="text-center md:text-left">
                      <h4 className="text-lg font-bold text-gray-900 mb-2">2. Analyze Product</h4>
                      <p className="text-sm text-gray-500 mb-4">Identify the product category and find similar items.</p>
                      <button
                        onClick={handleRecognize}
                        disabled={isRecognizing}
                        className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-all hover:-translate-y-0.5 flex items-center justify-center gap-2"
                      >
                        {isRecognizing ? (
                          <>
                            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            Analyzing...
                          </>
                        ) : (
                          <>
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                            Identify Product
                          </>
                        )}
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {/* Main Result */}
                      <div className="bg-gradient-to-br from-indigo-50 to-violet-50 p-5 rounded-2xl border border-indigo-100">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Detected</span>
                          <span className="px-2 py-1 bg-white text-indigo-600 text-xs font-bold rounded-md shadow-sm">
                            {(recognitionData.confidence * 100).toFixed(0)}% Match
                          </span>
                        </div>
                        <h3 className="text-2xl font-black text-indigo-900 capitalize leading-tight mb-3">
                          {recognitionData.category.replace(/_/g, ' ')}
                        </h3>

                        {/* Keyword Chips */}
                        <div className="flex flex-wrap gap-2">
                          {recognitionData.keywords?.slice(0, 3).map((keyword, idx) => (
                            <span key={idx} className="px-2.5 py-1 bg-white/60 text-indigo-700 text-xs font-semibold rounded-md border border-indigo-100/50">
                              #{keyword}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Top Predictions List */}
                      {recognitionData.top_predictions?.length > 1 && (
                        <div>
                          <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Alternatives</p>
                          <div className="space-y-2">
                            {recognitionData.top_predictions.slice(1, 3).map((pred, idx) => (
                              <div key={idx} className="flex items-center justify-between text-sm">
                                <span className="text-gray-600 capitalize">{pred.label.replace(/_/g, ' ')}</span>
                                {/* Simple Progress Bar */}
                                <div className="flex items-center gap-2 w-24">
                                  <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                    <div className="h-full bg-gray-400 rounded-full" style={{ width: `${pred.score * 100}%` }}></div>
                                  </div>
                                  <span className="text-xs text-gray-400 w-6 text-right">{(pred.score * 100).toFixed(0)}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* Error Message Toast */}
              {uploadStatus?.type === 'error' && (
                <div className="mt-4 p-3 bg-red-50 text-red-700 text-sm rounded-lg border border-red-100 flex items-start gap-2 animate-shake">
                  <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  <span>{uploadStatus.message}</span>
                </div>
              )}

            </div>
          </div>
        )}
      </div>
    </div>
  );
}