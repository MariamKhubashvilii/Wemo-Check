# DRIP — Your AI Wardrobe Stylist

A local Streamlit app that manages your wardrobe and suggests outfits based on vibes and weather.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## First use

1. Paste your Anthropic API key in the sidebar (never stored to disk)
2. Go to **Wardrobe → Add Item**, upload a photo, hit **Auto-label with AI**, edit if needed, save
3. Go to **Get Dressed**, type a vibe like `"dinner in rain"` or `"beach day"`, get 3 outfit suggestions
4. Rate and save outfits to folders in **Saved Outfits**

## Data storage

Everything is stored locally:
- `data/wardrobe.db` — SQLite database with items and outfits
- `uploads/` — your clothing photos

Nothing is sent to any cloud except the Anthropic API calls (photos for labeling, wardrobe metadata for suggestions).

## What's next (v2 ideas)

- Vacation packing mode (minimise items)
- Style profile ML from your ratings
- Pinterest outfit rating to train your taste profile
- "What am I missing?" style gap analysis
