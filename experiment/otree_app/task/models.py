from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = "task"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ENDOWMENT = 100

    # Real SPF Finances annual charitable donation averages (declared, per region):
    # Source: SPF Finances administrative data
    # Brussels excluded as norm source (~2x higher, creates magnitude confound)
    NORM_SCORES = {
        "flanders": 309,
        "wallonia": 301,
    }

    # Average annual net income per region (source: Statbel)
    AVG_INCOME = {
        "flanders": 21776,
        "wallonia": 19192,
    }

    # Percentage of income: 309/21776 = 1.42%, 301/19192 = 1.57%
    NORM_PCT = {
        "flanders": round(309 / 21776 * 100, 2),  # 1.42
        "wallonia": round(301 / 19192 * 100, 2),  # 1.57
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        """
        Block randomization: 3 arms at ~33% each.
          - control
          - norm_flanders
          - norm_wallonia
        Brussels is excluded as a norm source (incompatible norm value).
        Brussels participants are retained in the sample but receive control or
        one of the two regional norms like any other participant.
        """
        players = self.get_players()
        n = len(players)

        cells = ["control", "norm_flanders", "norm_wallonia"]
        random.shuffle(cells)  # randomize which arm absorbs the remainder

        # Repeat cells to cover all players, then shuffle
        assignments = (cells * ((n // 3) + 1))[:n]
        random.shuffle(assignments)

        for pl, cell in zip(players, assignments):
            part = pl.participant

            if cell == "control":
                part.vars["norm_condition"] = "control"
                part.vars["norm_region"] = None
            elif cell == "norm_flanders":
                part.vars["norm_condition"] = "norm"
                part.vars["norm_region"] = "flanders"
            elif cell == "norm_wallonia":
                part.vars["norm_condition"] = "norm"
                part.vars["norm_region"] = "wallonia"

            part.vars.pop("norm_score", None)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Main decision
    donation = models.IntegerField(
        min=0,
        max=C.ENDOWMENT,
        initial=50,
        label="",
    )

    # Time spent on the norm display / decision page (seconds)
    norm_page_time = models.IntegerField(blank=True)

    looked_up_info = models.IntegerField(min=0, max=1, label="")

    # Norm recall check (only filled for treated participants)
    # Bracket codes: lt100 / 100_200 / 200_300 / 300_400 / gt400 / no_figure
    norm_recall_bracket = models.StringField(blank=True, label="")
    recall_correct = models.IntegerField(min=0, max=1, blank=True)

    # Manipulation checks (treated participants only)
    norm_credibility = models.IntegerField(min=0, max=10, blank=True, label="")
    # Directional belief update: 2=much more, 1=somewhat more, 0=as expected,
    # -1=somewhat less, -2=much less; null for control (saw no norm)
    belief_update_direction = models.IntegerField(min=-2, max=2, blank=True, label="")



def assign_treatment(participant):
    """
    Stability guard: assignment is done in creating_session().
    This is called on the Decision page to ensure vars are set
    even if a participant somehow arrives without them (e.g. demo mode).
    Falls back to 3-arm i.i.d. randomization: 33% each.
    """
    if "norm_condition" in participant.vars and "norm_region" in participant.vars:
        return participant.vars["norm_condition"]

    condition, region = random.choice([
        ("control", None),
        ("norm", "flanders"),
        ("norm", "wallonia"),
    ])
    participant.vars["norm_condition"] = condition
    participant.vars["norm_region"] = region
    return condition



def compute_norm_score(participant):
    norm_region = participant.vars.get("norm_region")
    if norm_region is None:
        return None
    return C.NORM_SCORES[norm_region]


def custom_export(players):
    """
    Custom export V1.7: one row per participant (player), analysis-ready for Stata/R.
    - Demographics are stored in participant.vars (from mini_demographics)
    - Treatment stored in participant.vars
    - Outcomes & post-questionnaire stored on Player
    - Demo sessions excluded automatically
    """
    yield [
        # identifiers
        "participant_code",
        "session_code",
        "participant_id_in_session",

        # completion indicators
        "has_finished_task",
        "has_finished_survey",

        # timing
        "start_date",
        "start_time",

        # demographics (from mini_demographics)
        "region",
        "province",
        "gender",
        "age_group",
        "education_level",
        "income_bracket",

        # treatment (structural)
        "norm_condition",
        "norm_region",
        "norm_score",

        # treatment dummies
        "treat_norm",
        "treat_norm_flanders",
        "treat_norm_wallonia",

        # in-group (defined only if norm shown)
        "ingroup_norm",

        # pre-treatment attitudinal battery (from mini_demographics)
        "prior_belief",
        "identity_strength",
        "outgroup_closeness",
        "attention_check_passed",
        "filler_giving_importance",
        "filler_donated_recently",
        "filler_others_give",

        # outcome
        "donation",

        # post-experiment
        "looked_up_info",
        "norm_page_time",
        "norm_recall_bracket",
        "recall_correct",
        "norm_credibility",
        "belief_update_direction",
    ]

    import datetime as dt
    from zoneinfo import ZoneInfo
    _brussels = ZoneInfo("Europe/Brussels")

    for p in players:
        part = p.participant

        # has_finished_task: norm_page_time is only set in before_next_page on Decision,
        # so it's None for dropouts even though donation defaults to 50 (initial=50)
        has_finished_task = int(p.norm_page_time is not None)
        has_finished_survey = int(bool(part.finished))

        # timing (Brussels local time)
        ts = part.vars.get("experiment_start")
        if ts is not None:
            t_local = dt.datetime.fromtimestamp(ts, tz=_brussels)
            start_date = t_local.strftime("%Y-%m-%d")
            start_time = t_local.strftime("%H:%M")
        else:
            start_date = None
            start_time = None

        # demographics
        region = part.vars.get("region")
        province = part.vars.get("province")
        gender = part.vars.get("gender")
        age_group = part.vars.get("age_group")
        education_level = part.vars.get("education_level")
        income_bracket = part.vars.get("income_bracket")
        prior_belief = part.vars.get("prior_belief")
        identity_strength = part.vars.get("identity_strength")
        outgroup_closeness = part.vars.get("outgroup_closeness")
        attention_check_passed = part.vars.get("attention_check_passed")
        filler_giving_importance = part.vars.get("filler_giving_importance")
        filler_donated_recently = part.vars.get("filler_donated_recently")
        filler_others_give = part.vars.get("filler_others_give")

        # treatment
        norm_condition = part.vars.get("norm_condition")
        norm_region = part.vars.get("norm_region")
        norm_score = part.vars.get("norm_score")

        # robust: if norm condition and score missing, compute deterministically
        if norm_condition == "norm" and norm_score is None and norm_region is not None:
            norm_score = C.NORM_SCORES.get(norm_region)

        # dummies
        treat_norm = 1 if norm_condition == "norm" else 0
        treat_norm_flanders = 1 if norm_condition == "norm" and norm_region == "flanders" else 0
        treat_norm_wallonia = 1 if norm_condition == "norm" and norm_region == "wallonia" else 0
        # in-group: 1 if treated and region matches norm region, 0 if treated and out-group,
        # None if control (no norm received)
        ingroup_norm = None
        if norm_condition == "norm" and region is not None and norm_region is not None:
            ingroup_norm = 1 if region == norm_region else 0

        yield [
            # identifiers
            part.code,
            p.session.code,
            part.id_in_session,

            # completion indicators
            has_finished_task,
            has_finished_survey,

            # timing
            start_date,
            start_time,

            # demographics
            region,
            province,
            gender,
            age_group,
            education_level,
            income_bracket,

            # treatment
            norm_condition,
            norm_region,
            norm_score,

            # dummies
            treat_norm,
            treat_norm_flanders,
            treat_norm_wallonia,

            # in-group
            ingroup_norm,

            # pre-treatment attitudinal battery
            prior_belief,
            identity_strength,
            outgroup_closeness,
            attention_check_passed,
            filler_giving_importance,
            filler_donated_recently,
            filler_others_give,

            # outcome
            p.donation,

            # post-experiment
            p.looked_up_info,
            p.norm_page_time,
            p.norm_recall_bracket,
            p.recall_correct,
            p.norm_credibility,
            p.belief_update_direction,
        ]
