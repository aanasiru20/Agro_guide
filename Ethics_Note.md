# Ethics, Safety & Inclusion Note
**Project:** Code-Switched Speech Recognition for Agricultural Coordination  
**Track:** Intron Health Hackathon Submission  

---

### 1. Consent & Data Privacy
* **Anonymization:** All farmer and driver voice recordings are stripped of Personally Identifiable Information (PII)—including personal names, phone numbers, and precise home locations—before audio processing.
* **Consent Mechanisms:** Audio data collection strictly follows informed opt-in consent protocols tailored for rural, multilingual communities, ensuring participants understand how their voice data is used.
* **Data Lifecycles & Encryption:** Audio streams and transcriptions are encrypted in transit (TLS 1.3) and at rest (AES-256). Audio logs used during benchmarking are temporary and securely deleted post-evaluation.

---

### 2. Bias Awareness & Inclusivity
* **Dialectal Diversity:** Traditional global Speech-to-Text (STT) models penalize non-standard English accents and code-switching (e.g., Hausa-English, Yoruba-English, Pidgin). Benchmarking explicitly against localized models ensures equitable utility for rural farmers.
* **Low-Literacy & Accessibility:** By prioritizing voice interfaces over text inputs, the application accommodates low-literacy users, allowing them to communicate naturally in their native language and dialect.
* **Linguistic Fairness:** Evaluation spans diverse code-switched syntactic patterns to prevent model bias toward single-language dominant speakers.

---

### 3. Safety & Dignity
* **Scope Limitation:** Audio data is processed strictly for agricultural route planning, transport coordination, and supply chain logistics.
* **Prohibition of Misuse:** Voice logs will never be sold, monetized, or shared with third-party advertisers, credit scoring platforms, or surveillance entities.
* **Dignified AI Design:** Models are optimized to accurately capture local crop names, traditional measurements (e.g., "buhun masara"), and regional phrasing without falsely categorizing local vocabulary as noise or error.