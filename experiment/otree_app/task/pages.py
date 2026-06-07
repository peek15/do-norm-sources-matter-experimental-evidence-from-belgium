from otree.api import *
from .models import C, assign_treatment, compute_norm_score
import time


TEXT = {
    "en": {
        "title_decision": "Decision",
        "title_final": "Final questions",
        "title_summary": "Summary",
        "p_context": (
            "You receive a hypothetical budget of {endowment} €. "
            "You can allocate it between yourself and a donation to a charitable organisation "
            "(e.g., supporting health research, disease prevention, or education)."
        ),
        "p_norm": (
            "According to data from SPF Finances (Belgian federal tax administration), "
            "the average annual amount donated to charity and declared by residents of {region} "
            "is approximately {norm_score} €."
        ),
        "p_norm_pct": (
            "For context, this represents approximately {norm_pct}% of the average annual net income "
            "in {region} (€{avg_income:,})."
        ),
        "p_filler": (
            "Charitable organisations like this one are active across different fields, "
            "including health research, disease prevention, and education. "
            "They rely in part on voluntary contributions from individuals."
        ),
        "amount_donated": "How much would you like to donate?",
        "keep_all": "keep all",
        "donate_all": "donate all",
        "donated": "Donated",
        "kept_label": "Kept",
        "kept": "kept",
        "looked_up_info": "Did you look up external information (e.g., online) while answering?",
        "yes": "Yes",
        "no": "No",

        "results_sentence": "You donated {donation} € and kept {keep} €.",
        "recall_bracket_question": "Earlier, you were shown the average annual donation in {region}. Which of the following best matches what you saw?",
        "recall_bracket_lt100": "Less than €100",
        "recall_bracket_100_200": "€100–€200",
        "recall_bracket_200_300": "€200–€300",
        "recall_bracket_300_400": "€300–€400",
        "recall_bracket_gt400": "More than €400",
        "recall_bracket_no_figure": "I did not see a figure",
        "norm_credibility": "How credible did you find the information about average donations in your region?",
        "credibility_low": "Not at all credible",
        "credibility_high": "Completely credible",
        "belief_update_question": "Compared to what you expected, do you think people in this region donate more or less than you thought?",
        "belief_update_much_more": "Much more than I expected",
        "belief_update_somewhat_more": "Somewhat more than I expected",
        "belief_update_as_expected": "About what I expected",
        "belief_update_somewhat_less": "Somewhat less than I expected",
        "belief_update_much_less": "Much less than I expected",
        "debrief_title": "Thank you!",
        "debrief_body": (
            "Your participation is greatly appreciated. "
            "This study examines how information about others' charitable behaviour influences individual giving decisions. "
            "Your responses will contribute to research on social norms and charity in Belgium."
        ),
        "debrief_contact": "If you have any questions about this study, feel free to reach out: theo.mauroy@student.uclouvain.be",
        "error_required": "Please fill in all required fields before continuing.",
    },

    "fr": {
        "title_decision": "Décision",
        "title_final": "Questions finales",
        "title_summary": "Récapitulatif",
        "p_context": (
            "Vous disposez d’un budget hypothétique de {endowment} €. "
            "Vous pouvez le répartir entre vous-même et une donation à une organisation caritative "
            "(par exemple soutenant la recherche en santé, la prévention des maladies ou l’éducation)."
        ),
        # NOTE: {region} already contains "de Flandre"/"de Wallonie"
        "p_norm": (
            "Selon les données du SPF Finances (administration fiscale fédérale belge), "
            "le montant annuel moyen donné à des œuvres caritatives et déclaré par les habitants {region} "
            "est d’environ {norm_score} €."
        ),
        "p_norm_pct": (
            "À titre de contexte, cela représente environ {norm_pct}% du revenu net annuel moyen "
            "{region} ({avg_income:,} €)."
        ),
        "p_filler": (
            "Les organisations caritatives comme celle-ci interviennent dans différents domaines, "
            "notamment la recherche en santé, la prévention des maladies et l’éducation. "
            "Elles dépendent en partie des contributions volontaires des particuliers."
        ),
        "amount_donated": "Quel montant souhaitez-vous donner ?",
        "keep_all": "tout garder",
        "donate_all": "tout donner",
        "donated": "Donné",
        "kept_label": "Gardé",
        "kept": "gardé",
        "looked_up_info": "Avez-vous consulté une information externe (par exemple en ligne) pendant vos réponses ?",
        "yes": "Oui",
        "no": "Non",

        "results_sentence": "Vous avez donné {donation} € et gardé {keep} €.",
        "recall_bracket_question": "Plus tôt, vous avez vu le don annuel moyen {region}. Lequel des éléments suivants correspond le mieux à ce que vous avez vu ?",
        "recall_bracket_lt100": "Moins de 100 €",
        "recall_bracket_100_200": "100 €–200 €",
        "recall_bracket_200_300": "200 €–300 €",
        "recall_bracket_300_400": "300 €–400 €",
        "recall_bracket_gt400": "Plus de 400 €",
        "recall_bracket_no_figure": "Je n'ai pas vu de chiffre",
        "norm_credibility": "Dans quelle mesure avez-vous trouvé crédible l'information sur les dons moyens dans votre région ?",
        "credibility_low": "Pas du tout crédible",
        "credibility_high": "Tout à fait crédible",
        "belief_update_question": "Par rapport à ce que vous attendiez, pensez-vous que les personnes dans cette région donnent plus ou moins que vous ne le pensiez ?",
        "belief_update_much_more": "Beaucoup plus que prévu",
        "belief_update_somewhat_more": "Un peu plus que prévu",
        "belief_update_as_expected": "À peu près ce que j'attendais",
        "belief_update_somewhat_less": "Un peu moins que prévu",
        "belief_update_much_less": "Beaucoup moins que prévu",
        "debrief_title": "Merci !",
        "debrief_body": (
            "Votre participation est vivement appréciée. "
            "Cette étude examine dans quelle mesure l'information sur le comportement charitable d'autrui influence les décisions individuelles de don. "
            "Vos réponses contribueront à la recherche sur les normes sociales et la charité en Belgique."
        ),
        "debrief_contact": "Si vous avez des questions concernant cette étude, n'hésitez pas à me contacter : theo.mauroy@student.uclouvain.be",
        "error_required": "Veuillez remplir tous les champs obligatoires avant de continuer.",
    },

    "nl": {
        "title_decision": "Beslissing",
        "title_final": "Laatste vragen",
        "title_summary": "Samenvatting",
        "p_context": (
            "U krijgt een hypothetisch budget van {endowment} €. "
            "U kunt dit verdelen tussen uzelf en een donatie aan een goed doel "
            "(bijv. gezondheidsonderzoek, ziektepreventie of onderwijs)."
        ),
        "p_norm": (
            "Volgens gegevens van de FOD Financiën (federale belastingadministratie) "
            "bedraagt het gemiddelde jaarlijkse bedrag dat inwoners van {region} schenken aan goede doelen "
            "en aangeven in hun belastingaangifte ongeveer {norm_score} €."
        ),
        "p_norm_pct": (
            "Ter vergelijking: dit vertegenwoordigt ongeveer {norm_pct}% van het gemiddelde jaarlijkse netto-inkomen "
            "in {region} (€{avg_income:,})."
        ),
        "p_filler": (
            "Goede doelen zoals dit zijn actief in verschillende domeinen, "
            "waaronder gezondheidsonderzoek, ziektepreventie en onderwijs. "
            "Ze steunen deels op vrijwillige bijdragen van particulieren."
        ),
        "amount_donated": "Hoeveel wilt u doneren?",
        "keep_all": "alles houden",
        "donate_all": "alles doneren",
        "donated": "Gedoneerd",
        "kept_label": "Behouden",
        "kept": "behouden",
        "looked_up_info": "Heeft u externe informatie opgezocht (bijv. online) tijdens het invullen?",
        "yes": "Ja",
        "no": "Nee",

        "results_sentence": "U doneerde {donation} € en behield {keep} €.",
        "recall_bracket_question": "Eerder werd u het gemiddelde jaarlijkse donatiebedrag in {region} getoond. Welk van de volgende opties komt het beste overeen met wat u zag?",
        "recall_bracket_lt100": "Minder dan €100",
        "recall_bracket_100_200": "€100–€200",
        "recall_bracket_200_300": "€200–€300",
        "recall_bracket_300_400": "€300–€400",
        "recall_bracket_gt400": "Meer dan €400",
        "recall_bracket_no_figure": "Ik heb geen getal gezien",
        "norm_credibility": "Hoe geloofwaardig vond u de informatie over de gemiddelde donaties in uw regio?",
        "credibility_low": "Helemaal niet geloofwaardig",
        "credibility_high": "Volledig geloofwaardig",
        "belief_update_question": "Vergeleken met wat u verwachtte, denkt u dat mensen in deze regio meer of minder geven dan u had gedacht?",
        "belief_update_much_more": "Veel meer dan ik verwachtte",
        "belief_update_somewhat_more": "Iets meer dan ik verwachtte",
        "belief_update_as_expected": "Ongeveer wat ik verwachtte",
        "belief_update_somewhat_less": "Iets minder dan ik verwachtte",
        "belief_update_much_less": "Veel minder dan ik verwachtte",
        "debrief_title": "Dank u wel!",
        "debrief_body": (
            "Uw deelname wordt zeer gewaardeerd. "
            "Dit onderzoek bestudeert hoe informatie over het charitatieve gedrag van anderen individuele schenkingsbeslissingen beïnvloedt. "
            "Uw antwoorden dragen bij aan onderzoek naar sociale normen en vrijgevigheid in België."
        ),
        "debrief_contact": "Als u vragen heeft over dit onderzoek, neem dan gerust contact op: theo.mauroy@student.uclouvain.be",
        "error_required": "Vul alle verplichte velden in voor u verdergaat.",
    },
}

# Bracket recall options: (stored code, TEXT key)
# recall_correct = 1 if code in ("200_300", "300_400") — the bracket spanning €301–€309
RECALL_BRACKETS = [
    ("lt100",    "recall_bracket_lt100"),
    ("100_200",  "recall_bracket_100_200"),
    ("200_300",  "recall_bracket_200_300"),
    ("300_400",  "recall_bracket_300_400"),
    ("gt400",    "recall_bracket_gt400"),
    ("no_figure","recall_bracket_no_figure"),
]

# Belief update direction options: (integer value, TEXT key)
BELIEF_OPTIONS = [
    ( 2, "belief_update_much_more"),
    ( 1, "belief_update_somewhat_more"),
    ( 0, "belief_update_as_expected"),
    (-1, "belief_update_somewhat_less"),
    (-2, "belief_update_much_less"),
]

REGION_LABELS = {
    "en": {"flanders": "Flanders", "wallonia": "Wallonia", "brussels": "Brussels"},
    "fr": {"flanders": "la Flandre", "wallonia": "la Wallonie", "brussels": "Bruxelles"},
    "nl": {"flanders": "Vlaanderen", "wallonia": "Wallonië", "brussels": "Brussel"},
}


def get_lang(participant):
    lang = participant.vars.get("lang", "en")
    return lang if lang in TEXT else "en"


class Decision(Page):
    form_model = "player"
    form_fields = ["donation"]

    def vars_for_template(self):
        assign_treatment(self.participant)
        # Record page arrival time for norm_page_time calculation
        self.participant.vars["decision_page_start"] = time.time()

        lang = get_lang(self.participant)
        t = TEXT[lang]

        condition = self.participant.vars.get("norm_condition")
        norm_region = self.participant.vars.get("norm_region")
        show_norm = (condition == "norm")

        p_context = t["p_context"].format(endowment=C.ENDOWMENT)

        norm_score = None
        p_norm = None

        p_norm_pct = None

        if show_norm:
            norm_score = compute_norm_score(self.participant)
            self.participant.vars["norm_score"] = norm_score

            region_label = REGION_LABELS[lang].get(norm_region, "")
            region_label_pct = region_label  # used in pct sentence (same form for EN/NL)

            if lang == "fr":
                region_label = f"de {region_label}"  # "de la Flandre" / "de la Wallonie" for p_norm
                # p_norm_pct uses preposition "en" without article (correct French)
                if norm_region == "brussels":
                    region_label_pct = "à Bruxelles"
                elif norm_region == "flanders":
                    region_label_pct = "en Flandre"
                else:
                    region_label_pct = "en Wallonie"

            p_norm = t["p_norm"].format(
                norm_score=norm_score,
                region=region_label,
            )

            norm_pct = C.NORM_PCT.get(norm_region)
            avg_income = C.AVG_INCOME.get(norm_region)
            if norm_pct is not None:
                p_norm_pct = t["p_norm_pct"].format(
                    norm_pct=norm_pct,
                    avg_income=avg_income,
                    region=region_label_pct,
                )
        else:
            self.participant.vars["norm_score"] = None

        return dict(
            t=t,
            endowment=C.ENDOWMENT,
            show_norm=show_norm,
            p_context=p_context,
            p_norm=p_norm,
            p_norm_pct=p_norm_pct,
            p_filler=t["p_filler"],
            amount_donated_label=t["amount_donated"],
        )

    def before_next_page(self, timeout_happened=False, **kwargs):
        start = self.participant.vars.get("decision_page_start")
        if start is not None:
            self.player.norm_page_time = int(time.time() - start)


class PostExperiment(Page):
    """Norm recall (bracket) + belief update direction + credibility + external info check."""
    form_model = "player"
    form_fields = [
        "looked_up_info",
        "norm_recall_bracket",
        "norm_credibility",
        "belief_update_direction",
    ]

    def looked_up_info_error_message(self, value):
        if value is None:
            return TEXT[get_lang(self.participant)]["error_required"]

    def error_message(self, values):
        # norm_recall_bracket and belief_update_direction are blank=True so oTree
        # won't catch them at field level; enforce here for treated participants only
        if self.participant.vars.get("norm_condition") == "norm":
            if not values.get("norm_recall_bracket"):
                return TEXT[get_lang(self.participant)]["error_required"]
            if values.get("belief_update_direction") is None:
                return TEXT[get_lang(self.participant)]["error_required"]

    def vars_for_template(self):
        lang = get_lang(self.participant)
        t = TEXT[lang]
        show_recall = self.participant.vars.get("norm_condition") == "norm"

        recall_bracket_question = ""
        if show_recall:
            norm_region = self.participant.vars.get("norm_region", "")
            region_label = REGION_LABELS[lang].get(norm_region, "")
            if lang == "fr":
                region_label = f"en {region_label}" if norm_region != "brussels" else "à Bruxelles"
            recall_bracket_question = t["recall_bracket_question"].format(region=region_label)

        recall_brackets = [(code, t[key]) for code, key in RECALL_BRACKETS]
        belief_options = [(val, t[key]) for val, key in BELIEF_OPTIONS]

        return dict(
            t=t,
            show_recall=show_recall,
            recall_bracket_question=recall_bracket_question,
            recall_brackets=recall_brackets,
            belief_options=belief_options,
        )

    def before_next_page(self, timeout_happened=False, **kwargs):
        if self.participant.vars.get("norm_condition") == "norm":
            bracket = self.player.norm_recall_bracket
            # Correct if bracket is €300–€400 (spans both €301 WA and €309 FL)
            self.player.recall_correct = 1 if bracket == "300_400" else 0
        # Control participants: recall_correct and belief_update_direction remain None (blank)


class Debrief(Page):
    def vars_for_template(self):
        lang = get_lang(self.participant)
        t = TEXT[lang]
        keep = C.ENDOWMENT - self.player.donation
        return dict(
            t=t,
            results_sentence=t["results_sentence"].format(
                donation=self.player.donation,
                keep=keep,
            ),
        )


page_sequence = [Decision, PostExperiment, Debrief]
