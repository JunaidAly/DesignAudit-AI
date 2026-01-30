'use client';

import React, { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, AlertTriangle, Info, Download, Share2 } from 'lucide-react';

interface Violation {
  id: string;
  category: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  suggestion: string;
  affected_elements: string[];
  guideline_reference: string;
}

interface AuditReportProps {
  violations: Violation[];
  summary: string;
  detailedFeedback: string;
  improvements: any[];
  quickWins: string[];
}

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'critical':
      return 'bg-red-50 border-red-200 text-red-800';
    case 'high':
      return 'bg-orange-50 border-orange-200 text-orange-800';
    case 'medium':
      return 'bg-yellow-50 border-yellow-200 text-yellow-800';
    case 'low':
      return 'bg-blue-50 border-blue-200 text-blue-800';
    default:
      return 'bg-gray-50 border-gray-200 text-gray-800';
  }
};

const getSeverityIcon = (severity: string) => {
  switch (severity) {
    case 'critical':
      return <AlertCircle className="text-red-600" size={20} />;
    case 'high':
      return <AlertTriangle className="text-orange-600" size={20} />;
    case 'medium':
      return <AlertTriangle className="text-yellow-600" size={20} />;
    case 'low':
      return <Info className="text-blue-600" size={20} />;
    default:
      return <Info className="text-gray-600" size={20} />;
  }
};

export default function AuditReport({ violations, summary, detailedFeedback, improvements, quickWins }: AuditReportProps) {
  const [filter, setFilter] = useState<string>('all');

  const filteredViolations = filter === 'all' ? violations : violations.filter((v) => v.severity === filter);

  const stats = {
    total: violations.length,
    critical: violations.filter((v) => v.severity === 'critical').length,
    high: violations.filter((v) => v.severity === 'high').length,
    medium: violations.filter((v) => v.severity === 'medium').length,
    low: violations.filter((v) => v.severity === 'low').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Audit Report</h2>
            <p className="text-gray-600 mt-2">{summary}</p>
          </div>
          <div className="flex gap-2">
            <button className="p-2 hover:bg-gray-100 rounded-lg transition">
              <Download size={20} />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-lg transition">
              <Share2 size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {[
          { label: 'Total Issues', value: stats.total, color: 'text-gray-600' },
          { label: 'Critical', value: stats.critical, color: 'text-red-600' },
          { label: 'High', value: stats.high, color: 'text-orange-600' },
          { label: 'Medium', value: stats.medium, color: 'text-yellow-600' },
          { label: 'Low', value: stats.low, color: 'text-blue-600' },
        ].map((stat) => (
          <div key={stat.label} className="card text-center">
            <p className="text-3xl font-bold" style={{ color: stat.color.replace('text-', '') }}>
              {stat.value}
            </p>
            <p className="text-sm text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Quick Wins */}
      {quickWins.length > 0 && (
        <div className="card border-l-4 border-green-500">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <CheckCircle className="text-green-600" size={24} />
            Quick Wins
          </h3>
          <ul className="space-y-2">
            {quickWins.map((win, idx) => (
              <li key={idx} className="flex items-start gap-3">
                <span className="text-green-600 font-bold">✓</span>
                <span className="text-gray-700">{win}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Filter & Violations */}
      <div className="card">
        <div className="mb-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Issues by Severity</h3>
          <div className="flex gap-2 flex-wrap">
            {['all', 'critical', 'high', 'medium', 'low'].map((sev) => (
              <button
                key={sev}
                onClick={() => setFilter(sev)}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  filter === sev
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {sev.charAt(0).toUpperCase() + sev.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          {filteredViolations.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No issues in this category</p>
          ) : (
            filteredViolations.map((violation) => (
              <div key={violation.id} className={`border rounded-lg p-4 ${getSeverityColor(violation.severity)}`}>
                <div className="flex gap-3">
                  {getSeverityIcon(violation.severity)}
                  <div className="flex-1">
                    <h4 className="font-bold text-lg">{violation.title}</h4>
                    <p className="text-sm mt-1 opacity-90">{violation.description}</p>
                    <div className="mt-3 space-y-2 text-sm">
                      <p>
                        <strong>Suggestion:</strong> {violation.suggestion}
                      </p>
                      <p>
                        <strong>Reference:</strong> {violation.guideline_reference}
                      </p>
                    </div>
                    {violation.affected_elements.length > 0 && (
                      <p className="text-sm mt-2">
                        <strong>Affected:</strong> {violation.affected_elements.join(', ')}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Detailed Feedback */}
      {detailedFeedback && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Analysis</h3>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 whitespace-pre-wrap">{detailedFeedback}</p>
          </div>
        </div>
      )}

      {/* Improvements */}
      {improvements.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Recommended Improvements</h3>
          <div className="space-y-4">
            {improvements.map((improvement, idx) => (
              <div key={idx} className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-bold text-gray-900">{improvement.area}</h4>
                <p className="text-sm text-gray-600 mt-1">{improvement.issue}</p>
                <p className="text-sm text-gray-700 mt-2">
                  <strong>Impact:</strong> {improvement.impact}
                </p>
                <p className="text-sm text-gray-700 mt-2">
                  <strong>Recommendation:</strong> {improvement.recommendation}
                </p>
                <div className="mt-2 inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">
                  {improvement.priority}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
