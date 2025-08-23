interface TabButtonProps {
  isActive: boolean;
  onClick: () => void;
  icon: string;
  label: string;
}

export function TabButton({ isActive, onClick, icon, label }: TabButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`
        flex-1 flex items-center justify-center space-x-2 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200
        ${isActive 
          ? 'bg-blue-50 text-blue-700 border border-blue-200 shadow-sm' 
          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
        }
      `}
    >
      <span className="text-lg">{icon}</span>
      <span className="hidden sm:inline">{label}</span>
    </button>
  );
}
