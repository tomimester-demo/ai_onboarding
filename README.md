# AI-Powered Personalized Onboarding Emails

Automates **personalized onboarding emails** for new members of *Data Science Klub* using Python + LLMs. Reads a Typeform onboarding survey, builds a structured prompt, generates a tailored HTML email via OpenAI, and sends it through the Brevo API.

---

## 📈 Why

- **Goal:** Improve early retention by guiding members to the right starting materials.
- **Impact:** Retention rose from ~25% → **40–50%** by month 3.
- **Cost:** Only cents/month for LLM usage.
- **Speed:** End-to-end in ~4–5 minutes.
- **UX:** Positive member feedback — emails feel personal and helpful.

---

## ⚙ How it Works

1. **Typeform webhook** posts the onboarding form JSON.
2. **Parser** cleans and normalizes answers into a `qa_dict`.
3. **Prompt builder** merges:
   - Context & style rules
   - Member answers
   - Content catalogue (talks/courses with audience tags)
4. **Business rules** classify member (*beginner* vs *not beginner*), select content.
5. **OpenAI API** generates HTML email body.
6. **Brevo API** sends the email.

---

## 📂 Files

- `AI_onboarding_dataklub.py` – full workflow script
- `ai onboarding github prezi.pdf` – slides with background, pipeline, metrics, examples

---

## 🚀 Quick Start

**Requirements**
```bash
pip install openai requests pyyaml
```

### Auth (YAML)  
openai_api_key: "sk-..."  
brevo_api: "xkeysib-..."  

> Keep secrets out of version control.  

### Run  
python AI_onboarding_dataklub.py  

---

## Deployment notes  

- Replace file-based JSON with a live webhook handler.  
- Store secrets in env vars or a secret manager.  
- Add logging + spot checks for quality; track clicks to improve recommendations.  

---

## License  

Educational/demo code originally built for **Data Science Klub** (Data36). Adapt paths, keys, and services for your environment.  

