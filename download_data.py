import os
import json
import soundfile as sf
from datasets import load_dataset
from dotenv import load_dotenv

# 1. Load your Hugging Face token
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    print("⚠️ HUGGINGFACE_TOKEN is missing in your .env file!")
    exit()

print("Downloading official AfriSwitch dataset (Hausa) from Hugging Face...")

# 2. Download the gated dataset (This will work now that you have access!)
iterable_dataset = load_dataset(
    "intronhealth/AfriSwitch",
    "hausa",
    split="test",
    token=hf_token,
    streaming=True,
)

os.makedirs("data/audio", exist_ok=True)
ground_truths = {}

# 3. Save the first 50 samples for a fast benchmark
sample_size = 50
print(f"Saving up to {sample_size} audio files and transcripts...")

for i, item in enumerate(iterable_dataset.take(sample_size)):
    audio_data = item["audio"]["array"]
    sample_rate = item["audio"]["sampling_rate"]
    
    # AfriSwitch uses the 'transcription' column for text
    transcript = item["transcription"] 
    
    audio_id = f"hausa_clip_{i}.wav"
    file_path = f"data/audio/{audio_id}"
    
    sf.write(file_path, audio_data, sample_rate)
    ground_truths[audio_id] = transcript

# 4. Save the ground truth text file
with open("data/ground_truths.json", "w", encoding="utf-8") as f:
    json.dump(ground_truths, f, indent=4)

print("✅ Official AfriSwitch Data successfully downloaded!")