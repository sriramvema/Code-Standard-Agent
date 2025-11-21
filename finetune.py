import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)

from datasets import load_dataset
from peft import LoraConfig, get_peft_model

MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-base" 
DATASET_PATH = "dataset/"  

dataset = load_dataset("json", data_files={
    "train": f"{DATASET_PATH}/train.json",
    "val": f"{DATASET_PATH}/val.json"
})

def format_example(example):
    prompt = f"<messy>\n{example['messy_code']}\n</messy>\n<clean>"
    completion = f"{example['clean_code']}</clean>"
    return {"text": prompt + completion}

dataset = dataset.map(format_example)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

def tokenize(example):
    return tokenizer(
        example["text"], 
        truncation=True, 
        max_length=2048,
        padding="max_length"
    )

tokenized = dataset.map(tokenize, batched=True, remove_columns=dataset["train"].column_names)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True,     # QLoRA (optional, saves GPU memory)
    trust_remote_code=True
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir="./code-standard-agent",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    logging_dir="./logs",
    logging_steps=50,
    save_steps=500,
    learning_rate=2e-4,
    num_train_epochs=3,
    bf16=torch.cuda.is_available(),
    eval_strategy="epoch",
    save_total_limit=2,
    report_to="none",
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["val"],
    data_collator=data_collator,
)

trainer.train()

trainer.save_model("./deepseek-coder-cleaner-lora")
