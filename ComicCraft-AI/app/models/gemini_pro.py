import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

STORY_PROMPT = """
You are a professional comic story writer.

Expand the given 5-panel comic outline into a detailed and engaging comic story.

Outline:
{outline}

Character: {character_name}
Setting: {setting}
Tone: {tone}

IMPORTANT:
- Write exactly 5 panels.
- Each panel must contain a Caption and Narration.
- Each Caption should be 2 to 3 sentences.
- Each Narration should be 3 to 5 sentences.
- Include natural dialogue from the character when appropriate.
- Make every panel different from the previous panel.
- Continue the story naturally from one panel to the next.
- Do not repeat the same sentences.
- Describe actions, emotions, surroundings, obstacles and discoveries.
- Make the complete story detailed and interesting.
- The final panel must provide a proper ending.

Return exactly in this format:

PANEL 1:
Caption: ...
Narration: ...

PANEL 2:
Caption: ...
Narration: ...

PANEL 3:
Caption: ...
Narration: ...

PANEL 4:
Caption: ...
Narration: ...

PANEL 5:
Caption: ...
Narration: ...
"""


def generate_story(outline, character_name, setting, tone):
    try:
        model = genai.GenerativeModel("gemini-3.8-flash")

        prompt = STORY_PROMPT.format(
            outline=str(outline),
            character_name=character_name,
            setting=setting,
            tone=tone
        )

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"Pro Error: {e}")

        story = ""

        for p in outline:
            panel = p["panel"]

            story += f"""
PANEL {panel}:
Caption: {p["scene_description"]}. The atmosphere around {character_name} changes as the adventure continues.

Narration: {character_name} carefully moves through the {setting}. 
The journey becomes more challenging, but {character_name} refuses to give up. 
Using courage and intelligence, {character_name} studies the surroundings and searches for the next clue. 
Every discovery brings {character_name} closer to solving the mystery.
"""

            story += "\n"

        return story