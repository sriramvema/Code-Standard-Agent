# DeepSeek Code Cleaner — Fine-Tuned Code-Quality Model

This project builds a fine-tuned **DeepSeek Coder** model capable of taking raw “messy” Python code and generating a **clean, standardized, and fully equivalent** Python version. The goal is to help developers maintain clean, Pythonic, and professional-quality code while preserving functional behavior.

---

## Project Overview

This project fine-tunes a DeepSeek Coder model using **PyTorch**, **HuggingFace Transformers**, and **LoRA/QLoRA**.  
The model learns to:

- Detect common code anti-patterns  
- Recognize messy or poorly structured Python code  
- Produce clean, PEP-8–aligned replacements  
- Maintain *identical functional behavior*  

Training uses a 2,600-example paired “messy → clean” dataset synthesized with **Claude Haiku** and validated to guarantee functional equivalence.

---

## Dataset

### **Dataset Size:**  
**2,600 paired examples** (`messy_code` → `clean_code`)

### **How the dataset was generated**
I built a custom synthetic dataset generator using Claude models:

- **Claude Sonnet** produces intentionally messy Python code:
  - Bad variable names  
  - Dead code  
  - Misleading comments  
  - Redundant logic  
  - Indentation issues  
  - Unnecessary variables  
- **Claude Haiku** rewrites the messy code using strict rules:
  - Must preserve *exact behavior*  
  - Must not modify algorithms, return values, or logic  
  - Only structural and stylistic improvements allowed  


## Dataset Generation Script

The `generation.py` creates synthetic pairs using Claude Sonnet + Haiku with behavior-preservation constraints.

Key features:
- Messy code generator  
- Clean code generator  
- JSON + JSONL writing  
- Automatic appending to existing dataset  

---

## Model Finetuning

The training uses:

- **DeepSeek Coder 1.3B Base**
- **PyTorch**
- **HuggingFace Transformers**
- **LoRA** via `peft` (efficient parameter tuning)
- **QLoRA** (4-bit quantization for GPU efficiency)
