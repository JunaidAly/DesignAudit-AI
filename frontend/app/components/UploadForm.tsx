'use client';

import React, { useState } from 'react';
import { Upload, AlertCircle } from 'lucide-react';
import { useAuditStore } from '@/app/store/audit';
import { auditApi } from '@/app/lib/api';
import { formatBytes } from '@/app/lib/utils';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function UploadForm() {
  const [isDragActive, setIsDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const { setAuditId, setStatus, setProgress, setError } = useAuditStore();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleFile = async (files: FileList) => {
    const selectedFile = files[0];

    if (!selectedFile) return;

    if (!['image/png', 'image/jpeg', 'image/webp'].includes(selectedFile.type)) {
      setError('Invalid file type. Please upload PNG, JPG, or WebP');
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(`File too large. Maximum size is ${formatBytes(MAX_FILE_SIZE)}`);
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    handleDrag(e);
    if (e.dataTransfer.files) {
      handleFile(e.dataTransfer.files);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFile(e.target.files);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setStatus('uploading');
      setError(null);

      const result = await auditApi.upload(file, (progress: number) => {
        setProgress(progress);
      });

      setAuditId(result.audit_id);
      setStatus('pending');
      setProgress(0);

      // Redirect to results page
      window.location.href = `/audit/${result.audit_id}`;
    } catch (error) {
      setStatus('failed');
      setError(error instanceof Error ? error.message : 'Upload failed');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h1 className="text-4xl font-bold text-center mb-2 text-gray-900">DesignAudit AI</h1>
          <p className="text-center text-gray-600 mb-8">Your AI-Powered Design Team Member</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-xl p-8 text-center transition cursor-pointer ${
                isDragActive
                  ? 'border-blue-500 bg-blue-50'
                  : file
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-300 hover:border-blue-500'
              }`}
            >
              <Upload className={`mx-auto mb-4 ${isDragActive || file ? 'text-blue-600' : 'text-gray-400'}`} size={48} />
              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={handleChange}
                className="hidden"
                id="file-input"
              />
              <label htmlFor="file-input" className="cursor-pointer block">
                <p className="font-semibold text-gray-900">
                  {file ? file.name : 'Click to upload or drag and drop'}
                </p>
                <p className="text-sm text-gray-500 mt-1">PNG, JPG, or WebP up to {formatBytes(MAX_FILE_SIZE)}</p>
              </label>
            </div>

            {file && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">File:</span> {file.name}
                </p>
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Size:</span> {formatBytes(file.size)}
                </p>
              </div>
            )}

            {useAuditStore.getState().error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
                <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
                <p className="text-sm text-red-700">{useAuditStore.getState().error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={!file || useAuditStore.getState().status === 'uploading'}
              className="btn-primary w-full"
            >
              {useAuditStore.getState().status === 'uploading'
                ? `Uploading... ${useAuditStore.getState().progress}%`
                : 'Analyze Design'}
            </button>

            <p className="text-xs text-gray-500 text-center">
              Analysis typically takes 30-60 seconds. We respect your privacy—images are deleted after analysis.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
