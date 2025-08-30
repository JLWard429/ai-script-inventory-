# AI Models and Tools Inventory

This document provides a comprehensive inventory of all AI, ML, chatbot, and LLM-related models, libraries, and tools present in the `ai-script-inventory` repository.

## Table of Contents

1. [Large Language Models (LLMs)](#large-language-models-llms)
2. [AI Frameworks and SDKs](#ai-frameworks-and-sdks)
3. [Model Hosting and Serving Tools](#model-hosting-and-serving-tools)
4. [Conversational AI Models](#conversational-ai-models)
5. [Specialized AI Tools](#specialized-ai-tools)
6. [Integration Libraries](#integration-libraries)
7. [Development and Testing Tools](#development-and-testing-tools)

## Large Language Models (LLMs)

### OpenAI Models
**Location**: Throughout `ai_tools/`, `documentation/openai_*.md`
**Usage**: Primary LLM provider for various AI tasks

- **GPT-4o**: Advanced language model for complex reasoning tasks
- **GPT-4.5 Preview**: Preview version with enhanced capabilities  
- **GPT-3.5 Turbo**: Faster, cost-effective model for standard tasks
- **O1 Series**: OpenAI's latest reasoning models (O1, O1 Mini)
- **O3 Mini**: Compact version of the O3 model family

**Key Files**:
- `ai_tools/openai.py` - Core OpenAI integration
- `ai_tools/openai_tts.py` - Text-to-speech functionality
- `ai_tools/openai_responses.py` - Response handling
- `documentation/openai_chatcompletions.md` - Chat completions API documentation

### Anthropic Models  
**Location**: `ai_tools/anthropic_*.py`, `documentation/`
**Usage**: Alternative LLM provider focused on safety and reliability

- **Claude 3.7**: Latest Claude model with enhanced capabilities
- **Claude 3.5**: Improved version of Claude 3
- **Claude 3**: Base Claude model for general tasks
- **Claude 3 Opus**: Large-scale Claude variant

**Key Files**:
- `ai_tools/claude.py` - Claude model integration
- `ai_tools/anthropic_claude3_transformation.py` - Claude 3 transformations
- `ai_tools/anthropic_passthrough_logging_handler.py` - Logging integration
- `ai_tools/anthropic_cache_control_hook.py` - Caching mechanisms

### DeepSeek Models
**Location**: Referenced in `documentation/cai_list_of_models.md`
**Usage**: Open-source LLM alternatives

- **DeepSeek V3**: Latest version of DeepSeek model
- **DeepSeek R1**: Reasoning-focused variant

### Meta LLaMA Models
**Location**: `ai_tools/amazon_llama_transformation.py`, documentation
**Usage**: Open-source large language models

- **LLaMA variants**: Through OpenRouter integration
- **Amazon Bedrock LLaMA**: AWS-hosted LLaMA models

### Qwen Models
**Location**: `documentation/cai_list_of_models.md`
**Usage**: Alibaba's open-source language models

- **Qwen2.5 72B**: Large parameter Qwen model
- **Qwen2.5 14B**: Medium-sized Qwen model

## AI Frameworks and SDKs

### CAI SDK (Cybersecurity AI)
**Location**: `documentation/cai_*.md`
**Usage**: Primary AI agent framework for cybersecurity tasks

**Features**:
- Agent orchestration and workflow management
- Multi-model support (300+ models via LiteLLM)
- Tool integration for cybersecurity tasks
- Local and cloud deployment options

**Key Documentation**:
- `documentation/cai_architecture.md` - System architecture
- `documentation/cai_quickstart.md` - Getting started guide
- `documentation/cai_installation.md` - Installation instructions

### LiteLLM
**Location**: `ai_tools/litellm.py`
**Usage**: Unified interface for multiple LLM providers

**Capabilities**:
- 300+ model support across providers
- Standardized API interface
- Cost tracking and usage analytics
- Fallback and load balancing

### AI Orchestra Project
**Location**: `ai_orchestra_project/`
**Usage**: Comprehensive AI service orchestration

**Components**:
- `src/ai_orchestrator.py` - Main orchestration logic
- `src/ai_services/openai_service.py` - OpenAI service wrapper
- `tests/test_ai_integration.py` - Integration testing

## Model Hosting and Serving Tools

### OpenRouter Integration
**Location**: `documentation/cai_list_of_models.md`
**Usage**: Access to hosted models via OpenRouter API

**Supported Models**:
- Meta-LLaMA models
- Various open-source models
- Community-hosted models

### Ollama Integration  
**Location**: `documentation/cai_list_of_models.md`
**Usage**: Local model hosting and serving

**Capabilities**:
- Local model deployment
- Custom model hosting
- Offline AI capabilities

### Amazon Bedrock Models
**Location**: `ai_tools/amazon_*.py`
**Usage**: AWS-hosted AI models

**Models Available**:
- Amazon Titan (multiple variants)
- Claude via Bedrock
- LLaMA via Bedrock
- Cohere models
- AI21 models
- Mistral models
- Stability AI models

**Key Files**:
- `ai_tools/amazon_titan_*.py` - Titan model integrations
- `ai_tools/amazon_cohere_transformation.py` - Cohere integration
- `ai_tools/amazon_ai21_transformation.py` - AI21 integration

## Conversational AI Models

### DialoGPT Models
**Location**: `documentation/hf_conversational_models.txt`
**Usage**: Conversational AI and chatbot development

**Model Variants**:
- Small, Medium, Large DialoGPT models
- Character-specific trained variants (Harry Potter, Rick & Morty, etc.)
- Custom fine-tuned conversational models

**Applications**:
- Discord bots
- Character roleplay bots
- General conversation systems

### Hugging Face Text Generation Models
**Location**: `documentation/hf_text_generation_models.txt`
**Usage**: Text generation and completion tasks

### BlenderBot Models
**Location**: Referenced in conversational models list
**Usage**: Facebook's conversational AI models

- BlenderBot 400M
- BlenderBot 1B
- BlenderBot 3B

## Specialized AI Tools

### Text-to-Speech (TTS)
**Location**: `ai_tools/openai_tts.py`, `documentation/openai_tts.md`
**Usage**: Converting text to speech using OpenAI's TTS models

### Speech-to-Text (STT)
**Location**: `documentation/openai_stt.md`
**Usage**: Converting speech to text using OpenAI's Whisper models

### Code Interpretation
**Location**: `ai_tools/code_interpreter_output_image.py`
**Usage**: AI-powered code analysis and interpretation

### Model Validation and Testing
**Location**: `ai_tools/fake_models.py`, `ai_tools/models.py`
**Usage**: Testing and validation of AI model integrations

## Integration Libraries

### Weights & Biases (wandb)
**Location**: `ai_tools/wandb.py`
**Usage**: Experiment tracking and model monitoring

### MLflow
**Location**: `ai_tools/mlflow.py`
**Usage**: ML lifecycle management and model versioning

### ClearML
**Location**: `ai_tools/clearml.py`
**Usage**: ML experiment management and automation

### LangSmith
**Location**: `ai_tools/langsmith.py`
**Usage**: LangChain application monitoring and debugging

### Argilla
**Location**: `ai_tools/argilla.py`
**Usage**: Data annotation and model evaluation

## Development and Testing Tools

### Model Testing Infrastructure
**Location**: `tests/test_openai_integration.py`
**Usage**: Integration testing for AI models

### Response Handling
**Location**: `ai_tools/*_responses.py`
**Usage**: Processing and validating AI model responses

### Caching and Optimization
**Location**: `ai_tools/*_cache_*.py`
**Usage**: Performance optimization through caching

### Logging and Monitoring
**Location**: `ai_tools/*_logging_*.py`
**Usage**: Comprehensive logging for AI operations

## Configuration and Environment

### Environment Setup
- `.env` file configuration for API keys
- Model selection via environment variables
- Provider-specific configurations

### Key Environment Variables
- `CAI_MODEL` - Primary model selection
- `OPENAI_API_KEY` - OpenAI authentication
- `ANTHROPIC_API_KEY` - Anthropic authentication
- `OPENROUTER_API_KEY` - OpenRouter authentication
- `OLLAMA_API_BASE` - Ollama endpoint configuration

## Security and Privacy

### Local-Only Processing
Many tools support local-only operation to maintain data privacy:
- Ollama for local model hosting
- Local model evaluation tools
- Offline processing capabilities

### API Key Management
Secure handling of API keys and credentials:
- Environment variable-based configuration
- Encrypted storage options
- Key rotation support

## Maintenance and Updates

### Model Version Management
- Regular updates to supported model lists
- Version compatibility checks
- Migration tools for model upgrades

### Documentation Maintenance
- Automated documentation generation
- Model capability documentation
- Usage examples and best practices

---

**Last Updated**: Generated automatically during types module conflict resolution
**Total Models Supported**: 300+ via LiteLLM integration
**Primary Use Cases**: Cybersecurity automation, conversational AI, text processing, code analysis