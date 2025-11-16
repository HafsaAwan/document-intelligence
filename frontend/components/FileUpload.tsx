'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File as FileIcon, Loader2 } from 'lucide-react';

// Define the props our component will accept
interface FileUploadProps {
  onUploadSuccess: (filename: string) => void;
  onUploadError: (error: string) => void;
}

export function FileUpload({ onUploadSuccess, onUploadError }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Reset states
    setIsUploading(true);
    setUploadError(null);

    // --- THIS IS THE REAL UPLOAD LOGIC ---
    try {
      const formData = new FormData();
      formData.append('file', file);

      console.log('Starting real file upload...');

      const response = await fetch('document-intelligence-production-6269.up.railway.app/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        // Try to parse the error message from the backend
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      console.log('Upload successful:', result);
      onUploadSuccess(result.filename); // Pass the filename to the parent
      
    } catch (error: any) {
      const errorMsg = error.message || 'An unknown error occurred';
      console.error('Upload error:', errorMsg);
      setUploadError(errorMsg);
      onUploadError(errorMsg);
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess, onUploadError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed border-gray-300 rounded-xl p-12 text-center text-gray-500 cursor-pointer
                  transition-all duration-300 ease-in-out 
                  ${isDragActive ? 'border-blue-500 bg-blue-50' : 'hover:border-gray-400 hover:bg-gray-50'}
                  ${uploadError ? 'border-red-500 bg-red-50' : ''}`}
    >
      <input {...getInputProps()} />
      
      {isUploading ? (
        <div className="flex flex-col items-center justify-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-500" />
          <p className="mt-4 text-lg">Processing...</p>
          <p className="text-sm">This may take a moment.</p>
        </div>
      ) : uploadError ? (
        <div className="flex flex-col items-center justify-center text-red-600">
          <FileIcon className="h-12 w-12" />
          <p className="mt-4 text-lg font-semibold">Upload Failed</p>
          <p className="text-sm">{uploadError}</p>
          <p className="mt-2 text-xs">Please try another file.</p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center">
          <UploadCloud className="h-12 w-12 text-gray-400" />
          <p className="mt-4 text-lg">
            {isDragActive ? 'Drop the file here ...' : 'Drag & drop PDF here, or click to select'}
          </p>          
          <p className="text-sm">Only .pdf files are supported</p>
        </div>
      )}
    </div>
  );
}