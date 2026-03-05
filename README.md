# 💍 Wedded Wonderland AI Content Engine

Built by **Drishya Lal Chuke** as part of the Gen AI Intern application for Wonder Group / Wedded Wonderland.

---

## What This App Does

A branded AI-powered content tool with 3 modules:

| Tab | What It Does |
|-----|-------------|
| 💍 Vendor Profile Generator | Turns basic vendor info into full directory listings, Instagram bios, social captions & SEO descriptions |
| ✍️ Blog Article Generator | Generates full SEO-optimised articles for Wedded Wonderland's global content calendar |
| 📊 ROI Calculator | Quantifies the business value of AI adoption across content operations |

---

## Setup (5 minutes)

### Step 1 — Get your OpenAI API Key
1. Go to https://platform.openai.com
2. Sign up / log in
3. Go to API Keys → Create new secret key
4. Add $5 credit (this app costs cents per run)

### Step 2 — Install and Run Locally

```bash
# Make sure Python is installed, then:
pip install streamlit openai

# Run the app
streamlit run app.py
```

The app opens at http://localhost:8501 in your browser.

---

## Deploy Publicly (Free) — Streamlit Cloud

1. Push this folder to a **GitHub repo** (public)
2. Go to https://share.streamlit.io
3. Click **New App** → select your repo → select `app.py`
4. Click **Deploy**

You'll get a public URL like:
`https://your-name-ww-ai-engine.streamlit.app`

Share this link in your video interview.

---

## How to Demo in Your Interview

1. Open the deployed app
2. Enter your API key in the ⚙️ box at the top
3. Tab 1: Enter a real Wedded Wonderland vendor (e.g. "Bloom & Gather, Sydney, floral design")
4. Tab 2: Generate an article on "Bali destination weddings 2025"
5. Tab 3: Show the ROI — drag the sliders to match their actual scale

**Key line to say:**
> *"I built this specifically for Wedded Wonderland's workflow. Based on your 50,000 vendor directory and weekly content output, this tool can save your team over X hours and $Y per month."*

---

## Tech Stack

- Python 3.10+
- Streamlit (frontend + deployment)
- OpenAI GPT-4o API (content generation)
- Custom CSS (Wedded Wonderland brand: gold, cream, Cormorant Garamond serif)

---

*Built in under 24 hours as a practical demonstration of Gen AI deployment skills.*
