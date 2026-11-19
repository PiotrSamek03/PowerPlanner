class CircuitCalculator:
    @staticmethod
    def calculate_load(fuses_list: list, agd_list: list) -> dict:
        obciazenie_bezpiecznikow = {}
        for f in fuses_list:
            f_name = f.name if hasattr(f, "name") else f.get("name", "Bezpiecznik")
            amps = getattr(f, "amps", f.get("amps", 16) if isinstance(f, dict) else 16)
            limit_watow = getattr(f, "max_power", amps * 230)
            obciazenie_bezpiecznikow[f_name] = {
                "aktualna_moc": 0,
                "limit": limit_watow,
                "urzadzenia": []
            }

        bledy = []
        nieprzypisane = 0
        calkowita_moc_urzadzen = 0
        calkowity_limit_bezpiecznikow = sum(d["limit"] for d in obciazenie_bezpiecznikow.values())

        for agd in agd_list:
            nazwa = agd.get("text", "Urządzenie")
            moc = int(agd.get("moc", 0))
            bezpiecznik = agd.get("fuse_name")

            calkowita_moc_urzadzen += moc

            if moc <= 0:
                bledy.append(f"⚠️ Urządzenie **'{nazwa}'** ma ustawioną moc 0 W.")

            if not bezpiecznik:
                nieprzypisane += 1
                bledy.append(f"❌ Urządzenie **'{nazwa}'** nie jest przypisane do żadnego bezpiecznika!")
            elif bezpiecznik in obciazenie_bezpiecznikow:
                obciazenie_bezpiecznikow[bezpiecznik]["aktualna_moc"] += moc
                obciazenie_bezpiecznikow[bezpiecznik]["urzadzenia"].append({"nazwa": nazwa, "moc": moc})
            else:
                bledy.append(f"❌ Urządzenie **'{nazwa}'** wskazuje na nieistniejący bezpiecznik: {bezpiecznik}")

        przeciazony_jakikolwiek = any(d["aktualna_moc"] > d["limit"] for d in obciazenie_bezpiecznikow.values())

        konflikty = []
        for f_name, dane in obciazenie_bezpiecznikow.items():
            if dane["aktualna_moc"] > dane["limit"]:
                posortowane = sorted(dane["urzadzenia"], key=lambda x: x["moc"], reverse=True)
                if len(posortowane) >= 2:
                    konflikty.append({
                        "fuse_name": f_name,
                        "u1": posortowane[0],
                        "u2": posortowane[1],
                        "limit": dane["limit"]
                    })

        return {
            "obciazenie_bezpiecznikow": obciazenie_bezpiecznikow,
            "bledy": bledy,
            "nieprzypisane": nieprzypisane,
            "calkowita_moc": calkowita_moc_urzadzen,
            "calkowity_limit": calkowity_limit_bezpiecznikow,
            "przeciazony": przeciazony_jakikolwiek,
            "konflikty": konflikty
        }