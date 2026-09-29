def build_comic_layout(panels):
    layout = []

    for i, panel in enumerate(panels, start=1):
        layout.append({
            "panel": i,
            "caption": panel.get("caption", ""),
            "narration": panel.get("narration", "")
        })

    return layout