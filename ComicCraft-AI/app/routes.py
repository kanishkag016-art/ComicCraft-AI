from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .models.gemini_flash import generate_outline
from .models.gemini_pro import generate_story
from .models.image_generator import generate_image
from .models.layout_builder import build_comic_layout

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    # 1. Generate outline
    outline = generate_outline(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    # 2. Generate story
    story_text = generate_story(
        outline,
        character_name,
        setting,
        tone
    )

    # 3. Generate images
    image_paths = []

    for panel in outline:
        image_path = generate_image(
            panel["image_prompt"],
            f"app/static/panels/panel_{panel['panel']}.png"
        )

        image_paths.append(image_path)

    # 4. Build layout
    layout = build_comic_layout(outline)

    # 5. Create preview directly
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ComicCraft - Comic Preview</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f2f2f2;
                margin: 0;
                padding: 30px;
            }

            .container {
                max-width: 900px;
                margin: auto;
            }

            h1 {
                text-align: center;
                color: #222;
            }

            .panel {
                background: white;
                padding: 20px;
                margin: 25px 0;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            }

            .panel h2 {
                color: #6c2bd9;
            }

            .panel img {
                width: 100%;
                max-width: 768px;
                display: block;
                margin: 15px auto;
                border-radius: 10px;
            }

            .scene {
                font-size: 17px;
                line-height: 1.6;
            }

            .story {
                white-space: pre-line;
                font-size: 17px;
                line-height: 1.7;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>✨ ComicCraft - Comic Preview ✨</h1>
    """

    for panel in outline:
        panel_number = panel["panel"]
        title = panel.get("title", f"Panel {panel_number}")
        scene = panel.get("scene_description", "")

        html += f"""
            <div class="panel">
                <h2>Panel {panel_number} - {title}</h2>

                <img src="/static/panels/panel_{panel_number}.png?v=2" alt="Panel {panel_number}">

                <div class="scene">
                    <strong>Scene:</strong>
                    <p>{scene}</p>
                </div>
            </div>
        """

    html += f"""
            <div class="panel">
                <h2>📖 Story</h2>
                <div class="story">{story_text}</div>
            </div>

        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


@router.post("/export")
async def export_comic(
    request: Request,
    character_name: str = Form("Aria")
):
    return JSONResponse(
        {
            "status": "success",
            "message": "Comic export completed!"
        }
    )