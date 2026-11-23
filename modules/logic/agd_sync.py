from modules.constants.agd_colors import PALETA_AGD_SLOWNIK


class AgdSynchronizer:
    @staticmethod
    def get_reversed_palette() -> dict:
        return {v: k for k, v in PALETA_AGD_SLOWNIK.items()}

    @staticmethod
    def apply_updates(agd_list: list, canvas_data: dict, updates: list[dict]) -> tuple[list, dict]:
        for item in updates:
            idx = item["idx"]
            if idx >= len(agd_list):
                continue

            obj_idx = agd_list[idx].get("object_index", 0)
            new_color = item["color"]

            agd_list[idx]["text"] = item["text"]
            agd_list[idx]["moc"] = item["moc"]
            agd_list[idx]["color"] = new_color
            if item["fuse_name"]:
                agd_list[idx]["fuse_name"] = item["fuse_name"]

            if canvas_data and "objects" in canvas_data:
                if obj_idx < len(canvas_data["objects"]):
                    canvas_data["objects"][obj_idx]["stroke"] = new_color
                    canvas_data["objects"][obj_idx]["fill"] = new_color + "66"

        return agd_list, canvas_data

    @staticmethod
    def has_unsaved_changes(agd: dict, current_name: str, current_color: str, current_moc: int, current_fuse: str | None) -> bool:
        return (
            current_name != agd.get("text")
            or current_color != agd.get("color")
            or int(current_moc) != int(agd.get("moc", 0))
            or current_fuse != agd.get("fuse_name")
        )