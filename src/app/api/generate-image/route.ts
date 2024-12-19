import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { text } = body;

    // TODO: Call your Image Generation API here
    // For now, we'll just echo back the text
    // URL of the web endpoint exposed by your Modal app
    const modalEndpoint = 'https://elishajean84--app-demo-model-generate-dev.modal.run'; 

    // Make a POST request to the Modal service's web endpoint
    const response = await fetch(modalEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: text }), // Pass the text as a prompt to Modal
    });

    // Wait for the response from Modal and return the result
    const result = await response.json();

    return NextResponse.json({
      success: true,
      message: `Received: ${text}`,
      image: result,
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: "Failed to process request" },
      { status: 500 }
    );
  }
}
