interface DataDisplayProps {
  data: any;
}

export function DataDisplay({ data }: DataDisplayProps) {
  if (!data) return null;

  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'object') return JSON.stringify(value);
    return String(value);
  };

  const getFieldLabel = (key: string): string => {
    const labels: Record<string, string> = {
      attestation_number: 'Attestation Number',
      importateur: 'Importateur',
      exporter: 'Exporter',
      forwarding_agent: 'Forwarding Agent',
      transport_id: 'Transport ID',
      cbm: 'CBM (Cubic Meters)',
      gross_weight: 'Gross Weight (Kg)',
      feri_number: 'FERI Number',
      transitaire: 'Transitaire',
      bl: 'Bill of Lading',
    };
    return labels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="mt-8 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">Extracted Data</h2>
        <p className="text-sm text-gray-600 mt-1">Data successfully extracted from your PDF</p>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(data).map(([key, value]) => (
            <div key={key} className="bg-gray-50 rounded-lg p-4">
              <dt className="text-sm font-medium text-gray-500 mb-1">
                {getFieldLabel(key)}
              </dt>
              <dd className="text-sm text-gray-900 font-medium">
                {formatValue(value)}
              </dd>
            </div>
          ))}
        </div>
        
        {Object.keys(data).length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="mt-2">No data extracted</p>
          </div>
        )}
      </div>
    </div>
  );
}
