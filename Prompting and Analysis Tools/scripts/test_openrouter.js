async function testOpenRouter() {
    const apiKey = process.env.OPENROUTER_API_KEY;

    if (!apiKey || apiKey === 'your_actual_key_goes_here') {
        console.error("Error: OPENROUTER_API_KEY is not set correctly in your .env file.");
        process.exit(1);
    }

    console.log("Testing OpenRouter API connection...");

    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "google/gemini-2.0-flash-001",
                messages: [
                    { role: "user", content: "Say 'Connection Successful!'" }
                ]
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Response:", data.choices[0].message.content);
        } else {
            console.error("API Error:", data.error || data);
        }
    } catch (error) {
        console.error("Fetch Error:", error.message);
    }
}

testOpenRouter();
