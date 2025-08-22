import { BaseForm } from './BaseForm';
import { useFormData } from '@/hooks/useFormData';

interface PossianoFormProps {
  onProcessingStart: () => void;
  onProcessingComplete: (data: any, modified: boolean) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
}

export function PossianoForm(props: PossianoFormProps) {
  const { formData, updateField } = useFormData();
  
  // Mock templates - in real app, these would come from the backend
  const templates = [
    'PROFORMA ponsiano 1x40.xlsx',
    'PROFORMA ponsiano normal.xlsx'
  ];

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload Possiano PDF</h2>
        <p className="text-gray-600">Process Possiano FERI documents with container specifications</p>
      </div>
      
      <BaseForm
        pdfType="possiano"
        templates={templates}
        {...props}
      >
        {/* Container Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Container Type
          </label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="radio"
                name="container_type"
                value="40FT"
                checked={formData.containerType === '40FT'}
                onChange={(e) => updateField('containerType', e.target.value)}
                className="mr-2 text-blue-600 focus:ring-blue-500"
              />
              1×40FT
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="container_type"
                value="20FT"
                checked={formData.containerType === '20FT'}
                onChange={(e) => updateField('containerType', e.target.value)}
                className="mr-2 text-blue-600 focus:ring-blue-500"
              />
              1×20FT
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="container_type"
                value=""
                checked={formData.containerType === ''}
                onChange={(e) => updateField('containerType', e.target.value)}
                className="mr-2 text-blue-600 focus:ring-blue-500"
              />
              None
            </label>
          </div>
        </div>

        {/* Number of Containers */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Containers
          </label>
          <input
            type="number"
            min="1"
            step="1"
            value={formData.numContainers}
            placeholder="Default: 1"
            onChange={(e) => updateField('numContainers', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          />
        </div>
      </BaseForm>
    </div>
  );
}
