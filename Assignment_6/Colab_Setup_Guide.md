# Assignment 6: Fine-tuning Mistral with LoRA on Google Colab

This directory contains the code to fine-tune `Mistral-7B-Instruct` using **QLoRA** (Quantized Low-Rank Adaptation) and the HuggingFace ecosystem (`peft`, `trl`, `transformers`).

Because fine-tuning a 7B parameter model requires significant GPU VRAM, this code is specifically optimized to run on **Google Colab** (using the free T4 GPU or the premium A100).

## 🚀 How to Run on Google Colab

### Step 1: Create a New Notebook
1. Go to [Google Colab](https://colab.research.google.com/).
2. Click **File -> New Notebook**.
3. Go to **Runtime -> Change runtime type**.
4. Select **T4 GPU** (or A100 if you have Colab Pro).

### Step 2: Install Dependencies
Create the first cell in your notebook and paste the following commands to install the necessary HuggingFace libraries:
```python
!pip install -q -U transformers==4.38.2
!pip install -q -U peft==0.9.0
!pip install -q -U trl==0.7.11
!pip install -q -U accelerate==0.27.2
!pip install -q -U bitsandbytes==0.42.0
!pip install -q -U datasets==2.18.0 scipy
```

### Step 3: Run the Fine-Tuning Script
Create a second cell, copy the entire contents of the `finetune_mistral_lora.py` file from this folder, and paste it into the cell. 

Run the cell. The script will automatically:
1. Download the `timdettmers/openassistant-guanaco` instruction dataset.
2. Load the `Mistral-7B` model in 4-bit precision (saving massive amounts of RAM).
3. Inject the LoRA adapters into the attention modules.
4. Train the model using the `SFTTrainer`.
5. Save the fine-tuned adapter to the `/results` folder.

### Step 4: Export your Model
Once training completes, you can zip the results folder and download your fine-tuned LoRA adapter:
```python
import shutil
shutil.make_archive('lora_adapter', 'zip', 'Mistral-7B-Instruct-Guanaco-LoRA')
from google.colab import files
files.download('lora_adapter.zip')
```

---
**Note:** The script is currently configured to run for `max_steps=100` as a proof-of-concept to verify the pipeline works without waiting hours. To do a full fine-tuning run, comment out the `max_steps=100` parameter in the `TrainingArguments` section of the script.
