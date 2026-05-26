import anthropic
import base64
import json
import re


def encode_image(image_path: str) -> tuple[str, str]:
    ext = image_path.lower().split(".")[-1]
    media_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    media_type = media_map.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def analyze_clothing_item(image_path: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    img_data, media_type = encode_image(image_path)

    prompt = """Analyze this clothing item and return ONLY a JSON object with these exact keys:
{
  "name": "short descriptive name (e.g. 'White Linen Shirt')",
  "category": one of ["Top", "Bottom", "Dress/Jumpsuit", "Outerwear", "Shoes", "Accessory", "Bag", "Other"],
  "colors": "comma-separated main colors (e.g. 'navy, white')",
  "seasons": "comma-separated seasons it suits (Spring, Summer, Autumn, Winter)",
  "occasions": "comma-separated occasions (Casual, Smart Casual, Formal, Sport, Party, Beach, Work)",
  "brand": "brand name if visible, else empty string",
  "notes": "one brief style note"
}

Return ONLY the JSON, no markdown, no explanation."""

    response = client.messages.create(
     model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_data,
                        },
                    },
                    {"type": "text", "text": prompt}
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def suggest_outfits(wardrobe: list[dict], vibe: str, api_key: str) -> list[dict]:
    client = anthropic.Anthropic(api_key=api_key)

    wardrobe_summary = []
    for item in wardrobe:
        wardrobe_summary.append({
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "colors": item["colors"],
            "seasons": item["seasons"],
            "occasions": item["occasions"],
            "notes": item.get("notes", ""),
        })

    prompt = f"""You are a personal stylist. The user wants to dress for: "{vibe}"

Here is their wardrobe:
{json.dumps(wardrobe_summary, indent=2)}

Create exactly 3 distinct outfit suggestions. Each outfit should be coherent, weather/vibe appropriate, and stylish.

Return ONLY a JSON array with exactly 3 objects, each with these keys:
{{
  "outfit_name": "short creative name for the outfit",
  "item_ids": [list of item ids from the wardrobe],
  "reasoning": "1-2 sentences explaining why this works for the vibe"
}}

Rules:
- Use only items from the wardrobe (by their id)
- Each outfit needs at minimum: a top or dress, and shoes if available
- Make the 3 outfits meaningfully different from each other
- Return ONLY the JSON array, no markdown, no explanation."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)
