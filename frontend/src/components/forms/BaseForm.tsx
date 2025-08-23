'use client';

import { useFormData } from '@/hooks/useFormData';
import { FileUpload } from '../FileUpload';
import { TemplateSelector } from '../TemplateSelector';

interface BaseFormProps {
  pdfType: string;
  templates: string[];
  onProcessingStart: () => void;
  onProcessingComplete: (data: any, modified: boolean) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
  children?: React.ReactNode;
}

export function BaseForm({ 
  pdfType, 
  templates, 
  onProcessingStart, 
  onProcessingComplete, 
  onError, 
  isProcessing,
  children 
}: BaseFormProps) {
  const { formData, updateField } = useFormData();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.pdfFile) {
      onError('Please select a PDF file');
      return;
    }

    onProcessingStart();

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('pdf_file', formData.pdfFile);
      
      if (formData.templateFile) {
        formDataToSend.append('template_file', formData.templateFile);
      }
      
      if (formData.freightNumber) {
        formDataToSend.append('freight_number', formData.freightNumber);
      }
      
      if (formData.containerType) {
        formDataToSend.append('container_type', formData.containerType);
      }
      
      if (formData.numContainers) {
        formDataToSend.append('num_containers', formData.numContainers);
      }

      const response = await fetch(`/api/process/${pdfType}`, {
        method: 'POST',
        body: formDataToSend,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Processing failed');
      }

      const result = await response.json();
      
      if (result.error) {
        onError(result.error);
      } else {
        onProcessingComplete(result.data, result.modified);
      }
    } catch (error) {
      onError(error instanceof Error ? error.message : 'An error occurred during processing');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* PDF Upload */}
        <div className="lg:col-span-2">
          <FileUpload
            onFileSelect={(file) => updateField('pdfFile', file)}
            acceptedTypes=".pdf"
            label="PDF File"
            required
          />
        </div>

        {/* Template Selection */}
        <div>
          <TemplateSelector
            templates={templates}
            value={formData.templateFile}
            onChange={(value) => updateField('templateFile', value)}
            label="Excel Template (Optional)"
          />
        </div>

        {/* Freight Number */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Freight Number
          </label>
          <input
            type="number"
            min="1"
            step="1"
            placeholder="e.g., 200, 250, 500"
            value={formData.freightNumber}
            onChange={(e) => updateField('freightNumber', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          />
        </div>

        {/* Additional Form Fields */}
        {children}
      </div>

      {/* Submit Button */}
      <div className="pt-4">
        <button
          type="submit"
          disabled={isProcessing || !formData.pdfFile}
          className={`
            w-full px-6 py-3 text-white font-medium rounded-lg transition-all duration-200
            ${isProcessing || !formData.pdfFile
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
            }
          `}
        >
          {isProcessing ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : (
            'Upload and Process'
          )}
        </button>
      </div>
    </form>
  );
}
