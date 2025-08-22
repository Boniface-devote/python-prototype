import { useState } from 'react';

interface FormData {
  pdfFile: File | null;
  templateFile: string;
  freightNumber: string;
  containerType: string;
  numContainers: string;
}

export function useFormData() {
  const [formData, setFormData] = useState<FormData>({
    pdfFile: null,
    templateFile: '',
    freightNumber: '',
    containerType: '',
    numContainers: '1'
  });

  const updateField = (field: keyof FormData, value: string | File | null) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const resetForm = () => {
    setFormData({
      pdfFile: null,
      templateFile: '',
      freightNumber: '',
      containerType: '',
      numContainers: '1'
    });
  };

  return {
    formData,
    updateField,
    resetForm
  };
}
