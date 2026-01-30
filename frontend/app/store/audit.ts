'use client';

import { create } from 'zustand';

interface AuditState {
  auditId: string | null;
  status: 'idle' | 'uploading' | 'pending' | 'analyzing' | 'completed' | 'failed';
  progress: number;
  error: string | null;
  auditData: any | null;

  setAuditId: (id: string) => void;
  setStatus: (status: AuditState['status']) => void;
  setProgress: (progress: number) => void;
  setError: (error: string | null) => void;
  setAuditData: (data: any) => void;
  reset: () => void;
}

export const useAuditStore = create<AuditState>((set) => ({
  auditId: null,
  status: 'idle',
  progress: 0,
  error: null,
  auditData: null,

  setAuditId: (id) => set({ auditId: id }),
  setStatus: (status) => set({ status }),
  setProgress: (progress) => set({ progress }),
  setError: (error) => set({ error }),
  setAuditData: (data) => set({ auditData: data }),
  reset: () => set({
    auditId: null,
    status: 'idle',
    progress: 0,
    error: null,
    auditData: null,
  }),
}));
