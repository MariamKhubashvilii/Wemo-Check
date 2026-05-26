import streamlit as st
import os
from database import get_all_outfits, get_all_items, update_outfit_rating, delete_outfit


def show():
    st.markdown("# Saved Outfits")
    st.markdown("<p class='section-title'>Your curated looks</p>", unsafe_allow_html=True)

    outfits = get_all_outfits()
    items = get_all_items()
    item_map = {i["id"]: i for i in items}

    if not outfits:
        st.markdown("""
        <div style='text-align:center; padding:4rem 2rem; color:var(--warm-gray);'>
            <p style='font-family:Playfair Display,serif; font-size:1.4rem; font-style:italic;'>
                No saved outfits yet.
            </p>
            <p style='font-size:0.8rem; letter-spacing:0.1em; text-transform:uppercase;'>
                Get dressed and save a look →
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Group by folder
    folders = {}
    for o in outfits:
        folder = o["folder"] or "General"
        folders.setdefault(folder, []).append(o)

    # Folder filter
    all_folders = list(folders.keys())
    selected_folder = st.selectbox("Folder", ["All"] + all_folders, label_visibility="collapsed")

    st.markdown("---")

    display_outfits = outfits if selected_folder == "All" else folders.get(selected_folder, [])

    for outfit in display_outfits:
        outfit_item_ids = [int(x) for x in outfit["item_ids"].split(",") if x.strip().isdigit()]
        outfit_items = [item_map[i] for i in outfit_item_ids if i in item_map]

        col_meta, col_grid = st.columns([1, 3], gap="large")

        with col_meta:
            st.markdown(f"""
            <div style='font-family:Playfair Display,serif; font-size:1.05rem; margin-bottom:0.3rem;'>
                {outfit['name']}
            </div>
            <div style='font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase;
                 color:var(--warm-gray); margin-bottom:0.6rem;'>
                {outfit['folder']}
            </div>
            """, unsafe_allow_html=True)

            if outfit["vibe"]:
                st.markdown(f"<div style='font-size:0.75rem; color:var(--warm-gray); margin-bottom:0.5rem;'>✦ {outfit['vibe']}</div>", unsafe_allow_html=True)

            # Star rating display
            stars = int(round(outfit["rating"] or 0))
            star_str = "★" * stars + "☆" * (5 - stars)
            st.markdown(f"<div style='font-size:1rem; color:var(--accent); letter-spacing:0.1em;'>{star_str}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.7rem; color:var(--warm-gray);'>{outfit['rating']}/5</div>", unsafe_allow_html=True)

            if outfit["notes"]:
                st.markdown(f"<div style='font-size:0.75rem; color:var(--warm-gray); margin-top:0.5rem; font-style:italic;'>{outfit['notes']}</div>", unsafe_allow_html=True)

            # Update rating
            new_rating = st.slider(
                "Update rating",
                0.0, 5.0,
                float(outfit["rating"] or 0),
                0.5,
                key=f"r_{outfit['id']}",
                label_visibility="collapsed"
            )
            if new_rating != outfit["rating"]:
                update_outfit_rating(outfit["id"], new_rating)
                st.rerun()

            if st.button("Delete", key=f"del_{outfit['id']}", type="secondary"):
                delete_outfit(outfit["id"])
                st.rerun()

        with col_grid:
            if outfit_items:
                n = len(outfit_items)
                gcols = st.columns(min(n, 5), gap="small")
                for gcol, it in zip(gcols, outfit_items):
                    with gcol:
                        if it["image_path"] and os.path.exists(it["image_path"]):
                            st.image(it["image_path"], use_container_width=True)
                        else:
                            st.markdown("""
                            <div style='background:#F0EBE3; height:160px; display:flex;
                                 align-items:center; justify-content:center; font-size:1.5rem;'>
                                 👕</div>
                            """, unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:0.65rem; color:var(--warm-gray); text-align:center;'>{it['name']}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:var(--warm-gray); font-size:0.8rem;'>Items no longer in wardrobe.</p>", unsafe_allow_html=True)

        st.markdown("---")
