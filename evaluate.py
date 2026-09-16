import os
import json
import time
import requests
import jiwer
from dotenv import load_dotenv
from transformers import pipeline, logging

# 0. Suppress noisy Hugging Face warnings
logging.set_verbosity_error()

# 1. Load API keys from .env
load_dotenv()
sahara_api_key = os.getenv("INTRON_SAHARA_API_KEY")

# 2. Load ground truths mapping
with open("data/ground_truths.json", "r", encoding="utf-8") as f:
    full_data = json.load(f)
    # Take only the first 10 samples for fast execution
    ground_truths = dict(list(full_data.items())[:10])

print("Loading local Whisper models via Transformers (downloading weights if first run)...")

# Load offline Whisper pipelines cleanly
whisper_tiny = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
whisper_base = pipeline("automatic-speech-recognition", model="openai/whisper-base")

def compute_wer(reference, hypothesis):
    """Calculates Word Error Rate using normalized text."""
    if not hypothesis or not reference:
        return 100.0 if reference else 0.0
    
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip()
    ])
    ref_clean = transformation(reference)
    hyp_clean = transformation(hypothesis)
    
    if not ref_clean:
        return 0.0
    return round(jiwer.wer(ref_clean, hyp_clean) * 100, 2)

results = []
total_files = len(ground_truths)

print(f"\n🚀 Starting benchmark for {total_files} audio clips across 3 models...\n")

for idx, (filename, reference) in enumerate(ground_truths.items(), 1):
    audio_path = os.path.join("data", "audio", filename)
    if not os.path.exists(audio_path):
        continue

    # Live progress output
    print(f"[{idx}/{total_files}] Processing {filename}...", end="", flush=True)

    # --- Model 1: Whisper Tiny (Local) ---
    start = time.time()
    try:
        res_tiny = whisper_tiny(audio_path, generate_kwargs={"task": "transcribe"})["text"]
    except Exception:
        res_tiny = ""
    latency_tiny = round(time.time() - start, 3)
    wer_tiny = compute_wer(reference, res_tiny)

    # --- Model 2: Whisper Base (Local) ---
    start = time.time()
    try:
        res_base = whisper_base(audio_path, generate_kwargs={"task": "transcribe"})["text"]
    except Exception:
        res_base = ""
    latency_base = round(time.time() - start, 3)
    wer_base = compute_wer(reference, res_base)

    # --- Model 3: Intron Sahara API ---
    start = time.time()
    res_sahara = ""
    if sahara_api_key:
        try:
            headers = {"Authorization": f"Bearer {sahara_api_key}"}
            with open(audio_path, "rb") as audio_file:
                response = requests.post(
                    "https://api.intron.io/transcribe",
                    headers=headers,
                    files={"file": audio_file},
                    timeout=10
                )
            if response.status_code == 200:
                res_sahara = response.json().get("transcription", "")
        except Exception:
            pass
            
    latency_sahara = round(time.time() - start, 3)
    wer_sahara = compute_wer(reference, res_sahara)

    results.append({
        "file": filename,
        "reference": reference,
        "whisper_tiny": {"transcript": res_tiny, "wer": wer_tiny, "latency_sec": latency_tiny},
        "whisper_base": {"transcript": res_base, "wer": wer_base, "latency_sec": latency_base},
        "intron_sahara": {"transcript": res_sahara, "wer": wer_sahara, "latency_sec": latency_sahara}
    })

    print(f" Done! (Sahara WER: {wer_sahara}%, Base WER: {wer_base}%, Tiny WER: {wer_tiny}%)")

# Compute Average Summary
if results:
    avg_wer_tiny = round(sum(r["whisper_tiny"]["wer"] for r in results) / len(results), 2)
    avg_wer_base = round(sum(r["whisper_base"]["wer"] for r in results) / len(results), 2)
    avg_wer_sahara = round(sum(r["intron_sahara"]["wer"] for r in results) / len(results), 2)

    output_data = {
        "summary": {
            "total_samples": len(results),
            "whisper_tiny_avg_wer": avg_wer_tiny,
            "whisper_base_avg_wer": avg_wer_base,
            "intron_sahara_avg_wer": avg_wer_sahara
        },
        "details": results
    }

    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print("\n✅ Evaluation complete! Results successfully saved to benchmark_results.json")