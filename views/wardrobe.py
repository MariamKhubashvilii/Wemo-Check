import streamlit as st
import os
import shutil
from database import add_item, get_all_items, delete_item, update_item
from ai_helper import analyze_clothing_item

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

CATEGORIES = ["Top", "Bottom", "Dress/Jumpsuit", "Outerwear", "Shoes", "Accessory", "Bag", "Other"]
ALL_SEASONS = ["Spring", "Summer", "Autumn", "Winter"]
ALL_OCCASIONS = ["Casual", "Smart Casual", "Formal", "Sport", "Party", "Beach", "Work"]


def save_uploaded_file(uploaded_file):
    dest = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest


def show():
    st.markdown("# Wardrobe")
    st.markdown("<p class='section-title'>Your collection</p>", unsafe_allow_html=True)

    tab_browse, tab_add = st.tabs(["Browse", "Add Item"])

    # ---- ADD ITEM ----
    with tab_add:
        st.markdown("### Add a new piece")
        uploaded = st.file_uploader(
            "Upload photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="Photo of the clothing item"
        )

        if uploaded:
            img_path = save_uploaded_file(uploaded)
            col_img, col_form = st.columns([1, 2], gap="large")

            with col_img:
                st.image(img_path, use_container_width=True)

                if st.button("✨ Auto-label with AI"):
                    if "api_key" not in st.session_state:
                        st.error("Add your API key in the sidebar first.")
                    else:
                        with st.spinner("Analyzing..."):
                            try:
                                result = analyze_clothing_item(img_path, st.session_state["api_key"])
                                st.session_state["ai_label"] = result
                                st.success("Done! Edit below and save.")
                            except Exception as e:
                                st.error(f"AI error: {e}")

            with col_form:
                prefill = st.session_state.get("ai_label", {})

                name = st.text_input("Name", value=prefill.get("name", ""))
                category = st.selectbox(
                    "Category",
                    CATEGORIES,
                    index=CATEGORIES.index(prefill["category"]) if prefill.get("category") in CATEGORIES else 0
                )
                colors = st.text_input("Colors", value=prefill.get("colors", ""), placeholder="e.g. navy, white")

                default_seasons = [s.strip() for s in prefill.get("seasons", "").split(",") if s.strip() in ALL_SEASONS]
                seasons = st.multiselect("Seasons", ALL_SEASONS, default=default_seasons)

                default_occasions = [o.strip() for o in prefill.get("occasions", "").split(",") if o.strip() in ALL_OCCASIONS]
                occasions = st.multiselect("Occasions", ALL_OCCASIONS, default=default_occasions)

                brand = st.text_input("Brand", value=prefill.get("brand", ""))
                notes = st.text_area("Notes", value=prefill.get("notes", ""), height=80)

                if st.button("Save to Wardrobe"):
                    if not name:
                        st.error("Give it a name.")
                    else:
                        add_item(
                            name=name,
                            category=category,
                            colors=colors,
                            seasons=", ".join(seasons),
                            occasions=", ".join(occasions),
                            brand=brand,
                            notes=notes,
                            image_path=img_path
                        )
                        st.session_state.pop("ai_label", None)
                        st.success(f"'{name}' added!")
                        st.rerun()

    # ---- BROWSE ----
    with tab_browse:
        items = get_all_items()

        if not items:
            st.markdown("""
            <div style='text-align:center; padding:4rem 2rem; color:var(--warm-gray);'>
                <p style='font-family:Playfair Display,serif; font-size:1.4rem; font-style:italic;'>
                    Your wardrobe is empty.
                </p>
                <p style='font-size:0.8rem; letter-spacing:0.1em; text-transform:uppercase;'>
                    Add your first piece →
                </p>
            </div>
            """, unsafe_allow_html=True)
            return

        # Filter bar
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_cat = st.selectbox("Category", ["All"] + CATEGORIES, key="filter_cat")
        with col_f2:
            filter_season = st.selectbox("Season", ["All"] + ALL_SEASONS, key="filter_season")
        with col_f3:
            filter_occ = st.selectbox("Occasion", ["All"] + ALL_OCCASIONS, key="filter_occ")

        filtered = items
        if filter_cat != "All":
            filtered = [i for i in filtered if i["category"] == filter_cat]
        if filter_season != "All":
            filtered = [i for i in filtered if filter_season in (i["seasons"] or "")]
        if filter_occ != "All":
            filtered = [i for i in filtered if filter_occ in (i["occasions"] or "")]

        st.markdown(f"<p style='font-size:0.75rem; color:var(--warm-gray); margin-bottom:1rem;'>{len(filtered)} items</p>", unsafe_allow_html=True)

        # Grid
        cols_per_row = 4
        for row_start in range(0, len(filtered), cols_per_row):
            row_items = filtered[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row, gap="small")
            for col, item in zip(cols, row_items):
                with col:
                    if item["image_path"] and os.path.exists(item["image_path"]):
                        st.image(item["image_path"], use_container_width=True)
                    else:
                        st.markdown("""
                        <div style='background:#F0EBE3; height:180px; display:flex;
                             align-items:center; justify-content:center;
                             font-size:2rem;'>👕</div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style='font-size:0.75rem; font-weight:500; margin-top:0.4rem;'>{item['name']}</div>
                    <div style='font-size:0.65rem; color:var(--warm-gray); letter-spacing:0.06em;
                         text-transform:uppercase;'>{item['category']}</div>
                    """, unsafe_allow_html=True)

                    with st.expander("Details / Edit"):
                        with st.form(key=f"edit_{item['id']}"):
                            e_name = st.text_input("Name", value=item["name"])
                            e_cat = st.selectbox("Category", CATEGORIES,
                                index=CATEGORIES.index(item["category"]) if item["category"] in CATEGORIES else 0)
                            e_colors = st.text_input("Colors", value=item["colors"] or "")
                            e_seasons_default = [s.strip() for s in (item["seasons"] or "").split(",") if s.strip() in ALL_SEASONS]
                            e_seasons = st.multiselect("Seasons", ALL_SEASONS, default=e_seasons_default)
                            e_occ_default = [o.strip() for o in (item["occasions"] or "").split(",") if o.strip() in ALL_OCCASIONS]
                            e_occasions = st.multiselect("Occasions", ALL_OCCASIONS, default=e_occ_default)
                            e_brand = st.text_input("Brand", value=item["brand"] or "")
                            e_notes = st.text_area("Notes", value=item["notes"] or "", height=60)

                            col_save, col_del = st.columns(2)
                            with col_save:
                                if st.form_submit_button("Save"):
                                    update_item(item["id"], e_name, e_cat, e_colors,
                                                ", ".join(e_seasons), ", ".join(e_occasions),
                                                e_brand, e_notes)
                                    st.rerun()
                            with col_del:
                                if st.form_submit_button("Delete", type="secondary"):
                                    delete_item(item["id"])
                                    st.rerun()
