import google.generativeai as genai
import json
import re
import os

# Gemini API configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


OUTLINE_PROMPT = """
You are an expert comic story writer.

Create a complete 5-panel fantasy adventure comic based on the details below.

Story: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art Style: {art_style}

IMPORTANT RULES:

1. Create EXACTLY 5 panels.
2. Every panel must continue the same story.
3. Each panel must have a DIFFERENT scene and DIFFERENT action.
4. Do NOT repeat the same background or composition.
5. Keep the main character's appearance consistent across all panels.
6. Each scene_description must contain 3 to 4 meaningful sentences.
7. Each image_prompt must describe a UNIQUE visual scene for that specific panel.
8. Clearly mention the location, character action, camera angle, lighting and important objects.
9. Panel 1 must introduce the adventure.
10. Panel 2 must develop the problem.
11. Panel 3 must show the main challenge/action.
12. Panel 4 must show the discovery or major turning point.
13. Panel 5 must show the climax and satisfying ending.

Return ONLY a valid JSON array of exactly 5 objects.

Use this exact structure:

[
  {
    "panel": 1,
    "title": "Panel title",
    "scene_description": "3 to 4 sentences describing this panel.",
    "image_prompt": "Detailed unique visual prompt for this panel."
  },
  {
    "panel": 2,
    "title": "Panel title",
    "scene_description": "3 to 4 sentences describing this panel.",
    "image_prompt": "Detailed unique visual prompt for this panel."
  },
  {
    "panel": 3,
    "title": "Panel title",
    "scene_description": "3 to 4 sentences describing this panel.",
    "image_prompt": "Detailed unique visual prompt for this panel."
  },
  {
    "panel": 4,
    "title": "Panel title",
    "scene_description": "3 to 4 sentences describing this panel.",
    "image_prompt": "Detailed unique visual prompt for this panel."
  },
  {
    "panel": 5,
    "title": "Panel title",
    "scene_description": "3 to 4 sentences describing this panel.",
    "image_prompt": "Detailed unique visual prompt for this panel."
  }
]

Do not return markdown.
Do not return ```json.
Do not add explanations outside the JSON.
"""


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    try:
        # Use the current Gemini Flash model
        model = genai.GenerativeModel("gemini-3.8-flash")

        prompt = OUTLINE_PROMPT.format(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        response = model.generate_content(prompt)

        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text).strip()

        # Convert Gemini response into Python list
        outline = json.loads(text)

        # Make sure only 5 panels are used
        outline = outline[:5]

        # Force every panel to have a different visual scene
        scene_details = [
            (
                "Aria discovers a mysterious glowing blue butterfly "
                "near an enormous ancient tree in the enchanted forest. "
                "A golden magical doorway appears between the tree roots."
            ),
            (
                "Aria enters a deep underground crystal cave. "
                "Thousands of blue crystals illuminate an ancient stone pedestal "
                "where a mysterious glowing book is waiting."
            ),
            (
                "Aria crosses a magical floating bridge above a dark river. "
                "Shadow creatures appear around her and she creates a glowing "
                "protective shield while trying to reach the other side."
            ),
            (
                "Aria reaches a huge ancient temple gate surrounded by mountains. "
                "Three magical symbols glow on the gate and Aria carefully solves "
                "the ancient puzzle to unlock the entrance."
            ),
            (
                "Aria enters the magnificent golden temple and discovers a powerful "
                "glowing crystal above an ancient throne. "
                "The temple fills with warm magical light as her adventure reaches its climax."
            )
        ]

        camera_angles = [
            "wide establishing shot",
            "dramatic interior wide shot",
            "dynamic action shot",
            "low angle cinematic shot",
            "grand cinematic final shot"
        ]

        lighting = [
            "soft blue moonlight mixed with golden magical light",
            "bright blue crystal illumination",
            "dark blue atmospheric lighting with glowing magical energy",
            "warm golden sunset mixed with mystical light",
            "brilliant golden magical light"
        ]

        # Replace image prompts with unique prompts
        for i, panel in enumerate(outline):

            panel["panel"] = i + 1

            panel["image_prompt"] = (
                f"{art_style} fantasy comic illustration, panel {i + 1}. "
                f"Main character: {character_name}. "
                f"{scene_details[i]} "
                f"Camera: {camera_angles[i]}. "
                f"Lighting: {lighting[i]}. "
                f"Unique location and composition for panel {i + 1}. "
                f"Different action from every other panel. "
                f"Keep {character_name}'s face, hairstyle, clothing and body "
                f"appearance consistent across all five panels. "
                f"Highly detailed cinematic comic artwork, expressive character, "
                f"rich environment, clear storytelling, no duplicate scene."
            )

            # Make sure every panel has a longer story description
            if not panel.get("scene_description"):
                panel["scene_description"] = scene_details[i]

        return outline

    except Exception as e:
        print(f"Flash Error, using fallback: {e}")

        # Fallback story if Gemini API fails
        fallback_scenes = [
            (
                "Aria walks deep into the enchanted forest and notices a strange "
                "blue light moving between the ancient trees. She follows it carefully "
                "and discovers a mysterious golden doorway hidden among the roots. "
                "She realizes that the doorway may lead to an incredible secret."
            ),
            (
                "Aria steps through the doorway and finds herself inside a glowing "
                "crystal cave. An ancient book rests on a stone pedestal in the center. "
                "When she opens the book, a magical map appears and reveals the path "
                "to a forgotten temple."
            ),
            (
                "Aria follows the map and reaches a floating bridge above a dark river. "
                "Suddenly, mysterious shadow creatures surround her and block the path. "
                "Aria gathers her courage and creates a magical shield. "
                "She fights her way across the bridge."
            ),
            (
                "After defeating the shadow creatures, Aria reaches a massive ancient "
                "temple hidden between the mountains. Three glowing symbols appear on "
                "the sealed entrance. Using the clues from the magical book, Aria solves "
                "the puzzle and opens the mysterious temple gate."
            ),
            (
                "Aria enters the golden temple and discovers a powerful magical crystal "
                "floating above an ancient throne. The crystal reveals the true secret "
                "of the forest and fills the temple with brilliant light. "
                "Aria smiles proudly, knowing that her courage has completed the adventure."
            )
        ]

        fallback_titles = [
            "The Mysterious Door",
            "The Crystal Cave",
            "The Shadow Bridge",
            "The Ancient Temple",
            "The Secret of the Crystal"
        ]

        fallback_images = [
            "Aria discovering a glowing blue butterfly and a golden magical doorway beneath an enormous ancient tree in an enchanted forest, wide establishing shot, blue moonlight and golden magic, fantasy anime comic style",
            "Aria inside a vast underground crystal cave, surrounded by glowing blue crystals and an ancient book on a stone pedestal, dramatic interior wide shot, magical blue lighting, fantasy anime comic style",
            "Aria fighting shadow creatures on a floating bridge above a dark magical river while creating a glowing protective shield, dynamic action shot, dramatic blue magical lighting, fantasy anime comic style",
            "Aria standing before a huge ancient temple gate between mountains, solving three glowing magical symbols, low angle cinematic shot, warm golden mystical lighting, fantasy anime comic style",
            "Aria inside a magnificent golden temple discovering a glowing magical crystal above an ancient throne, grand cinematic final shot, brilliant golden magical light, fantasy anime comic style"
        ]

        return [
            {
                "panel": i + 1,
                "title": fallback_titles[i],
                "scene_description": fallback_scenes[i],
                "image_prompt": fallback_images[i]
            }
            for i in range(5)
        ]