import { BaseForm } from './BaseForm';

interface NormalFormProps {
  onProcessingStart: () => void;
  onProcessingComplete: (data: any, modified: boolean) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
}

export function NormalForm(props: NormalFormProps) {
  // Mock templates - in real app, these would come from the backend
  const templates = [
    'Corporate Legends Limited.xlsx',
    'PROFORMA_INVOICE_1x20.xlsx',
    'PROFORMA_INVOICE_1x40.xlsx',
    'PROFORMA_INVOICE.xlsx',
    'RHO LOGISTICS AND FREIGHT FORWARDER.xlsx'
  ];

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload Normal FERI PDF</h2>
        <p className="text-gray-600">Process standard FERI documents with optional Excel template integration</p>
      </div>
      
      <BaseForm
        pdfType="normal"
        templates={templates}
        {...props}
      />
    </div>
  );
}
