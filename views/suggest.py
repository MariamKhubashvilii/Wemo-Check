import streamlit as st
import os
from database import get_all_items, save_outfit, get_folders
from ai_helper import suggest_outfits


def show():
    st.markdown("# Get Dressed")
    st.markdown("<p class='section-title'>Tell me the vibe</p>", unsafe_allow_html=True)

    items = get_all_items()
    if not items:
        st.info("Your wardrobe is empty. Add some clothes first.")
        return

    if "api_key" not in st.session_state:
        st.warning("Add your Anthropic API key in the sidebar to use this feature.")
        return

    # Vibe input
    col_input, col_btn = st.columns([3, 1], gap="medium")
    with col_input:
        vibe = st.text_input(
            "What's the occasion?",
            placeholder='e.g. "dinner in the rain", "beach day", "job interview", "lazy sunday"',
            label_visibility="collapsed"
        )
    with col_btn:
        go = st.button("Suggest Outfits", use_container_width=True)

    st.markdown("---")

    # Suggestion results
    if go and vibe.strip():
        with st.spinner("Styling you..."):
            try:
                suggestions = suggest_outfits(items, vibe.strip(), st.session_state["api_key"])
                st.session_state["suggestions"] = suggestions
                st.session_state["vibe"] = vibe.strip()
            except Exception as e:
                st.error(f"Error: {e}")
                return

    suggestions = st.session_state.get("suggestions", [])
    current_vibe = st.session_state.get("vibe", "")

    if suggestions:
        st.markdown(f"### Outfits for *\"{current_vibe}\"*")
        st.markdown(f"<p style='font-size:0.75rem; color:var(--warm-gray); margin-bottom:2rem;'>{len(items)} items in wardrobe — pick a look:</p>", unsafe_allow_html=True)

        item_map = {i["id"]: i for i in items}

        for idx, outfit in enumerate(suggestions):
            outfit_items = [item_map[i] for i in outfit["item_ids"] if i in item_map]

            with st.container():
                st.markdown(f"""
                <div style='border-top: 2px solid var(--charcoal); padding-top:1rem; margin-bottom:0.5rem;'>
                    <span style='font-family:Playfair Display,serif; font-size:1.1rem;'>
                        {idx+1}. {outfit['outfit_name']}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<p style='font-size:0.82rem; color:var(--warm-gray); margin-bottom:1rem;'>💬 {outfit['reasoning']}</p>", unsafe_allow_html=True)

                # Photo grid of outfit items
                if outfit_items:
                    n = len(outfit_items)
                    grid_cols = st.columns(min(n, 5), gap="small")
                    for gcol, it in zip(grid_cols, outfit_items):
                        with gcol:
                            if it["image_path"] and os.path.exists(it["image_path"]):
                                st.image(it["image_path"], use_container_width=True)
                            else:
                                st.markdown("""
                                <div style='background:#F0EBE3; height:140px; display:flex;
                                     align-items:center; justify-content:center; font-size:1.5rem;'>
                                     👕</div>
                                """, unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size:0.65rem; color:var(--warm-gray); text-align:center; margin-top:0.2rem;'>{it['name']}</div>", unsafe_allow_html=True)

                # Save section
                save_key = f"save_open_{idx}"
                if st.button(f"Save this outfit", key=f"save_btn_{idx}"):
                    st.session_state[save_key] = True

                if st.session_state.get(save_key):
                    with st.container():
                        sc1, sc2, sc3 = st.columns([2, 1, 1], gap="small")
                        with sc1:
                            outfit_name_input = st.text_input(
                                "Outfit name",
                                value=outfit["outfit_name"],
                                key=f"oname_{idx}",
                                label_visibility="collapsed",
                                placeholder="Name this outfit"
                            )
                        with sc2:
                            folders = get_folders() or ["General"]
                            if "General" not in folders:
                                folders = ["General"] + folders
                            new_folder = st.text_input("Folder (new or existing)", key=f"folder_{idx}", placeholder="e.g. Work", label_visibility="collapsed")
                            folder_choice = new_folder if new_folder.strip() else st.selectbox(
                                "Folder", folders, key=f"fsel_{idx}", label_visibility="collapsed"
                            )
                        with sc3:
                            rating = st.slider("Rate it", 0.0, 5.0, 3.0, 0.5, key=f"rating_{idx}", label_visibility="collapsed")

                        notes_input = st.text_input("Notes (optional)", key=f"notes_{idx}", label_visibility="collapsed", placeholder="Any notes...")

                        if st.button("Confirm Save", key=f"confirm_{idx}"):
                            save_outfit(
                                name=outfit_name_input,
                                item_ids=outfit["item_ids"],
                                vibe=current_vibe,
                                rating=rating,
                                folder=folder_choice if not new_folder.strip() else new_folder.strip(),
                                notes=notes_input
                            )
                            st.session_state[save_key] = False
                            st.success(f"Saved to '{folder_choice}'!")

                st.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)
