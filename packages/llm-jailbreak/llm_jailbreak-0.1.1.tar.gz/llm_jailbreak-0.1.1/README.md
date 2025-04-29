# LLM Jailbreak Testing Toolkit

A Python package for testing jailbreak vulnerabilities in large language models (LLMs).

## Features

- Supports multiple LLM models (LLaMA-2, Vicuna, WizardLM, etc.)
- Configurable testing parameters
- Automatic model downloading
- Attack success rate calculation
- Easy to extend with new algorithms

## Installation

```bash
pip install autodan
```

Or install from source:
```bash
git clone https://github.com/yourusername/autodan.git
cd autodan
pip install -e .
```

## Usage

### Basic Usage

```python
from autodan import AutoDAN, AutoDANConfig

# Create config with custom model
config = AutoDANConfig(
    model_name="vicuna",
    api_key="your_openai_key"  # optional for prompt mutation
)

# Run full pipeline
autodan = AutoDAN(config)
results = autodan.run()

print(f"Attack Success Rate: {results['asr']}")
```

### Configuration Options

Key configuration parameters:

- `model_name`: Name of model to test (llama2, vicuna, etc.)
- `api_key`: OpenAI API key for prompt mutation (optional)
- `device`: CUDA device index (default: 0)
- `num_steps`: Number of optimization steps (default: 100)
- `batch_size`: Batch size for evaluation (default: 256)
- `dataset_path`: Path to harmful behaviors dataset

See `AutoDANConfig` class for all available options.

## Data Files

The package includes:
- Harmful behaviors dataset (`data/advbench/harmful_behaviors.csv`)
- Initial prompts (`assets/autodan_initial_prompt.txt`)
- Prompt templates (`assets/prompt_group.pth`)

## License

MIT

## Acknowledge

The core code comes from [AutoDAN](https://github.com/SheltonLiu-N/AutoDAN), I just expand and package it.
If there are any infringement issues, first, I would like express my apology, second, contact me with email and I will delete it.
I do this because I am preparing a project now, and I need to use these great code conveniently.
