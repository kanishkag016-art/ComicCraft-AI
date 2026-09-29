import os
import requests
from urllib.parse import quote
import random
import time

PANELS_DIR = "app/static/panels"
os.makedirs(PANELS_DIR, exist_ok=True)


def generate_image(image_prompt, file_path):
    panel_name = os.path.basename(file_path)

    # PANEL 2 - ARIA ENTERING CRYSTAL CAVE
    if "panel_2" in panel_name:
        image_prompt = """
        Aria is a brave young female adventurer walking into a huge
        underground crystal cave. Show Aria from behind as she enters
        through a mysterious glowing cave entrance. Thousands of bright
        blue and cyan crystals cover the walls, ceiling and ground.
        Aria carries a small adventure backpack and looks amazed at
        the magical cave in front of her. A beautiful blue glow lights
        the path deep inside the cave.
        Fantasy anime comic book illustration, cinematic wide shot,
        dramatic perspective, magical atmosphere, beautiful blue
        crystal lighting, highly detailed, professional comic artwork,
        consistent character design, no text, no letters, no words.
        """

        print("=== PANEL 2 SPECIAL IMAGE GENERATION ===")

    # OTHER PANELS
    else:
        image_prompt = (
            f"{image_prompt}, "
            "beautiful anime fantasy comic illustration, "
            "cinematic lighting, highly detailed, "
            "professional comic book artwork, "
            "consistent character design, "
            "no text, no letters, no words, no captions"
        )

    # IMAGE GENERATION
    for attempt in range(1, 6):
        try:
            seed = random.randint(100000, 999999999)

            final_prompt = (
                f"{image_prompt}. "
                f"Create a unique comic panel for {panel_name}. "
                "Do not create text, letters, words or captions "
                "inside the image."
            )

            encoded_prompt = quote(final_prompt)

            url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                f"?width=768"
                f"&height=768"
                f"&seed={seed}"
                f"&nologo=true"
            )

            print(
                f"Generating {panel_name} - Attempt {attempt}"
            )

            response = requests.get(
                url,
                timeout=180
            )

            response.raise_for_status()

            print(
                f"Received {len(response.content)} bytes "
                f"for {panel_name}"
            )

            if len(response.content) < 10000:
                raise Exception("Image response too small")

            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"SUCCESS: {panel_name}")

            return file_path

        except Exception as e:
            print(
                f"FAILED: {panel_name} - {e}"
            )

            if attempt < 5:
                time.sleep(5)

    print(f"FINAL FAILURE: {panel_name}")

    return None