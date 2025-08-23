export function DownloadSection() {
  const handleDownload = async (type: 'excel' | 'pdf') => {
    try {
      const response = await fetch(`/api/download_${type}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = type === 'excel' ? 'proforma_invoice.xlsx' : 'proforma_invoice.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Download failed. Please try again.');
    }
  };

  return (
    <div className="mt-8 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-green-50 to-emerald-50 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">Downloads Available</h2>
        <p className="text-sm text-gray-600 mt-1">Your processed files are ready for download</p>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Excel Download */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Excel File</h3>
                <p className="text-sm text-gray-600">Modified template with extracted data</p>
              </div>
            </div>
            <button
              onClick={() => handleDownload('excel')}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Download Excel
            </button>
          </div>

          {/* PDF Download */}
          <div className="bg-gradient-to-r from-red-50 to-pink-50 rounded-lg p-6 border border-red-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">PDF File</h3>
                <p className="text-sm text-gray-600">Generated PDF with processed data</p>
              </div>
            </div>
            <button
              onClick={() => handleDownload('pdf')}
              className="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors font-medium"
            >
              Download PDF
            </button>
          </div>
        </div>
        
        <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <div className="flex items-start space-x-3">
            <svg className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="text-sm text-amber-800">
                <strong>Note:</strong> Files are automatically named based on the extracted data. 
                Make sure to save them with appropriate names for your records.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
