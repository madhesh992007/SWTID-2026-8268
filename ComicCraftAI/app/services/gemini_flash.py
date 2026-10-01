from ..config import get_settings
from ..models import (
    OutlineResponse,
    PromptRequest,
)


def _demo_outline(
    request: PromptRequest,
) -> OutlineResponse:

    beats = [
        (
            "The Spark",
            (
                f"{request.character_name} discovers "
                f"a strange clue in {request.setting}."
            ),
        ),
        (
            "Into the Unknown",
            (
                f"{request.character_name} follows "
                f"the clue deeper into {request.setting}."
            ),
        ),
        (
            "The Turning Point",
            (
                f"A surprising obstacle forces "
                f"{request.character_name} to rethink the plan."
            ),
        ),
        (
            "The Brave Choice",
            (
                f"{request.character_name} makes a courageous "
                f"choice that changes everything."
            ),
        ),
        (
            "A New Beginning",
            (
                f"The mystery is resolved, leaving "
                f"{request.character_name} with a memorable lesson."
            ),
        ),
    ]

    panels = []

    for number, (title, description) in enumerate(
        beats,
        start=1,
    ):
        panels.append(
            {
                "panel_number": number,
                "title": title,
                "scene_description": description,
                "image_prompt": (
                    f"{request.art_style} comic illustration, "
                    f"{request.tone} mood, "
                    f"{request.character_name} in "
                    f"{request.setting}, "
                    f"{description} "
                    "cinematic composition, "
                    "expressive character, "
                    "clean comic linework, "
                    "no text, no speech bubbles"
                ),
            }
        )

    return OutlineResponse(
        panels=panels
    )


def generate_outline(
    request: PromptRequest,
) -> OutlineResponse:

    settings = get_settings()

    if settings.demo_mode:
        return _demo_outline(request)

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is required "
            "when DEMO_MODE=false."
        )

    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a coherent five-panel comic outline.

User story prompt:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Return exactly five panels.

Each panel must contain:

- panel_number: 1 through 5
- title: short panel title
- scene_description: vivid but concise description
- image_prompt: detailed prompt for an image generator

Image prompts must maintain the same character,
setting, visual style, and continuity.

Do not request readable text in images.

Make the final panel meaningfully resolve or advance
the story.
""".strip()

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutlineResponse,
            temperature=0.9,
            max_output_tokens=2500,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    return OutlineResponse.model_validate_json(
        response.text
    )