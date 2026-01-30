'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import AuditReport from '@/app/components/AuditReport';
import ChatInterface from '@/app/components/ChatInterface';
import { auditApi } from '@/app/lib/api';

interface AuditData {
  id: string;
  status: string;
  created_at: string;
  inspector: any;
  analyst: any;
  advisor: any;
}

export default function AuditPage() {
  const params = useParams();
  const auditId = params.id as string;
  const [audit, setAudit] = useState<AuditData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAudit = async () => {
      try {
        const data = await auditApi.getAudit(auditId);
        setAudit(data);

        if (data.status !== 'completed' && data.status !== 'failed') {
          // Poll for updates if not completed
          const timer = setTimeout(fetchAudit, 2000);
          return () => clearTimeout(timer);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load audit');
      } finally {
        setLoading(false);
      }
    };

    fetchAudit();
  }, [auditId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="animate-spin mx-auto mb-4 text-blue-600" size={40} />
          <p className="text-xl text-gray-700">Analyzing your design...</p>
          <p className="text-sm text-gray-500 mt-2">This typically takes 30-60 seconds</p>
        </div>
      </div>
    );
  }

  if (error || !audit) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-4xl mx-auto">
          <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
            <ArrowLeft size={20} />
            Back to Upload
          </Link>
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-xl text-red-600">Error: {error || 'Audit not found'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={20} />
          New Audit
        </Link>

        {audit.status === 'pending' && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 flex items-center gap-3">
            <Loader2 className="animate-spin text-yellow-600" size={20} />
            <p className="text-yellow-800">Analysis in progress...</p>
          </div>
        )}

        {audit.status === 'failed' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">Analysis failed. Please try uploading again.</p>
          </div>
        )}

        {audit.status === 'completed' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <AuditReport
                  violations={audit.analyst?.violations || []}
                  summary={audit.advisor?.summary || ''}
                  detailedFeedback={audit.advisor?.detailed_feedback || ''}
                  improvements={audit.advisor?.improvements || []}
                  quickWins={audit.advisor?.quick_wins || []}
                />
              </div>
              <div>
                <ChatInterface auditId={auditId} />
              </div>
            </div>

            {/* Design Preview */}
            {audit.inspector && (
              <div className="card mt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Design Analysis</h3>
                <div className="bg-gray-100 rounded p-4">
                  <pre className="text-xs overflow-auto max-h-96 text-gray-600">
                    {JSON.stringify(audit.inspector, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
