from otree.api import *


TEXT = {
    "en": {
        "title": "Informed Consent",
        "body": (
            "This study is conducted as part of a master's thesis in economics at "
            "UCLouvain – Università degli Studi di Milano. It examines attitudes and decisions "
            "related to charitable giving. You will complete a short survey and one decision task "
            "(~10 minutes). No real money is involved."
        ),
        "bullets": [
            "Your responses are completely anonymous.",
            "Data will be used for academic research only.",
            "Participation is voluntary — you may stop at any time.",
        ],
        "contact": "Questions? Contact: theo.mauroy@student.uclouvain.be",
        "checkbox_label": "I have read the above and agree to participate.",
        "error_must_consent": "You must agree to participate in order to continue.",
    },
    "fr": {
        "title": "Consentement éclairé",
        "body": (
            "Cette étude est menée dans le cadre d'un mémoire de master en économie à "
            "l'UCLouvain – Università degli Studi di Milano. Elle porte sur les attitudes et "
            "décisions liées aux dons caritatifs. Vous remplirez un court questionnaire et "
            "effectuerez une tâche de décision (~10 minutes). Aucun argent réel n'est impliqué."
        ),
        "bullets": [
            "Vos réponses sont totalement anonymes.",
            "Les données seront utilisées à des fins de recherche académique uniquement.",
            "La participation est volontaire — vous pouvez arrêter à tout moment.",
        ],
        "contact": "Questions ? Contactez : theo.mauroy@student.uclouvain.be",
        "checkbox_label": "J'ai lu ce qui précède et j'accepte de participer.",
        "error_must_consent": "Vous devez accepter de participer pour continuer.",
    },
    "nl": {
        "title": "Geïnformeerde toestemming",
        "body": (
            "Dit onderzoek wordt uitgevoerd als onderdeel van een masterthesis in de economie aan "
            "UCLouvain – Università degli Studi di Milano. Het bestudeert attitudes en beslissingen "
            "rond liefdadigheidsdonaties. U vult een korte enquête in en voltooit één beslissingstaak "
            "(~10 minuten). Er is geen echt geld mee gemoeid."
        ),
        "bullets": [
            "Uw antwoorden zijn volledig anoniem.",
            "Gegevens worden uitsluitend voor academisch onderzoek gebruikt.",
            "Deelname is vrijwillig — u kunt op elk moment stoppen.",
        ],
        "contact": "Vragen? Neem contact op: theo.mauroy@student.uclouvain.be",
        "checkbox_label": "Ik heb het bovenstaande gelezen en ga akkoord met deelname.",
        "error_must_consent": "U moet akkoord gaan met deelname om door te gaan.",
    },
}


def get_lang(participant):
    lang = participant.vars.get("lang", "en")
    return lang if lang in TEXT else "en"


class ConsentPage(Page):
    form_model = "player"
    form_fields = ["consent_given"]

    def vars_for_template(self):
        lang = get_lang(self.participant)
        return dict(t=TEXT[lang])

    def error_message(self, values):
        lang = get_lang(self.participant)
        if not values.get("consent_given"):
            return TEXT[lang]["error_must_consent"]


page_sequence = [ConsentPage]
