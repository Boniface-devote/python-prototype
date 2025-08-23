'use client';

import { useState } from 'react';
import { UploadForm } from '@/components/UploadForm';
import { DataDisplay } from '@/components/DataDisplay';
import { DownloadSection } from '@/components/DownloadSection';
import { Header } from '@/components/Header';

export default function Home() {
  const [extractedData, setExtractedData] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isModified, setIsModified] = useState(false);

  const handleProcessingStart = () => {
    setIsProcessing(true);
    setError(null);
  };

  const handleProcessingComplete = (data: any, modified: boolean) => {
    setExtractedData(data);
    setIsModified(modified);
    setIsProcessing(false);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        <UploadForm 
          onProcessingStart={handleProcessingStart}
          onProcessingComplete={handleProcessingComplete}
          onError={handleError}
          isProcessing={isProcessing}
        />

        {isProcessing && (
          <div className="mt-8 flex justify-center">
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Processing PDF...</h3>
              <p className="text-gray-600">Please wait while we extract and process your data</p>
            </div>
          </div>
        )}

        {extractedData && (
          <DataDisplay data={extractedData} />
        )}

        {isModified && (
          <DownloadSection />
        )}
      </main>
    </div>
  );
}
