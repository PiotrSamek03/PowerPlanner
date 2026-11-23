from modules.constants.agd_colors import PALETA_AGD_SLOWNIK


class DrawingStyleResolver:
    @staticmethod
    def resolve_colors(element_type: str, selected_agd_color_name: str | None = None) -> tuple[str, str]:
        if element_type == "Sprzęt AGD / Światło (Własny kolor z palety)":
            stroke_color = PALETA_AGD_SLOWNIK.get(selected_agd_color_name, "#0077b6")
            fill_color = stroke_color + "66"
            return stroke_color, fill_color

        if element_type.startswith("Ściana"):
            return "#000000", "rgba(0, 0, 0, 0.1)"

        return "#FFD700", "rgba(255, 215, 0, 0.5)"

    @staticmethod
    def create_agd_index_object(number: int, cx: float, cy: float) -> dict:
        return {
            "type": "i-text",
            "text": str(number),
            "left": cx,
            "top": cy,
            "fill": "#000000",
            "fontSize": 16,
            "fontWeight": "bold",
            "originX": "center",
            "originY": "center",
            "textAlign": "center",
            "selectable": False,
            "evented": False,
            "is_agd_label": True,
        }