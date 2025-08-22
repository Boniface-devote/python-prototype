import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ type: string }> }
) {
  try {
    // Await the params promise in Next.js 15
    const { type } = await params;
    const formData = await request.formData();
    
    // Forward the request to the Flask backend
    const flaskResponse = await fetch(`http://localhost:5000/api/process/${type}`, {
      method: 'POST',
      body: formData,
    });

    if (!flaskResponse.ok) {
      const errorData = await flaskResponse.json();
      return NextResponse.json(
        { error: errorData.error || 'Processing failed' },
        { status: flaskResponse.status }
      );
    }

    const result = await flaskResponse.json();
    
    if (result.error) {
      return NextResponse.json(
        { error: result.error },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      data: result.data,
      modified: result.modified,
    });

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
