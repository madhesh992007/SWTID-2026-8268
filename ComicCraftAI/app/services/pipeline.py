from ..models import (
    ComicResponse,
    PromptRequest,
)

from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout


def generate_comic(
    request: PromptRequest,
) -> ComicResponse:

    # --------------------------------
    # STEP 1 — Generate outline
    # --------------------------------

    outline = generate_outline(
        request
    )

    if len(outline.panels) != 5:
        raise RuntimeError(
            "The outline service returned "
            f"{len(outline.panels)} panels. "
            "Exactly 5 panels are required."
        )

    # --------------------------------
    # STEP 2 — Generate story
    # --------------------------------

    story = generate_story(
        request,
        outline,
    )

    if len(story.panels) != 5:
        raise RuntimeError(
            "The story service returned "
            f"{len(story.panels)} panels. "
            "Exactly 5 panels are required."
        )

    # --------------------------------
    # STEP 3 — Generate images
    # --------------------------------

    image_paths = []

    for panel in outline.panels:

        path = generate_image(
            panel.image_prompt,
            panel.panel_number,
        )

        image_paths.append(
            path
        )

    image_urls = [
        f"/static/panels/{path.name}"
        for path in image_paths
    ]

    # --------------------------------
    # STEP 4 — Build comic layout
    # --------------------------------

    layout = build_comic_layout(
        outline,
        story,
        image_urls,
    )

    # --------------------------------
    # STEP 5 — PDF
    # --------------------------------

    title = (
        f"{request.character_name}: "
        f"{outline.panels[0].title}"
    )

    pdf_path = save_pdf(
        layout,
        title,
    )

    # --------------------------------
    # FINAL RESPONSE
    # --------------------------------

    return ComicResponse(
        title=title,
        panels=layout,
        pdf_url=(
            f"/download/{pdf_path.name}"
        ),
    )