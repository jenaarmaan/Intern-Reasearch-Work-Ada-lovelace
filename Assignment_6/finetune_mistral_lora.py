import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# -----------------------------------------------------------------------------
# 1. Configuration & Hyperparameters
# -----------------------------------------------------------------------------
# Model from Hugging Face hub (Mistral-7B-Instruct is a great base for fine-tuning)
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
# Dataset (We use a popular instruction-following dataset: OpenAssistant Guanaco)
dataset_name = "timdettmers/openassistant-guanaco"
# Fine-tuned model adapter name
new_model = "Mistral-7B-Instruct-Guanaco-LoRA"

# LoRA parameters
lora_r = 16
lora_alpha = 32
lora_dropout = 0.05

# bitsandbytes parameters (4-bit quantization for QLoRA)
use_4bit = True
bnb_4bit_compute_dtype = "float16"
bnb_4bit_quant_type = "nf4"
use_nested_quant = False

# TrainingArguments parameters
output_dir = "./results"
num_train_epochs = 1
fp16 = False
bf16 = True # Use bf16 if your Colab GPU supports it (A100/V100). Otherwise set fp16=True
per_device_train_batch_size = 4
gradient_accumulation_steps = 4
gradient_checkpointing = True
max_grad_norm = 0.3
learning_rate = 2e-4
weight_decay = 0.001
optim = "paged_adamw_32bit"
lr_scheduler_type = "cosine"
max_steps = 100 # For demonstration purposes. Remove for full fine-tuning.
warmup_ratio = 0.03

# -----------------------------------------------------------------------------
# 2. Setup & Load Model
# -----------------------------------------------------------------------------
print("[INFO] Loading dataset...")
# Load dataset
dataset = load_dataset(dataset_name, split="train")

print("[INFO] Configuring bitsandbytes...")
# Load tokenizer and model with QLoRA configuration
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)

print(f"[INFO] Loading base model: {model_name}...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto" # Automatically loads across available GPUs
)
model.config.use_cache = False
model.config.pretraining_tp = 1

# Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

print("[INFO] Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

# -----------------------------------------------------------------------------
# 3. Setup PEFT (Parameter-Efficient Fine-Tuning)
# -----------------------------------------------------------------------------
print("[INFO] Configuring LoRA...")
peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "lm_head",
    ],
)

# Apply LoRA adapter to the base model
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# -----------------------------------------------------------------------------
# 4. Training
# -----------------------------------------------------------------------------
print("[INFO] Setting up SFTTrainer...")
training_arguments = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=25,
    logging_steps=10,
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=fp16,
    bf16=bf16,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=True,
    lr_scheduler_type=lr_scheduler_type,
    report_to="tensorboard"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=False,
)

print("[INFO] Starting Fine-Tuning...")
trainer.train()

# -----------------------------------------------------------------------------
# 5. Save the Adapter
# -----------------------------------------------------------------------------
print(f"[INFO] Saving LoRA adapter to {new_model}...")
trainer.model.save_pretrained(new_model)
tokenizer.save_pretrained(new_model)

print("[SUCCESS] Fine-tuning complete!")

# -----------------------------------------------------------------------------
# 6. Inference / Testing
# -----------------------------------------------------------------------------
print("[INFO] Testing the fine-tuned model...")
prompt = "### Human: What is the capital of France? ### Assistant:"
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=100)
result = pipe(f"<s>[INST] {prompt} [/INST]")
print(result[0]['generated_text'])
