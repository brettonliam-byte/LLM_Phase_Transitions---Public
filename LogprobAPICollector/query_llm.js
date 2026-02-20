const fs = require('fs');
const path = require('path');

// 1. Load Environment Variables from root .env
try {
    const envPath = path.join(__dirname, '../.env');
    if (fs.existsSync(envPath)) {
        require('dotenv').config({ path: envPath });
    } else {
        console.warn("Warning: .env file not found at " + envPath);
    }
} catch (e) {
    console.warn("Warning: Could not load .env file: " + e.message);
}

const CONFIG_PATH = path.join(__dirname, './llm_config.json');
const OUTPUT_DIR = path.join(__dirname, './llm_outputs');

// --- PROVIDER HANDLERS ---
const PROVIDERS = {
    openrouter: {
        url: "https://openrouter.ai/api/v1/chat/completions",
        getHeaders: (key) => ({
            "Authorization": `Bearer ${key}`,
            "Content-Type": "application/json"
        }),
        formatBody: (config, temperature) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt || "" },
                { role: "user", content: config.user_prompt }
            ],
            temperature: temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 5) : undefined
        })
    },
    openai: {
        url: "https://api.openai.com/v1/chat/completions",
        getHeaders: (key) => ({
            "Authorization": `Bearer ${key}`,
            "Content-Type": "application/json"
        }),
        formatBody: (config, temperature) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt || "" },
                { role: "user", content: config.user_prompt }
            ],
            temperature: temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 5) : undefined
        })
    },
    ollama: {
        url: (process.env.OLLAMA_BASE_URL || "http://localhost:11434/v1") + "/chat/completions",
        getHeaders: () => ({
            "Content-Type": "application/json"
        }),
        formatBody: (config, temperature) => ({
            model: config.model,
            messages: [
                { role: "system", content: config.system_prompt || "" },
                { role: "user", content: config.user_prompt }
            ],
            temperature: temperature,
            max_tokens: config.max_tokens,
            logprobs: config.logprobs,
            top_logprobs: config.logprobs ? (config.top_logprobs || 5) : undefined
        })
    }
};

async function runExperiment(config, index, total) {
    const providerName = config.provider?.toLowerCase() || 'openrouter';
    const iterations = parseInt(config.N) || 1;
    const tempRange = config.temperature_range || { start: 0, end: 0, step: 1 };
    
    console.log(`\n[${index}/${total}] Experiment: ${providerName.toUpperCase()} : ${config.model}`);
    if (config.system_prompt) {
        console.log(`System Prompt: "${config.system_prompt.substring(0, 50)}${config.system_prompt.length > 50 ? '...' : ''}"`);
    }
    console.log(`User Prompt: "${config.user_prompt.substring(0, 50)}..."`);

    // 2. Validate Provider
    const provider = PROVIDERS[providerName];
    if (!provider) {
        console.error(`Error: Provider '${providerName}' not supported.`);
        return;
    }

    // 3. Get API Key
    let apiKey = "";
    if (providerName === 'openrouter') apiKey = process.env.OPENROUTER_API_KEY;
    if (providerName === 'openai') apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey && providerName !== 'ollama') {
        console.error(`Error: Missing API key for ${providerName.toUpperCase()} in .env file.`);
        return;
    }

    const allResults = {
        config: config,
        timestamp: new Date().toISOString(),
        experiments: []
    };

    const temps = [];
    for (let t = tempRange.start; t <= tempRange.end + 0.00001; t += tempRange.step) {
        temps.push(parseFloat(t.toFixed(4)));
    }

    for (const temp of temps) {
        console.log(`\n  Temperature: ${temp}`);
        const tempResults = {
            temperature: temp,
            iterations: []
        };

        for (let i = 1; i <= iterations; i++) {
            process.stdout.write(`    Iteration ${i}/${iterations}... `);
            
            try {
                const response = await fetch(provider.url, {
                    method: "POST",
                    headers: provider.getHeaders(apiKey),
                    body: JSON.stringify(provider.formatBody(config, temp))
                });

                const data = await response.json();

                if (!response.ok) {
                    console.error(`\nAPI Error: ${response.status} - ${JSON.stringify(data)}`);
                    tempResults.iterations.push({ iteration: i, error: data });
                    continue;
                }

                const choice = data.choices?.[0];
                const result = {
                    iteration: i,
                    text: choice?.message?.content || "",
                    logprobs: choice?.logprobs || null,
                    finish_reason: choice?.finish_reason
                };

                tempResults.iterations.push(result);
                console.log("Done.");
                await new Promise(resolve => setTimeout(resolve, 500));

            } catch (error) {
                console.error(`\nFetch Error: ${error.message}`);
                tempResults.iterations.push({ iteration: i, error: error.message });
            }
        }
        allResults.experiments.push(tempResults);
    }

    // 5. Save results with unique filename logic
    let outputFile = config.output_file || path.join(OUTPUT_DIR, `logprobs_${Date.now()}.json`);
    let absoluteOutputPath = path.isAbsolute(outputFile) ? outputFile : path.join(__dirname, outputFile);
    
    if (fs.existsSync(absoluteOutputPath)) {
        const ext = path.extname(absoluteOutputPath);
        const base = absoluteOutputPath.slice(0, -ext.length);
        let counter = 1;
        while (fs.existsSync(`${base}_${counter}${ext}`)) {
            counter++;
        }
        absoluteOutputPath = `${base}_${counter}${ext}`;
    }

    fs.writeFileSync(absoluteOutputPath, JSON.stringify(allResults, null, 2));
    console.log(`\nResults saved to: ${absoluteOutputPath}`);
}

async function runQueue() {
    if (!fs.existsSync(CONFIG_PATH)) {
        console.error("Error: llm_config.json not found!");
        return;
    }
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    const experiments = config.experiments;

    if (!Array.isArray(experiments)) {
        console.error("Error: 'experiments' must be an array in llm_config.json");
        return;
    }

    if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

    console.log(`\nStarting Queue: ${experiments.length} experiments found.`);

    for (let i = 0; i < experiments.length; i++) {
        await runExperiment(experiments[i], i + 1, experiments.length);
    }

    console.log("\nAll experiments in queue complete.");
}

runQueue();
