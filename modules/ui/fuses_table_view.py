import streamlit as st
from modules.services.fuse_service import delete_fuse_from_db
from modules.state.user_data_state import remove_fuse_at_index


def _row_divider():
    st.markdown(
        "<hr style='margin: 3px 0; border: none; border-top: 1px solid rgba(150, 150, 150, 0.25);'>",
        unsafe_allow_html=True,
    )


def render_fuses_table(fuses_list):
    if not fuses_list:
        st.info("Brak zdefiniowanych bezpieczników.")
        return

    table_container, _ = st.columns([5.5, 4.5])

    with table_container:
        st.subheader("Lista bezpieczników")

        st.markdown(
            """
            <style>
            .fuse-row-scope div[data-testid="stButton"] > button {
                margin: 0 auto !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding-top: 2px !important;
                padding-bottom: 2px !important;
                min-height: 30px !important;
            }
            .fuse-row-scope div[data-testid="stVerticalBlock"],
            .fuse-row-scope div[data-testid="stMarkdownContainer"] {
                margin-bottom: 0px !important;
                padding-bottom: 0px !important;
            }
            .fuse-cell-center {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 30px;
                line-height: 1.2;
            }
            .fuse-header-center {
                text-align: center;
                font-weight: 700;
                margin-bottom: 2px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        header_cols = st.columns([1.0, 2.5, 1.8], vertical_alignment="center")
        header_cols[0].markdown("<div class='fuse-header-center'>Usuń</div>", unsafe_allow_html=True)
        header_cols[1].markdown("<div class='fuse-header-center'>Nazwa</div>", unsafe_allow_html=True)
        header_cols[2].markdown("<div class='fuse-header-center'>Prąd (A)</div>", unsafe_allow_html=True)
        _row_divider()

        for idx, f in enumerate(fuses_list):
            if isinstance(f, dict):
                name = f.get("name", "Brak nazwy")
                current_amp = f.get("current_amp", f.get("prad", 16))
            else:
                name = getattr(f, "name", getattr(f, "nazwa", "Brak nazwy"))
                current_amp = getattr(f, "amps", getattr(f, "current_amp", getattr(f, "prad", 16)))

            with st.container():
                st.markdown("<div class='fuse-row-scope'>", unsafe_allow_html=True)
                row_cols = st.columns([1.0, 2.5, 1.8], vertical_alignment="center")

                with row_cols[0]:
                    if st.button("Usuń", key=f"delete_fuse_{idx}", help=f"Usuń bezpiecznik {name}"):
                        updated_fuses, fuse_id = remove_fuse_at_index(
                            st.session_state.get("fuses_list", []), idx
                        )
                        if fuse_id:
                            delete_fuse_from_db(fuse_id)
                        st.session_state["fuses_list"] = updated_fuses
                        st.session_state["fuses"] = updated_fuses
                        st.rerun()

                with row_cols[1]:
                    st.markdown(f"<div class='fuse-cell-center'>{name}</div>", unsafe_allow_html=True)

                with row_cols[2]:
                    st.markdown(f"<div class='fuse-cell-center'>{current_amp} A</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            _row_divider()