<p align="center">
  <img alt="NoFakingWay" src="https://i.imgur.com/1kjTGOX.jpeg" width="120" style="border-radius: 16px;">
  <h1 align="center">NoFakingWay</h1>
  <p align="center"><b>Fake review & spam detection pipeline for e-commerce.</b></p>
  <p align="center">Multi-filter NLP system that validates reviews across language, PII, and URL checks.</p>
</p>

<p align="center">
  <a href="https://github.com/Amloii/NoFakingWay"><img alt="Stack" src="https://img.shields.io/badge/stack-Python%20%7C%20spaCy%20%7C%20Streamlit-25601B?style=flat-square&labelColor=ffffff&color=25601B"></a>
  <a href="https://github.com/Amloii/NoFakingWay"><img alt="Created" src="https://img.shields.io/badge/created-April%202022-000000?style=flat-square&labelColor=ffffff&color=000000"></a>
  <a href="https://github.com/Amloii/NoFakingWay"><img alt="Status" src="https://img.shields.io/badge/status-discontinued-ef4444?style=flat-square&labelColor=ffffff&color=ef4444"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square&labelColor=ffffff&color=blue"></a>
</p>

<p align="center">
  <a href="#-about">About</a> •
  <a href="#-filters">Filters</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-project-structure">Structure</a>
</p>

<br>

> **Created April 2022 as part of the NoFakes initiative within Grupo NextChance.**  
> This project has been **discontinued**. Since its creation, LLM-based classification (GPT, Gemini, etc.) has proven significantly more effective for fake review detection. The code remains available as a reference and learning resource.

---

## 🧐 About

Fake reviews and spam are persistent problems on e-commerce platforms like Amazon, Yelp, and Google Maps. At the time of development (2022), most detection relied on handcrafted rules and classical NLP pipelines.

NoFakingWay validates product reviews through a series of filters, flagging suspicious content before it reaches the platform. It was designed for the [NoFakes](https://github.com/Amloii/NoFakingWay) project, focused on digital fraud detection and content authenticity.

---

## 🔍 Filters

| Filter | Method | Flags |
|---|---|---|
| **Language** | `spaCy` + `langdetect` | Reviews not in allowed languages (ES, EN, FR) or gibberish text (e.g. `jsdfisefbijfd adifaio`) |
| **PII** | Regex patterns (phone, ID, email) | Reviews containing personal identifiable information |
| **URL** | `urlextract` | Any review containing a URL (common spam signal) |

Each filter operates independently and writes its verdict to a shared pipeline output. Filters can be extended or modified individually.

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Amloii/NoFakingWay.git
cd NoFakingWay

# Install dependencies
pip install -r requirements.txt
```

All filters require a local spaCy model. The `requirements.txt` includes `en_core_web_sm`.

---

## 🎈 Usage

### Streamlit demo

```bash
streamlit run streamlit/demo_streamlit.py
```

Or try the cloud version on [Streamlit Community Cloud](https://share.streamlit.io/amloii/nofakingway/main/streamlit/demo_streamlit.py).

### Programmatic

```python
from filters.Lang.Lang_filter import check_language
from filters.PII.pii_filter import check_pii
from filters.URL.url_filter import check_url

review = "Great product! Call me at +34 612 345 678"
print(check_url(review))   # Suspicious
print(check_pii(review))   # Suspicious
```

---

## 📁 Project Structure

```
├── filters/
│   ├── Lang/          # Language detection filter (spaCy + langdetect)
│   ├── PII/           # Personal Information filter (regex)
│   └── URL/           # URL detection filter (urlextract)
├── streamlit/
│   └── demo_streamlit.py  # Interactive Streamlit demo
└── requirements.txt
```

---

## 📝 License

MIT — see [LICENSE](LICENSE).

---

## 👤 Author

**Daniel Gómez Domínguez** — AI Systems Architect & Director of AI.

Built during his tenure as Lead Data Scientist at NoFakes (Grupo NextChance), focusing on NLP-based fraud detection.

[GitHub](https://github.com/Amloii) · [LinkedIn](https://linkedin.com/in/danigdominguez) · [Portfolio](https://amloii-page.pages.dev)

<br>

---

<p align="center">
  <sub>NoFakingWay · 2022 — Discontinued, but not forgotten.</sub>
</p>
