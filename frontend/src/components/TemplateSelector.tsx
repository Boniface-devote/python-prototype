interface TemplateSelectorProps {
  templates: string[];
  value: string;
  onChange: (value: string) => void;
  label: string;
}

export function TemplateSelector({ templates, value, onChange, label }: TemplateSelectorProps) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
      >
        <option value="">Select a template (optional)</option>
        {templates.map((template) => (
          <option key={template} value={template}>
            {template}
          </option>
        ))}
      </select>
      {templates.length === 0 && (
        <p className="text-xs text-gray-500 mt-1">No templates available</p>
      )}
    </div>
  );
}
