def detect_hidden_content(file_path):
    signatures = {
        "PDF": b"%PDF",
        "PNG": b"\x89PNG",
        "JPG": b"\xFF\xD8\xFF",
        "ZIP": b"PK\x03\x04",
        "EXE": b"MZ"
    }

    found_types = []

    try:
        with open(file_path, "rb") as f:
            data = f.read()

            for file_type, sig in signatures.items():
                if sig in data:
                    found_types.append(file_type)

        # Remove duplicates
        found_types = list(set(found_types))

        if len(found_types) > 1:
            return f"⚠ Multiple file signatures detected: {', '.join(found_types)}"
        elif len(found_types) == 1:
            return f"Single file type detected: {found_types[0]}"
        else:
            return "No known signature found"

    except Exception as e:
        return f"Error: {str(e)}"