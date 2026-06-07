from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "mini_demographics"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    region = models.StringField(
        choices=[
            ["flanders", "flanders"],
            ["wallonia", "wallonia"],
            ["brussels", "brussels"],
        ],
        label="",
    )

    # Province (full list, filtered in pages.py)
    province = models.StringField(
        choices=[
            ["antwerp", "antwerp"],
            ["flemish_brabant", "flemish_brabant"],
            ["east_flanders", "east_flanders"],
            ["west_flanders", "west_flanders"],
            ["limburg", "limburg"],
            ["hainaut", "hainaut"],
            ["walloon_brabant", "walloon_brabant"],
            ["namur", "namur"],
            ["liege", "liege"],
            ["luxembourg", "luxembourg"],
            ["brussels_capital", "brussels_capital"],
        ],
        label="",
    )

    gender = models.StringField(
        choices=[["male", "male"], ["female", "female"], ["other", "other"]],
        label="",
    )

    age_group = models.StringField(
        choices=[
            ["18_24", "18_24"],
            ["25_34", "25_34"],
            ["35_44", "35_44"],
            ["45_54", "45_54"],
            ["55_plus", "55_plus"],
        ],
        label="",
    )

    education_level = models.StringField(
        choices=[
            ["secondary_or_less", "secondary_or_less"],
            ["bachelor", "bachelor"],
            ["master", "master"],
            ["phd", "phd"],
            ["other", "other"],
        ],
        label="",
    )

    income_bracket = models.StringField(
        choices=[
            ["lt_1500", "lt_1500"],
            ["1500_2499", "1500_2499"],
            ["2500_3499", "2500_3499"],
            ["3500_4999", "3500_4999"],
            ["gte_5000", "gte_5000"],
            ["prefer_not", "prefer_not"],
        ],
        label="",
    )

    # Prior belief: collected pre-treatment, annual € frame matching norm stimulus
    prior_belief = models.IntegerField(min=0, label="")

    # Identity — pre-treatment, embedded in attitudinal battery
    identity_strength = models.IntegerField(min=0, max=10, label="")
    outgroup_closeness = models.IntegerField(min=0, max=10, label="")

    # Attention check — correct answer is "agree"
    attention_check = models.StringField(
        choices=[
            ["strongly_disagree", "Strongly disagree"],
            ["disagree", "Disagree"],
            ["neutral", "Neutral"],
            ["agree", "Agree"],
            ["strongly_agree", "Strongly agree"],
        ],
        label="",
    )
    attention_check_passed = models.IntegerField(blank=True)

    # Attitudinal filler items — buffer between belief elicitation and treatment
    filler_giving_importance = models.IntegerField(min=0, max=10, label="")
    filler_donated_recently = models.IntegerField(min=0, max=1, label="")
    filler_others_give = models.IntegerField(min=0, max=10, label="")
