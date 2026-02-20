"""
Central Configuration for LLM Experiments.
Copy and paste the dictionary blocks in the EXPERIMENTS list to queue up new experiments.
"""

EXPERIMENTS = [
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/gpt-oss:20b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/gemma3:1b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/gemma3:4b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/gemma3:12b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/gemma3:27b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/qwen3:4b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/qwen3:8b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "ollama/deepseek-r1:8b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/allenai/olmo-3.1-32b-think",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/openai/gpt-oss-120b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/alibaba/tongyi-deepresearch-30b-a3b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/tngtech/deepseek-r1t2-chimera",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/nvidia/nemotron-nano-9b-v2",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/nvidia/nemotron-nano-12b-v2-vl",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/qwen/qwen3-vl-235b-a22b-thinking",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/qwen/qwen3-vl-30b-a3b-thinking",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/qwen/qwen3-embedding-4b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/qwen/qwen3-embedding-8b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/qwen/qwen3-next-80b-a3b-thinking",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/x-ai/grok-4.1-fast",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/x-ai/grok-3-mini",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/moonshotai/kimi-k2-thinking",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/z-ai/glm-4.5-air",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meituan/longcat-flash-chat",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/mistralai/mistral-small-3.2-24b-instruct",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/mistralai/ministral-3b-2512",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/mistralai/ministral-14b-2512",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/mistralai/mixtral-8x7b-instruct",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/google/gemini-2.0-flash-001",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/nousresearch/hermes-3-llama-3.1-70b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/nousresearch/hermes-3-llama-3.1-405b:free",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/deepseek/deepseek-r1-0528:free",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/deepseek/deepseek-v3.2",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-3.3-70b-instruct",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-3.2-1b-instruct",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-3.2-3b-instruct",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-guard-3-8b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-guard-4-12b",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/meta-llama/llama-4-scout",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    },
    {
        "prompt": "Solve the following integral: ∫((tan(ln(x)))^3)/x dx.",
        "model": "openrouter/arcee-ai/trinity-mini",
        "temperature_range": {"start": 0.0, "end": 2.0, "step": 0.2},
        "iterations": 20,
        "output_file": "integral_experiment_supreme.xlsx"
    }
]
