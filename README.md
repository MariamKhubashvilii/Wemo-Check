# Wemo Check 🧥

**Initial release — v0.1**
A local-first AI wardrobe stylist built with Streamlit and Claude. Inspired by Haewon from NMIXX.

Wemo Check lets you catalog your clothing and tells you what to wear. Type a vibe like "dinner in the rain", "beach day", or "job interview" and it pulls together outfits from your actual wardrobe. No subscriptions, no cloud, no data leaving your machine except the API calls.

---

## Features

- **AI labeling** — upload a photo, Claude auto-fills category, colors, seasons, and occasions. Edit freely before saving.
- **Wardrobe browser** — filterable grid by category, season, and occasion.
- **Vibe-based outfit suggestions** — describe where you're going, get 3 styled outfits shown as photo grids with reasoning.
- **Save and rate** — rate outfits 0 to 5 stars, organize into folders, keep your favorites.
- **Fully local** — SQLite database and local file storage. Your wardrobe lives on your machine.

---

## Stack

- [Streamlit](https://streamlit.io/) for the UI
- [Anthropic Claude](https://www.anthropic.com/) for vision labeling and outfit generation
- SQLite for local storage
- Python 3.10+

---

## Setup

```bash
git clone https://github.com/your-username/wemo-check
cd wemo-check
pip install -r requirements.txt
streamlit run app.py
```

Add your [Anthropic API key](https://console.anthropic.com/) in the sidebar when the app opens. It is never written to disk.

---

## Project Structure

```
wemo-check/
├── app.py              # Entry point, layout, global CSS
├── database.py         # SQLite schema and queries
├── ai_helper.py        # Claude vision and outfit suggestion logic
├── pages/
│   ├── wardrobe.py     # Browse and add clothing items
│   ├── suggest.py      # Outfit suggestion flow
│   └── saved.py        # Saved outfits and folders
├── uploads/            # Local clothing photos (gitignored)
├── data/               # SQLite database (gitignored)
└── requirements.txt
```

---

## Roadmap

This is an early proof of concept. Here is what is planned next, roughly in order.

**Coming soon**
- Live weather integration — pull real conditions by location instead of typing the vibe manually
- Vacation / packing mode — build the most outfits from the fewest items
- Bulk import — add multiple items at once from a folder

**Style intelligence**
- Style profile — learn your taste from outfit ratings over time
- Wardrobe gap analysis — "based on what you wear, here is what is missing"
- Outfit history — track what you wore and when

**External integrations**
- Pinterest — rate outfits from Pinterest to train your style profile
- Shopping — surface items that fill your wardrobe gaps from external stores

**Quality of life**
- Outfit sharing — export a look as an image
- Multiple users and profiles
- Mobile-friendly layout

---

## Notes

Photos and the database are gitignored by default. Add a `.gitignore` with the following before pushing:

```
uploads/
data/
__pycache__/
.env
```

---

*Built as a personal project. Contributions and ideas welcome.*
