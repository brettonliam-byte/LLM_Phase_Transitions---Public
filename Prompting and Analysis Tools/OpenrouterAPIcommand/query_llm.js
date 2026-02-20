const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// 1. Load Environment Variables
try {
    process.loadEnvFile(path.join(__dirname, '../../.env'));
} catch (e) {
    console.warn("Warning: Could not load .env file via process.loadEnvFile");
}

const CONFIG_PATH = path.join(__dirname, './llm_config.json');
const OUTPUT_DIR = path.join(__dirname, './llm_outputs');
const PYTHON_SCRIPT = path.join(__dirname, './update_excel.py');

// --- PROVIDER HANDLERS ---
const PROVIDERS = {
    openrouter: {
        url: "https://openrouter.ai/api/v1/chat/completions",
        getHeaders: (key) => ({
            "Authorization": `Bearer ${key}`,
            "Content-Type": "application/json"
        }),
        formatBody: (config) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt },
                { role: "user", content: config.user_prompt }
            ],
            temperature: config.temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 2) : undefined
        })
    },
    openai: {
        url: "https://api.openai.com/v1/chat/completions",
        getHeaders: (key) => ({
            "Authorization": `Bearer ${key}`,
            "Content-Type": "application/json"
        }),
        formatBody: (config) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt },
                { role: "user", content: config.user_prompt }
            ],
            temperature: config.temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 2) : undefined
        })
    },
    ollama: {
        url: (process.env.OLLAMA_BASE_URL || "http://localhost:11434/v1") + "/chat/completions",
        getHeaders: () => ({
            "Content-Type": "application/json"
        }),
        formatBody: (config) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt },
                { role: "user", content: config.user_prompt }
            ],
            temperature: config.temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 2) : undefined
        })
    },
    anthropic: {
        url: "https://api.anthropic.com/v1/messages",
        getHeaders: (key) => ({
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }),
        formatBody: (config) => ({
            model: config.model,
            system: config.system_prompt,
            messages: [
                { role: "user", content: config.user_prompt }
            ],
            temperature: config.temperature,
            max_tokens: config.max_tokens
        })
    },
    google: {
        url: "https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
        getHeaders: () => ({
            "Content-Type": "application/json"
        }),
        formatBody: (config) => ({
            contents: [{
                role: "user",
                parts: [{ text: config.system_prompt + "\n\n" + config.user_prompt }] 
            }],
            generationConfig: {
                temperature: config.temperature,
                maxOutputTokens: config.max_tokens,
                responseLogprobs: config.logprobs
            }
        })
    }
};

async function runQuery() {
    // 1. Load Configuration
    if (!fs.existsSync(CONFIG_PATH)) {
        console.error("Error: llm_config.json not found!");
        return;
    }
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    const providerName = config.provider?.toLowerCase() || 'openrouter';
    
    let iterations = parseInt(config.N);
    if (isNaN(iterations) || iterations < 1) iterations = 1;

    console.log(`\n--- Querying ${providerName.toUpperCase()} : ${config.model} ---`);
    console.log(`Iterations: ${iterations}`);
    console.log(`Prompt: "${config.user_prompt.substring(0, 50)}"...`);

    // 2. Validate Provider
    const provider = PROVIDERS[providerName];
    if (!provider) {
        console.error(`Error: Unknown provider '${providerName}'. Supported: ${Object.keys(PROVIDERS).join(', ')}`);
        return;
    }

    // 3. Get API Key
    let apiKey = "";
    if (providerName === 'openrouter') apiKey = process.env.OPENROUTER_API_KEY;
    if (providerName === 'openai') apiKey = process.env.OPENAI_API_KEY;
    if (providerName === 'anthropic') apiKey = process.env.ANTHROPIC_API_KEY;
    if (providerName === 'google') apiKey = process.env.GOOGLE_API_KEY;

    if (!apiKey && providerName !== 'ollama') {
        console.error(`Error: Missing API key for ${providerName.toUpperCase()} in .env file.`);
        return;
    }

    // Prepare Output Directory
    if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

    // Store responses for Excel export
    const accumulatedResponses = [];

    // 4. Loop N times
    for (let i = 1; i <= iterations; i++) {
        process.stdout.write(`\rProcessing Iteration ${i}/${iterations}...`);

        let url = provider.url;
        if (providerName === 'google') {
            url = url.replace('{MODEL}', config.model).replace('{KEY}', apiKey);
        }

        const requestBody = provider.formatBody(config);
        
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: provider.getHeaders(apiKey),
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

            if (!response.ok) {
                console.error("\nAPI Error:", JSON.stringify(data, null, 2));
                accumulatedResponses.push("Error: " + JSON.stringify(data));
                continue; 
            }

            // Normalize
            let content = "";
            if (providerName === 'google') {
                content = data.candidates?.[0]?.content?.parts?.[0]?.text;
            } else if (providerName === 'anthropic') {
                content = data.content?.[0]?.text;
            } else {
                content = data.choices?.[0]?.message?.content;
            }

            const finalText = content || "(No text returned)";
            accumulatedResponses.push(finalText);

            // Optional: Small delay
            if (iterations > 1 && i < iterations) {
                await new Promise(resolve => setTimeout(resolve, 1000)); 
            }

        } catch (error) {
            console.error("\nExecution Error:", error.message);
            accumulatedResponses.push("Error: " + error.message);
        }
    }
    
    console.log("\n\nAll iterations complete. Exporting to Excel...");

    // 5. Hand off to Python for Excel Export
    if (config.excel_file) {
        const tempJsonPath = path.join(OUTPUT_DIR, `temp_excel_data_${Date.now()}.json`);
        
        // Resolve excel path (handle relative paths)
        let excelPath = config.excel_file;
        if (!path.isAbsolute(excelPath)) {
            excelPath = path.join(__dirname, excelPath);
        }

        const payload = {
            excel_file: excelPath,
            prompt: config.user_prompt,
            model: config.model,
            timestamp: new Date().toISOString(),
            responses: accumulatedResponses
        };

        fs.writeFileSync(tempJsonPath, JSON.stringify(payload, null, 2));

        exec(`python "${PYTHON_SCRIPT}" "${tempJsonPath}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing python script: ${error.message}`);
                console.error(stderr);
            } else {
                console.log(stdout);
            }
            // Cleanup temp file
            try { fs.unlinkSync(tempJsonPath); } catch (e) {}
        });

    } else {
        console.warn("Warning: 'excel_file' not specified in config. No Excel file updated.");
        // Fallback: dump to console or log
        console.log("Responses:", accumulatedResponses);
    }
}

runQuery();