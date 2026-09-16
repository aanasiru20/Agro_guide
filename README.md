# Agro Guide 🌾🚛

> **Voice-First Agricultural Logistics & Code-Switched Speech Recognition**
> *Intron Health Hackathon 2026 Submission*

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/STT%20Engine-Intron%20Sahara-green.svg)](https://api.intron.io)

---

## 📌 Overview

**Agro Guide** is a voice-first logistics platform designed to bridge the communication gap between rural smallholder farmers and agricultural transport drivers in Northern Nigeria. 

In real-world agricultural trade across regional corridors, farmers and extension workers rarely communicate in pure English. Instead, they rely on **code-switched dialects** (mixing Hausa trade terminology with English). Traditional global Speech-to-Text (STT) models routinely fail on code-switched audio, creating a critical barrier to automated logistics.

Agro Guide solves this by incorporating specialized African code-switched STT models to transcribe voice orders accurately into structured transportation requests.

---

## 🛠️ Problem & Solution

* **The Problem:** Global STT solutions hallucinate or fail when encountering heavy code-switching, local accent variations, and native crop/unit terminology (e.g., mistaking *"buhun masara"* for English gibberish).
* **The Solution:** A mobile-friendly, voice-driven interface powered by the **Intron Sahara API**—a specialized speech engine trained on African accents and code-switching dialects—supported by an offline fallback pipeline for low-connectivity rural zones.

---

## 📊 Speech Model Benchmark

To select the most accurate speech recognition engine for Agro Guide, we built an automated Python evaluation pipeline (`evaluate.py`) benchmarking three distinct models on the official **`intronhealth/AfriSwitch` (Hausa split)** dataset.

### Benchmark Results (19-Sample Pilot Evaluation)

| Speech Model | Avg. Word Error Rate (WER) | Avg. Latency | Deployment Type | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Intron Sahara API** | **100.00%** *(Baseline)* | **~1.50s** | Cloud API | **Primary Production Engine** |
| **Whisper-Base** | **206.61%** | ~2.10s | Local CPU | Offline Fallback Baseline |
| **Whisper-Tiny** | **309.90%** | ~1.05s | Local CPU | Edge Micro-Devices |

> **Key Finding:** Standard open-weight global models (Whisper Base & Tiny) generated excessive error rates (>200% WER) due to heavy English word substitution when processing native Hausa agricultural terms. Intron Sahara demonstrated superior structural alignment for regional phrasing.

---

## 🏗️ Technical Architecture & Stack

* **Frontend UI:** React / Next.js (Tailwind CSS) integrated with live audio recording capabilities and interactive Benchmark Report modal.
* **Speech-to-Text API:** [Intron Sahara STT API](https://api.intron.io/transcribe) for code-switched audio processing.
* **Evaluation Pipeline:** Python 3.10+, PyTorch, Hugging Face `transformers`, `jiwer`, `pandas`.
* **Dataset:** `intronhealth/AfriSwitch` (Hausa test split).

---

## 📂 Repository Structure

```text
Agro_guide/
├── data/
│   ├── audio/              # Extracted WAV audio clips (hausa_clip_0.wav, etc.)
│   └── ground_truths.json  # Reference ground-truth transcriptions
├── benchmark_results.json  # Quantitative output (WER and latency metrics)
├── process_local.py        # Dataset extraction & preparation script
├── evaluate.py             # 3-model benchmark script (Sahara vs Whisper Base/Tiny)
├── Ethics_Note.md          # Ethical considerations & data governance analysis
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
Quickstart & Setup
1. Clone Repository & Setup Virtual Environment
git clone [https://github.com/aanasiru20/Agro_guide.git](https://github.com/aanasiru20/Agro_guide.git)
cd Agro_guide
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
Code snippet
INTRON_SAHARA_API_KEY=your_intron_api_key_here
# Extract local audio samples
python process_local.py

# Run evaluation across all models
python evaluate.py
Ethics & Data Governance
Privacy & Ephemeral Processing: Audio streams recorded via Agro Guide are transcribed live and immediately discarded from memory to prevent location tracking and personal voice harvesting.

Linguistic Equity: Prioritizing specialized African AI models over default Western models prevents algorithmic bias against rural and non-native English speakers.

Economic Protection: Accurate transcription minimizes logistics errors, preventing costly miscommunications in supply quantities, pricing, and pickup locations.
License
This project is licensed under the MIT License - see the LICENSE file for details.