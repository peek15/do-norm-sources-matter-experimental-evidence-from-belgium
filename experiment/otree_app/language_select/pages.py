from otree.api import *
import time


TEXT = {
    "en": {"title": "Language", "choose": "Choose your language"},
    "fr": {"title": "Langue", "choose": "Choisissez votre langue"},
    "nl": {"title": "Taal", "choose": "Kies uw taal"},
}


def get_lang(participant):
    lang = participant.vars.get("lang", "en")
    return lang if lang in TEXT else "en"


class MyPage(Page):
    form_model = "player"
    form_fields = ["language"]

    def vars_for_template(self):
        lang = get_lang(self.participant)
        return dict(t=TEXT[lang])

    def before_next_page(self, timeout_happened=False, **kwargs):
        self.participant.vars["lang"] = self.language
        self.participant.vars["experiment_start"] = time.time()

page_sequence = [MyPage]
