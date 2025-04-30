# LLM Jailbreak Testing Toolkit

A Python package for testing jailbreak vulnerabilities in large language models (LLMs).

## Features

- Supports multiple LLM models (LLaMA-2, Vicuna, WizardLM, DeepSeek, etc.)
- Includes AutoDAN and MasterKey algorithms
- Configurable testing parameters
- Automatic model downloading
- Attack success rate calculation
- Modular design for easy extension

## Installation

### Basic Installation

```bash
pip install llm_jailbreak
```

### Algorithm-Specific Installation

```bash
# Install only AutoDAN
pip install llm_jailbreak[autodan]

# Install only MasterKey 
pip install llm_jailbreak[masterkey]

# Install all algorithms
pip install llm_jailbreak[all]
```

### From Source

```bash (not finish yet)
git clone https://github.com/WodenJay/llm_jailbreak.git
cd llm_jailbreak
pip install -e .[all]  # or [autodan]/[masterkey]
```

## Usage

### AutoDAN Usage

```python
from autodan import AutoDAN, AutoDANConfig

config = AutoDANConfig(
    model_name="vicuna",
    api_key="your_deepseek_key"
)
autodan = AutoDAN(config)
results = autodan.run()
```

### MasterKey Usage  

```python
from masterkey import MasterKey, MasterKeyConfig

config = MasterKeyConfig(
    api_key="your_deepseek_key",
    model_name="deepseek-chat"
)
masterkey = MasterKey(config)
results = masterkey.run()
```

### Command Line

```bash
# Run AutoDAN
autodan --api-key your_deepseek_key --model vicuna

# Run MasterKey
masterkey --api-key your_deepseek_key --model deepseek-chat
```

### Configuration Options

#### AutoDAN Config

- `model_name`: Name of model to test (llama2, vicuna, etc.)
- `api_key`: DeepSeek API key for prompt mutation (optional)
- `device`: CUDA device index (default: 0)
- `num_steps`: Number of optimization steps (default: 100)
- `batch_size`: Batch size for evaluation (default: 256)
- `dataset_path`: Path to harmful behaviors dataset

#### MasterKey Config

- `api_key`: DeepSeek API key (required)
- `model_name`: Model name (default: "deepseek-chat")
- `max_retries`: Maximum retry attempts (default: 3)
- `timeout`: Request timeout in seconds (default: 30)
- `temperature`: Generation temperature (default: 0.7)

See `AutoDANConfig` and `MasterKeyConfig` classes for all available options.

## Data Files

The package includes:

- Harmful behaviors dataset (`data/advbench/harmful_behaviors.csv`)
- Initial prompts (`assets/autodan_initial_prompt.txt`)
- Prompt templates (`assets/prompt_group.pth`)

## License

MIT

## Acknowledge

The core code comes from [AutoDAN](https://github.com/SheltonLiu-N/AutoDAN) [MasterKey](https://github.com/LLMSecurity/MasterKey), I just expand and package it.
If there are any infringement issues, first, I would like express my apology, second, contact me with email and I will delete it.
I do this because I am preparing a project now, and I need to use these great code conveniently.
