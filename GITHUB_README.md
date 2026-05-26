# DRIP 🧥

> **Initial release — v0.1**
> A local-first AI wardrobe stylist built with Streamlit and Claude.

DRIP lets you catalog your clothing, then tells you what to wear. Type a vibe — "dinner in the rain", "beach day", "job interview" — and it pulls outfits from your actual wardrobe. No subscriptions, no cloud, no data leaving your machine except the API calls.

---

## Features

- **AI labeling** — upload a photo, Claude auto-fills category, colors, seasons, and occasions. Edit freely before saving.
- **Wardrobe browser** — filterable grid by category, season, and occasion.
- **Vibe-based outfit suggestions** — describe where you're going, get 3 styled outfits shown as photo grids with reasoning.
- **Save and rate** — rate outfits 0–5 stars, organize into folders, keep your favorites.
- **Fully local** — SQLite database + local file storage. Your wardrobe lives on your machine.

---

## Stack

- [Streamlit](https://streamlit.io/) — UI
- [Anthropic Claude](https://www.anthropic.com/) — vision labeling + outfit generation
- SQLite — local database
- Python 3.10+

---

## Setup

```bash
git clone https://github.com/your-username/drip
cd drip
pip install -r requirements.txt
streamlit run app.py
```

Add your [Anthropic API key](https://console.anthropic.com/) in the sidebar when the app opens. It is never written to disk.

---

## Project structure

```
drip/
├── app.py              # Entry point, layout, global CSS
├── database.py         # SQLite schema and queries
├── ai_helper.py        # Claude vision + outfit suggestion logic
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

This is an early proof of concept. Planned features roughly in order:

**Near term**
- [ ] Live weather integration — pull real conditions by location instead of typing the vibe manually
- [ ] Vacation / packing mode — build the most outfits from the fewest items
- [ ] Bulk import — add multiple items at once from a folder

**Style intelligence**
- [ ] Style profile — learn your taste from outfit ratings over time
- [ ] Wardrobe gap analysis — "based on what you wear, here's what's missing"
- [ ] Outfit history — track what you wore and when

**External integrations**
- [ ] Pinterest — rate outfits from Pinterest to train your style profile
- [ ] Shopping — surface items that fill your wardrobe gaps from external stores

**Quality of life**
- [ ] Outfit sharing — export a look as an image
- [ ] Multiple users / profiles
- [ ] Mobile-friendly layout

---

## Notes

Photos and database are gitignored by default. Add a `.gitignore` if you're pushing a fork:

```
uploads/
data/
__pycache__/
.env
```

---

*Built as a personal project. Contributions and ideas welcome.*
