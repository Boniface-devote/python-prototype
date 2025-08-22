'use client';

import { useState } from 'react';
import { TabButton } from './TabButton';
import { NormalForm } from './forms/NormalForm';
import { MaritimeForm } from './forms/MaritimeForm';
import { BusiaForm } from './forms/BusiaForm';
import { PossianoForm } from './forms/PossianoForm';

type TabType = 'normal' | 'maritime' | 'possiano' | 'busia';

interface UploadFormProps {
  onProcessingStart: () => void;
  onProcessingComplete: (data: any, modified: boolean) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
}

export function UploadForm({ onProcessingStart, onProcessingComplete, onError, isProcessing }: UploadFormProps) {
  const [activeTab, setActiveTab] = useState<TabType>('normal');

  const tabs = [
    { id: 'normal', label: 'LABAN PDFs', icon: '📄' },
    { id: 'maritime', label: 'MALABA PDFs', icon: '🚢' },
    { id: 'possiano', label: 'POSSIANO PDFs', icon: '📋' },
    { id: 'busia', label: 'BUSIA PDFs', icon: '🏢' },
  ] as const;

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-1 p-1">
          {tabs.map((tab) => (
            <TabButton
              key={tab.id}
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id as TabType)}
              icon={tab.icon}
              label={tab.label}
            />
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'normal' && (
          <NormalForm
            onProcessingStart={onProcessingStart}
            onProcessingComplete={onProcessingComplete}
            onError={onError}
            isProcessing={isProcessing}
          />
        )}
        
        {activeTab === 'maritime' && (
          <MaritimeForm
            onProcessingStart={onProcessingStart}
            onProcessingComplete={onProcessingComplete}
            onError={onError}
            isProcessing={isProcessing}
          />
        )}
        
        {activeTab === 'possiano' && (
          <PossianoForm
            onProcessingStart={onProcessingStart}
            onProcessingComplete={onProcessingComplete}
            onError={onError}
            isProcessing={isProcessing}
          />
        )}
        
        {activeTab === 'busia' && (
          <BusiaForm
            onProcessingStart={onProcessingStart}
            onProcessingComplete={onProcessingComplete}
            onError={onError}
            isProcessing={isProcessing}
          />
        )}
      </div>
    </div>
  );
}
