from otree.api import *
import json


TEXT = {
    "en": {
        "title": "Demographics",
        "title_battery": "A few more questions",
        "region": "Which region do you currently live in?",
        "province": "Which province do you live in?",
        "choose_region_first": "Please choose a region first",
        "select_province": "Select a province",
        "gender": "What is your gender?",
        "age_group": "Which age group do you belong to?",
        "education_level": "What is your highest level of education?",
        "income_bracket": "What is your household's net monthly income?",
        "region_choices": [("flanders", "Flanders"), ("wallonia", "Wallonia"), ("brussels", "Brussels-Capital Region")],
        "gender_choices": [("male", "Male"), ("female", "Female"), ("other", "Other / prefer not to say")],
        "age_choices": [("18_24", "18–24"), ("25_34", "25–34"), ("35_44", "35–44"), ("45_54", "45–54"), ("55_plus", "55+")],
        "edu_choices": [
            ("secondary_or_less", "Secondary or less"),
            ("bachelor", "Bachelor"),
            ("master", "Master"),
            ("phd", "PhD"),
            ("other", "Other / prefer not to say"),
        ],
        "income_choices": [
            ("lt_1500", "< €1,500"),
            ("1500_2499", "€1,500 – €2,499"),
            ("2500_3499", "€2,500 – €3,499"),
            ("3500_4999", "€3,500 – €4,999"),
            ("gte_5000", "≥ €5,000"),
            ("prefer_not", "Prefer not to say"),
        ],
        # Attitudinal battery
        "identity_strength": "How strongly do you identify with",
        "outgroup_closeness": "How close do you feel to",
        "scale_low": "not at all",
        "scale_high": "very strongly",
        "attention_check_q": "To confirm you are reading carefully, please select \"Agree\" for this question.",
        "attention_choices": [
            ("strongly_disagree", "Strongly disagree"),
            ("disagree", "Disagree"),
            ("neutral", "Neutral"),
            ("agree", "Agree"),
            ("strongly_agree", "Strongly agree"),
        ],
        "prior_belief": "In your opinion, what is the average amount donated to charity per year by a person living in Belgium? (in €)",
        "error_required": "Please fill in all required fields before continuing.",
        # Attitudinal filler items
        "filler_giving_importance": "How important is charitable giving to you personally?",
        "filler_importance_low": "not at all important",
        "filler_importance_high": "very important",
        "filler_donated_recently": "Have you donated to charity in the past 12 months?",
        "filler_donated_yes": "Yes",
        "filler_donated_no": "No",
        "filler_others_give": "Do you think most people in Belgium donate to charity regularly?",
        "filler_others_low": "very few people",
        "filler_others_high": "almost everyone",
    },
    "fr": {
        "title": "Informations générales",
        "title_battery": "Quelques questions supplémentaires",
        "region": "Dans quelle région vivez-vous actuellement ?",
        "province": "Dans quelle province résidez-vous ?",
        "choose_region_first": "Choisissez d'abord une région",
        "select_province": "Sélectionnez une province",
        "gender": "Quel est votre genre ?",
        "age_group": "Dans quelle tranche d'âge vous situez-vous ?",
        "education_level": "Quel est votre niveau d'éducation le plus élevé ?",
        "income_bracket": "Quel est le revenu net mensuel de votre ménage ?",
        "region_choices": [("flanders", "Région flamande"), ("wallonia", "Région wallonne"), ("brussels", "Région de Bruxelles-Capitale")],
        "gender_choices": [("male", "Homme"), ("female", "Femme"), ("other", "Autre / préfère ne pas répondre")],
        "age_choices": [("18_24", "18–24 ans"), ("25_34", "25–34 ans"), ("35_44", "35–44 ans"), ("45_54", "45–54 ans"), ("55_plus", "55 ans ou plus")],
        "edu_choices": [
            ("secondary_or_less", "Secondaire ou moins"),
            ("bachelor", "Bachelor"),
            ("master", "Master"),
            ("phd", "Doctorat"),
            ("other", "Autre / préfère ne pas répondre"),
        ],
        "income_choices": [
            ("lt_1500", "< 1 500 €"),
            ("1500_2499", "1 500 € – 2 499 €"),
            ("2500_3499", "2 500 € – 3 499 €"),
            ("3500_4999", "3 500 € – 4 999 €"),
            ("gte_5000", "≥ 5 000 €"),
            ("prefer_not", "Préfère ne pas répondre"),
        ],
        # Attitudinal battery
        "identity_strength": "Dans quelle mesure vous identifiez-vous à",
        "outgroup_closeness": "Dans quelle mesure vous sentez-vous proche de",
        "scale_low": "pas du tout",
        "scale_high": "très fortement",
        "attention_check_q": "Pour confirmer que vous lisez attentivement, veuillez sélectionner « D'accord » pour cette question.",
        "attention_choices": [
            ("strongly_disagree", "Pas du tout d'accord"),
            ("disagree", "Pas d'accord"),
            ("neutral", "Neutre"),
            ("agree", "D'accord"),
            ("strongly_agree", "Tout à fait d'accord"),
        ],
        "prior_belief": "Selon vous, quel est le montant moyen donné à des œuvres caritatives par an par une personne vivant en Belgique ? (en €)",
        "error_required": "Veuillez remplir tous les champs obligatoires avant de continuer.",
        # Attitudinal filler items
        "filler_giving_importance": "Quelle importance accordez-vous personnellement aux dons caritatifs ?",
        "filler_importance_low": "pas du tout important",
        "filler_importance_high": "très important",
        "filler_donated_recently": "Avez-vous fait un don à une œuvre caritative au cours des 12 derniers mois ?",
        "filler_donated_yes": "Oui",
        "filler_donated_no": "Non",
        "filler_others_give": "Pensez-vous que la plupart des gens en Belgique donnent régulièrement à des œuvres caritatives ?",
        "filler_others_low": "très peu de personnes",
        "filler_others_high": "presque tout le monde",
    },
    "nl": {
        "title": "Algemene informatie",
        "title_battery": "Nog enkele vragen",
        "region": "In welk gewest woont u momenteel?",
        "province": "In welke provincie woont u?",
        "choose_region_first": "Kies eerst een gewest",
        "select_province": "Selecteer een provincie",
        "gender": "Wat is uw gender?",
        "age_group": "Tot welke leeftijdsgroep behoort u?",
        "education_level": "Wat is uw hoogst behaalde opleidingsniveau?",
        "income_bracket": "Wat is het netto maandinkomen van uw huishouden?",
        "region_choices": [("flanders", "Vlaams Gewest"), ("wallonia", "Waals Gewest"), ("brussels", "Brussels Hoofdstedelijk Gewest")],
        "gender_choices": [("male", "Man"), ("female", "Vrouw"), ("other", "Anders / liever niet zeggen")],
        "age_choices": [("18_24", "18–24"), ("25_34", "25–34"), ("35_44", "35–44"), ("45_54", "45–54"), ("55_plus", "55+")],
        "edu_choices": [
            ("secondary_or_less", "Secundair of lager"),
            ("bachelor", "Bachelor"),
            ("master", "Master"),
            ("phd", "Doctoraat"),
            ("other", "Anders / liever niet zeggen"),
        ],
        "income_choices": [
            ("lt_1500", "< €1.500"),
            ("1500_2499", "€1.500 – €2.499"),
            ("2500_3499", "€2.500 – €3.499"),
            ("3500_4999", "€3.500 – €4.999"),
            ("gte_5000", "≥ €5.000"),
            ("prefer_not", "Liever niet zeggen"),
        ],
        # Attitudinal battery
        "identity_strength": "In welke mate identificeert u zich met",
        "outgroup_closeness": "In welke mate voelt u zich verbonden met",
        "scale_low": "helemaal niet",
        "scale_high": "zeer sterk",
        "attention_check_q": "Om te bevestigen dat u aandachtig leest, gelieve 'Akkoord' te selecteren voor deze vraag.",
        "attention_choices": [
            ("strongly_disagree", "Helemaal niet akkoord"),
            ("disagree", "Niet akkoord"),
            ("neutral", "Neutraal"),
            ("agree", "Akkoord"),
            ("strongly_agree", "Helemaal akkoord"),
        ],
        "prior_belief": "Hoeveel denkt u dat een persoon in België gemiddeld per jaar aan goede doelen schenkt? (in €)",
        "error_required": "Vul alle verplichte velden in voor u verdergaat.",
        # Attitudinal filler items
        "filler_giving_importance": "Hoe belangrijk is liefdadigheid voor u persoonlijk?",
        "filler_importance_low": "helemaal niet belangrijk",
        "filler_importance_high": "zeer belangrijk",
        "filler_donated_recently": "Heeft u in de afgelopen 12 maanden aan een goed doel gedoneerd?",
        "filler_donated_yes": "Ja",
        "filler_donated_no": "Nee",
        "filler_others_give": "Denkt u dat de meeste mensen in België regelmatig aan goede doelen doneren?",
        "filler_others_low": "heel weinig mensen",
        "filler_others_high": "bijna iedereen",
    },
}


PROVINCES = {
    "en": {
        "flanders": [("antwerp", "Antwerp"), ("flemish_brabant", "Flemish Brabant"), ("east_flanders", "East Flanders"), ("west_flanders", "West Flanders"), ("limburg", "Limburg")],
        "wallonia": [("hainaut", "Hainaut"), ("walloon_brabant", "Walloon Brabant"), ("namur", "Namur"), ("liege", "Liège"), ("luxembourg", "Luxembourg")],
        "brussels": [("brussels_capital", "Brussels-Capital")],
    },
    "fr": {
        "flanders": [("antwerp", "Anvers"), ("flemish_brabant", "Brabant flamand"), ("east_flanders", "Flandre orientale"), ("west_flanders", "Flandre occidentale"), ("limburg", "Limbourg")],
        "wallonia": [("hainaut", "Hainaut"), ("walloon_brabant", "Brabant wallon"), ("namur", "Namur"), ("liege", "Liège"), ("luxembourg", "Luxembourg")],
        "brussels": [("brussels_capital", "Bruxelles-Capitale")],
    },
    "nl": {
        "flanders": [("antwerp", "Antwerpen"), ("flemish_brabant", "Vlaams-Brabant"), ("east_flanders", "Oost-Vlaanderen"), ("west_flanders", "West-Vlaanderen"), ("limburg", "Limburg")],
        "wallonia": [("hainaut", "Henegouwen"), ("walloon_brabant", "Waals-Brabant"), ("namur", "Namen"), ("liege", "Luik"), ("luxembourg", "Luxemburg")],
        "brussels": [("brussels_capital", "Brussel-Hoofdstad")],
    },
}

# Localised region names used in identity question labels
REGION_LABELS = {
    "en": {"flanders": "Flanders", "wallonia": "Wallonia", "brussels": "Brussels"},
    "fr": {"flanders": "la Flandre", "wallonia": "la Wallonie", "brussels": "Bruxelles"},
    "nl": {"flanders": "Vlaanderen", "wallonia": "Wallonië", "brussels": "Brussel"},
}

OUTGROUP_LABELS = {
    "en": {"flanders": "Wallonia", "wallonia": "Flanders", "brussels": "Flanders and Wallonia"},
    "fr": {"flanders": "la Wallonie", "wallonia": "la Flandre", "brussels": "la Flandre et la Wallonie"},
    "nl": {"flanders": "Wallonië", "wallonia": "Vlaanderen", "brussels": "Vlaanderen en Wallonië"},
}


def get_lang(participant):
    lang = participant.vars.get("lang", "en")
    return lang if lang in TEXT else "en"


class Demographics(Page):
    form_model = "player"
    form_fields = ["region", "province", "gender", "age_group", "education_level", "income_bracket"]

    def vars_for_template(self):
        lang = get_lang(self.participant)
        t = TEXT[lang]
        return dict(
            t=t,
            lang=lang,
            province_map_json=json.dumps(PROVINCES[lang]),
        )

    def region_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def province_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def gender_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def age_group_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def education_level_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def income_bracket_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def error_message(self, values):
        # Cross-field check: province must belong to the selected region
        lang = get_lang(self.participant)
        region = values.get("region")
        province = values.get("province")
        if region and province:
            valid = set(p for p, _ in PROVINCES[lang].get(region, []))
            if province not in valid:
                return TEXT[lang]["select_province"]

    def before_next_page(self):
        self.participant.vars["region"] = self.player.region
        self.participant.vars["province"] = self.player.province
        self.participant.vars["gender"] = self.player.gender
        self.participant.vars["age_group"] = self.player.age_group
        self.participant.vars["education_level"] = self.player.education_level
        self.participant.vars["income_bracket"] = self.player.income_bracket


class AttitudinalBattery(Page):
    """Pre-treatment: identity measures, prior belief, attention check, filler items.
    Region is already in participant.vars (set by Demographics.before_next_page),
    allowing region-specific question labels.
    """
    form_model = "player"
    form_fields = [
        "identity_strength", "outgroup_closeness",
        "prior_belief", "attention_check",
        "filler_giving_importance", "filler_donated_recently", "filler_others_give",
    ]

    def vars_for_template(self):
        lang = get_lang(self.participant)
        t = TEXT[lang]
        region = self.participant.vars.get("region", "")
        ingroup_label = REGION_LABELS[lang].get(region, "your region")
        outgroup_label = OUTGROUP_LABELS[lang].get(region, "other regions")
        return dict(
            t=t,
            ingroup_label=ingroup_label,
            outgroup_label=outgroup_label,
        )

    def prior_belief_error_message(self, value):
        if value is None:
            return TEXT[get_lang(self.participant)]["error_required"]

    def attention_check_error_message(self, value):
        if not value:
            return TEXT[get_lang(self.participant)]["error_required"]

    def filler_donated_recently_error_message(self, value):
        if value is None:
            return TEXT[get_lang(self.participant)]["error_required"]

    def before_next_page(self):
        self.participant.vars["identity_strength"] = self.player.identity_strength
        self.participant.vars["outgroup_closeness"] = self.player.outgroup_closeness
        self.participant.vars["prior_belief"] = self.player.prior_belief
        passed = 1 if self.player.attention_check == "agree" else 0
        self.player.attention_check_passed = passed
        self.participant.vars["attention_check_passed"] = passed
        self.participant.vars["filler_giving_importance"] = self.player.filler_giving_importance
        self.participant.vars["filler_donated_recently"] = self.player.filler_donated_recently
        self.participant.vars["filler_others_give"] = self.player.filler_others_give


page_sequence = [Demographics, AttitudinalBattery]
