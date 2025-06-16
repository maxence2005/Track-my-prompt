def hex_to_bgr(hex_color: str):
    if hex_color.lower() == "rainbow":
        return "rainbow"
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        try:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return (b, g, r)
        except ValueError:
            pass
    return (0, 255, 0)  # Vert
