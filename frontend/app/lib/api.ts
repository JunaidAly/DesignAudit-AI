'use client';

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
});

export const auditApi = {
  upload: async (file: File, onProgress?: (progress: number) => void) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/audits/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress?.(progress);
        }
      },
    });

    return response.data;
  },

  getAudit: async (auditId: string) => {
    const response = await apiClient.get(`/audits/${auditId}`);
    return response.data;
  },

  listAudits: async (limit = 20, offset = 0) => {
    const response = await apiClient.get('/audits', { params: { limit, offset } });
    return response.data;
  },

  askQuestion: async (auditId: string, question: string) => {
    const response = await apiClient.post(`/audits/${auditId}/chat`, { question });
    return response.data;
  },
};

export default apiClient;
