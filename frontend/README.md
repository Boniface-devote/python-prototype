# PDF Data Extractor - Modern Frontend

A beautiful, modern Next.js frontend for the PDF Data Extractor application. This frontend provides an intuitive user interface for processing FERI PDFs while maintaining all the functionality of the original Flask backend.

## Features

- 🎨 **Modern UI/UX**: Beautiful, responsive design with Tailwind CSS
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- 🚀 **Fast Performance**: Built with Next.js 15 and React 19
- 🔄 **Real-time Processing**: Live feedback during PDF processing
- 📁 **Drag & Drop**: Intuitive file upload with drag and drop support
- 🎯 **Smart Forms**: Context-aware forms for different PDF types
- 💾 **File Downloads**: Easy download of processed Excel and PDF files

## PDF Types Supported

1. **LABAN PDFs** - Standard FERI documents
2. **MALABA PDFs** - Maritime FERI documents with container specs
3. **POSSIANO PDFs** - Possiano-specific FERI documents
4. **BUSIA PDFs** - Busia-specific FERI documents

## Getting Started

### Prerequisites

- Node.js 18+ 
- Python 3.8+ (for the Flask backend)
- Flask backend running on port 5000

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Building for Production

```bash
npm run build
npm start
```

## Architecture

### Components Structure

```
src/
├── app/
│   ├── api/                    # API routes for backend communication
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Main page
├── components/
│   ├── forms/                 # Form components for each PDF type
│   │   ├── BaseForm.tsx       # Base form with common functionality
│   │   ├── NormalForm.tsx     # LABAN PDF form
│   │   ├── MaritimeForm.tsx   # MALABA PDF form
│   │   ├── BusiaForm.tsx      # BUSIA PDF form
│   │   └── PossianoForm.tsx   # POSSIANO PDF form
│   ├── FileUpload.tsx         # Drag & drop file upload
│   ├── TemplateSelector.tsx   # Excel template selection
│   ├── DataDisplay.tsx        # Extracted data display
│   ├── DownloadSection.tsx    # File download section
│   ├── Header.tsx             # Application header
│   ├── TabButton.tsx          # Tab navigation button
│   └── UploadForm.tsx         # Main upload form container
└── hooks/
    └── useFormData.ts         # Form state management hook
```

### Key Features

- **Form State Management**: Custom hook for managing form data across components
- **API Integration**: Seamless communication with Flask backend
- **Error Handling**: Comprehensive error handling and user feedback
- **Loading States**: Beautiful loading indicators during processing
- **File Validation**: PDF file type validation and size display

## API Endpoints

The frontend communicates with the Flask backend through these endpoints:

- `POST /api/process/{type}` - Process PDF files
- `GET /api/download_excel` - Download processed Excel files
- `GET /api/download_pdf` - Download processed PDF files

## Styling

Built with **Tailwind CSS 4** for:
- Responsive design
- Beautiful gradients and shadows
- Smooth animations and transitions
- Consistent spacing and typography
- Dark/light mode ready

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

### Code Style

- TypeScript for type safety
- ESLint for code quality
- Prettier for code formatting
- Component-based architecture

### Adding New Features

1. Create new components in the `components/` directory
2. Add new API routes in `app/api/`
3. Update types and interfaces as needed
4. Test thoroughly across different PDF types

## Troubleshooting

### Common Issues

1. **Backend Connection Error**: Ensure Flask backend is running on port 5000
2. **File Upload Issues**: Check file size and type restrictions
3. **Template Loading**: Verify template files exist in the backend directories

### Debug Mode

Enable debug logging by setting `NODE_ENV=development` and check browser console for detailed error messages.

## Contributing

1. Follow the existing code structure
2. Add TypeScript types for new features
3. Test with different PDF types
4. Ensure mobile responsiveness
5. Update documentation as needed

## License

This project maintains the same license as the main application.
