from modules.constants.agd_colors import PALETA_AGD_SLOWNIK


class CanvasParser:
    @staticmethod
    def _get_fabric_center(obj: dict) -> tuple[float, float] | None:
        if {"left", "top", "width", "height"}.issubset(obj.keys()):
            left = float(obj.get("left", 0.0))
            top = float(obj.get("top", 0.0))
            width = float(obj.get("width", 0.0)) * float(obj.get("scaleX", 1.0))
            height = float(obj.get("height", 0.0)) * float(obj.get("scaleY", 1.0))
            return left + width / 2.0, top + height / 2.0
        return None

    @staticmethod
    def parse_canvas_data(canvas_data: dict) -> list:
        objects = canvas_data.get("objects", []) if canvas_data else []
        agd_objects = []
        for i, obj in enumerate(objects):
            if obj.get("type") in ("i-text", "text", "textbox") and obj.get("is_agd_label"):
                continue
            kolor_obiektu = obj.get("stroke", "")
            if kolor_obiektu in PALETA_AGD_SLOWNIK.values():
                agd_objects.append((i, obj))

        new_agd_list = []
        for idx, (obj_idx, obj) in enumerate(agd_objects):
            agd_number = idx + 1
            kolor = obj.get("stroke", "#0077b6")
            center = CanvasParser._get_fabric_center(obj)
            new_agd_list.append({
                "object_index": obj_idx,
                "agd_number": agd_number,
                "center": center,
                "text": f"Urządzenie AGD #{agd_number}",
                "moc": 0,
                "fuse_id": None,
                "color": kolor,
            })
        return new_agd_list