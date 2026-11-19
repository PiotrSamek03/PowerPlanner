from modules.constants.agd_colors import PALETA_AGD_SLOWNIK

class CanvasParser:
    @staticmethod
    def parse_canvas_data(canvas_data: dict) -> list:

        objects = canvas_data.get("objects", []) if canvas_data else []
        agd_objects = []
        for i, obj in enumerate(objects):
            kolor_obiektu = obj.get("stroke", "")
            if kolor_obiektu in PALETA_AGD_SLOWNIK.values():
                agd_objects.append((i, obj))
            
        new_agd_list = []
        for idx, (obj_idx, obj) in enumerate(agd_objects):
            kolor = obj.get("stroke", "#0077b6")
            new_agd_list.append({
                "object_index": obj_idx,
                "text": f"Urządzenie AGD #{idx + 1}",
                "moc": 0,
                "fuse_id": None,
                "color": kolor
            })
        return new_agd_list