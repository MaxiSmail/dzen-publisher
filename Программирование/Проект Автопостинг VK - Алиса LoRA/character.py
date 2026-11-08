"""
Character Profile (Visual DNA) — Master specifications for our AI host.
Locked to user-curated Redhead Persona (ALISA_HERO):
  - Vibrant rich red / copper wavy hair
  - Warm amber eyes, confident charismatic gaze
  - Clean smooth porcelain skin without freckles
  - Larger than average bust, curvy feminine figure
  - Completely NO tattoos, NO body ink, NO piercings, NO nose ring
  - Authentic 35mm film photography, Kodak Portra 400 aesthetic
"""

from __future__ import annotations

CHARACTER_NAME = "Алиса"
TRIGGER_WORD = "ALISA_HERO"

# Master Visual DNA for the Redhead Character
CHARACTER_DNA = (
    f"Authentic raw candid 35mm film photograph of the unique beautiful 24yo woman {TRIGGER_WORD}, "
    "striking vibrant rich red hair with soft natural waves, warm amber eyes with confident charismatic expression, "
    "clean smooth glowing porcelain skin without freckles, larger than average bust, curvy feminine realistic proportions, "
    "completely NO tattoos, NO body ink, NO piercings, NO nose ring, "
)

# Natural Photography Lighting & Texture (Anti-plastic, anti-CGI, raw candid look)
PHOTO_REALISM_STYLE = (
    ", captured on 35mm film camera, Kodak Portra 400 film stock, natural soft ambient lighting, "
    "candid documentary photography, subtle film grain, real lens bokeh, genuine human emotion, unedited raw photo"
)


def build_character_prompt(scene_action: str, outfit: str) -> str:
    """
    Construct a complete prompt combining the fixed character DNA,
    the per-post outfit, and the per-slide dynamic scene/pose.
    """
    outfit_part = f"wearing a {outfit.strip()}, "
    scene_part = scene_action.strip(", ")
    return f"{CHARACTER_DNA}{outfit_part}{scene_part}{PHOTO_REALISM_STYLE}"
