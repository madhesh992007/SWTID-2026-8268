from ..config import get_settings
from ..models import (
    OutlineResponse,
    PanelStory,
    PromptRequest,
    StoryResponse,
)


def _demo_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    panels = []

    for panel in outline.panels:

        panels.append(
            PanelStory(
                panel_number=panel.panel_number,

                caption=(
                    f"{request.setting.upper()} — "
                    f"{panel.title}"
                ),

                narration=(
                    f"{request.character_name} moves through "
                    f"the moment with a {request.tone} spirit. "
                    f"{panel.scene_description}"
                ),

                dialogue=(
                    f'"We can do this," '
                    f'{request.character_name} says, '
                    f'"one brave step at a time."'
                ),
            )
        )

    return StoryResponse(
        panels=panels
    )


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    settings = get_settings()

    if settings.demo_mode:
        return _demo_story(
            request,
            outline,
        )

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
Expand the following five-panel comic outline
into polished narration, captions, and dialogue.

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Original story:
{request.story_prompt}

Outline:
{outline.model_dump_json(indent=2)}

Return exactly five panel story objects.

Each object must contain:

- panel_number
- caption
- narration
- dialogue

Requirements:

1. Keep the story continuous.
2. Do not create extra panels.
3. Keep dialogue short and natural.
4. Match the requested tone.
5. Make each panel move the story forward.
6. Keep content family-friendly.
""".strip()

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StoryResponse,
            temperature=0.95,
            max_output_tokens=3500,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty story."
        )

    return StoryResponse.model_validate_json(
        response.text
    )