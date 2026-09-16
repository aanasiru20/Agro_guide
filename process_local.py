import os
import json
import pandas as pd
import soundfile as sf

# Path to the parquet file you downloaded from Hugging Face
parquet_path = "hausa_test.parquet"  # Update filename if yours is named differently

print("Reading local parquet file...")
df = pd.read_parquet(parquet_path)

os.makedirs("data/audio", exist_ok=True)
ground_truths = {}

sample_size = min(50, len(df))
print(f"Extracting {sample_size} audio clips...")

for i in range(sample_size):
    row = df.iloc[i]
    audio_info = row["audio"]
    
    # Extract audio bytes / array and sampling rate
    audio_data = audio_info["bytes"] if "bytes" in audio_info else audio_info["array"]
    sample_rate = audio_info.get("sampling_rate", 16000)
    
    transcript = row.get("transcription", row.get("text", ""))
    
    filename = f"hausa_clip_{i}.wav"
    file_path = os.path.join("data", "audio", filename)
    
    # Save audio clip
    if isinstance(audio_data, bytes):
        with open(file_path, "wb") as f:
            f.write(audio_data)
    else:
        sf.write(file_path, audio_data, sample_rate)
        
    ground_truths[filename] = transcript

# Save ground truths
with open("data/ground_truths.json", "w", encoding="utf-8") as f:
    json.dump(ground_truths, f, indent=4)

print("✅ Extracted audio clips and created data/ground_truths.json successfully!")