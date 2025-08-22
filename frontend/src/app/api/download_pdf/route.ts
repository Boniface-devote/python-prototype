import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Forward the request to the Flask backend
    const flaskResponse = await fetch('http://localhost:5000/download_pdf');

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text();
      return NextResponse.json(
        { error: errorText || 'Download failed' },
        { status: flaskResponse.status }
      );
    }

    // Get the file content
    const fileBuffer = await flaskResponse.arrayBuffer();
    
    // Get the filename from the Flask response headers
    const contentDisposition = flaskResponse.headers.get('content-disposition');
    let filename = 'proforma_invoice.pdf';
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
      if (filenameMatch) {
        filename = filenameMatch[1];
      }
    }

    // Return the file as a response
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${filename}"`,
      },
    });

  } catch (error) {
    console.error('Download API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
