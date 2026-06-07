from os import environ

# -----------------------------
# Experiment parameters (V1)
# -----------------------------
ENDOWMENT = 100
CAUSE_LABEL = "Health research"

SESSION_CONFIGS = [
    # Full experiment (production)
    dict(
        name="thesis_v2",
        display_name="Thesis V2 — Full experiment",
        app_sequence=[
            "language_select",
            "consent",
            "mini_demographics",
            "task",
        ],
        num_demo_participants=9,  # 3 per arm for demo
    ),
    # Quick test: skip language + consent, 3 participants
    dict(
        name="test_quick",
        display_name="TEST — Quick (no language/consent)",
        app_sequence=[
            "mini_demographics",
            "task",
        ],
        num_demo_participants=3,
    ),
]



SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# --- i18n / languages ---
LANGUAGE_CODE = "en"
USE_I18N = False
USE_L10N = False


REAL_WORLD_CURRENCY_CODE = "EUR"
USE_POINTS = True

ADMIN_USERNAME = "theo"
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get("OTREE_SECRET_KEY", "set-this-in-production")

ROOMS = [
    dict(
        name='thesis_room',
        display_name='Thesis Experiment',
    ),
]
