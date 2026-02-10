# **Command Interpreter**

Summary of results
@Diego o @Adan

## Local Model Finetuning

### Overview

The finetuning process was initially conducted on a cloud environment inside Google Colab, but was later transitioned to a local setup to avoid the limitations of Colab's free tier, such as session timeouts and GPU availability. The local setup utilized a powerful GPU, which significantly improved the training speed and allowed for more extensive experimentation.

### Environment Setup

To facilitate the finetuning process, a [Dockerfile](https://github.com/RoBorregos/home-pipelines/blob/main/hri/command_interpreter/training_pipeline/local-finetuning/Dockerfile) was created to ensure a consistent environment across different machines. This Dockerfile included all necessary dependencies and configurations, allowing for easy setup and reproducibility of the finetuning process. To further streamline the process, a [docker-compose](https://github.com/RoBorregos/home-pipelines/blob/main/hri/command_interpreter/training_pipeline/local-finetuning/docker-compose.yaml) file was also created, which simplified the confirguration of the runtime and volume mounts.
The main dependencies included in the Dockerfile were:

- Python 3.11
- CUDA 12.6
- Unsloth
- Llama.cpp

> **Note:** Llama.cpp had to be built from source and one of the output binaries had to be copied to another directory to ensure compatibility with unsloth.

### Finetuning Process

The finetuning process is all contained in the finetune-llama.py script. This script is designed to be run inside the Docker container, ensuring that all dependencies are correctly configured. You can see a more in-depth explanation of the finetuning process in the [finetuning documentation](https://github.com/RoBorregos/frida-cortex/tree/main/fine_tuning). The finetuning process involves several key steps:

1. **Data Preparation**: The dataset is prepared in a specific format that the model can understand. This includes tokenization and formatting of the input data.
2. **Model Configuration**: The model is configured with specific parameters such as learning rate, batch size, and number of epochs.
3. **Training**: The model is trained on the prepared dataset using the specified parameters.
4. **Saving the Model**: The trained model is saved for later use, allowing it to be deployed in various applications. It is important to note that the model is saved in multiple quantization formats, to optimize the memory usage and performance.

Comparison to online finetuning
@Ivan

Dataset generator
@Oscar

Schema Aligned Parsing for command interpreter
@Adan

Embeddings and RAG for grounding commands
@Leo @Joce

Areas of improvement
@any

Link of paper
(Once available)
