********************************************************************************
* stata_import.do
* Run this after importing the oTree custom export CSV into Stata.
* Usage:
*   import delimited "task.csv", clear varnames(1) stringcols(_all)
*   do "stata_import.do"
********************************************************************************


* ── 1. Destring numeric variables ────────────────────────────────────────────

destring participant_id_in_session norm_score ///
         treat_norm treat_norm_flanders treat_norm_wallonia ingroup_norm ///
         prior_belief identity_strength outgroup_closeness attention_check_passed ///
         filler_giving_importance filler_donated_recently filler_others_give ///
         donation norm_page_time ///
         looked_up_info recall_correct norm_credibility belief_update_direction, ///
         replace force
* norm_recall_bracket is a string variable — not destringed


* ── 2. Variable labels ────────────────────────────────────────────────────────

label variable participant_code          "Participant identifier (oTree)"
label variable session_code              "Session identifier (oTree)"
label variable participant_id_in_session "Participant ID within session"

label variable region                    "Region of residence"
label variable province                  "Province of residence"
label variable gender                    "Gender"
label variable age_group                 "Age group"
label variable education_level           "Highest education level completed"
label variable income_bracket            "Household net monthly income bracket"

label variable norm_condition            "Treatment condition (control / norm)"
label variable norm_region               "Norm region shown (flanders / wallonia)"
label variable norm_score                "Norm value shown in euros (SPF Finances)"

label variable treat_norm                "Treatment indicator: 1 = received norm, 0 = control"
label variable treat_norm_flanders       "Treatment indicator: 1 = received Flanders norm"
label variable treat_norm_wallonia       "Treatment indicator: 1 = received Wallonia norm"

label variable ingroup_norm              "In-group: 1 = norm region matches participant region (treated only)"

label variable prior_belief              "Prior belief: stated avg annual Belgian charitable donation (euros, pre-treatment)"
label variable identity_strength         "Regional identity strength – ingroup region (0–10, pre-treatment)"
label variable outgroup_closeness        "Closeness to outgroup region(s) (0–10, pre-treatment)"
label variable attention_check_passed    "Attention check passed: 1 = selected correct response"

label variable filler_giving_importance  "How important is charitable giving to you personally? (0–10)"
label variable filler_donated_recently   "Donated to charity in past 12 months: 1 = yes, 0 = no"
label variable filler_others_give        "Belief: proportion of Belgians who give regularly (0–10)"

label variable donation                  "Donation decision (0–100 euros, hypothetical endowment)"
label variable norm_page_time            "Time spent on norm display / decision page (seconds)"

label variable looked_up_info            "1 = looked up external information during experiment"
label variable norm_recall_bracket       "Recalled norm bracket (treated only; lt100/100_200/200_300/300_400/gt400/no_figure)"
label variable recall_correct            "1 = recall bracket spans true norm value €301–€309 (treated only)"
label variable norm_credibility          "Credibility of norm information (0–10, treated only)"
label variable belief_update_direction   "Directional belief update (2=much more … -2=much less; null for control)"


* ── 3. Value labels ───────────────────────────────────────────────────────────
* NOTE: We use explicit gen/replace instead of encode to guarantee that numeric
* codes match the label definitions regardless of alphabetical sort order.

* region (stored as: flanders / wallonia / brussels)
gen region_n = .
replace region_n = 1 if region == "flanders"
replace region_n = 2 if region == "wallonia"
replace region_n = 3 if region == "brussels"
label define lbl_region 1 "Flanders" 2 "Wallonia" 3 "Brussels"
label values region_n lbl_region
label variable region_n "Region of residence (numeric)"

* gender (stored as: male / female / other)
gen gender_n = .
replace gender_n = 1 if gender == "male"
replace gender_n = 2 if gender == "female"
replace gender_n = 3 if gender == "other"
label define lbl_gender 1 "Male" 2 "Female" 3 "Other / prefer not to say"
label values gender_n lbl_gender
label variable gender_n "Gender (numeric)"

* age group (stored as: 18_24 / 25_34 / 35_44 / 45_54 / 55_plus)
gen age_group_n = .
replace age_group_n = 1 if age_group == "18_24"
replace age_group_n = 2 if age_group == "25_34"
replace age_group_n = 3 if age_group == "35_44"
replace age_group_n = 4 if age_group == "45_54"
replace age_group_n = 5 if age_group == "55_plus"
label define lbl_age 1 "18–24" 2 "25–34" 3 "35–44" 4 "45–54" 5 "55+"
label values age_group_n lbl_age
label variable age_group_n "Age group (numeric)"

* education (stored as: secondary_or_less / bachelor / master / phd / other)
gen education_n = .
replace education_n = 1 if education_level == "secondary_or_less"
replace education_n = 2 if education_level == "bachelor"
replace education_n = 3 if education_level == "master"
replace education_n = 4 if education_level == "phd"
replace education_n = 5 if education_level == "other"
label define lbl_edu ///
    1 "Secondary or less" 2 "Bachelor" 3 "Master" 4 "PhD" 5 "Other / prefer not to say"
label values education_n lbl_edu
label variable education_n "Education level (numeric)"

* income bracket (stored as: lt_1500 / 1500_2499 / 2500_3499 / 3500_4999 / gte_5000 / prefer_not)
gen income_n = .
replace income_n = 1 if income_bracket == "lt_1500"
replace income_n = 2 if income_bracket == "1500_2499"
replace income_n = 3 if income_bracket == "2500_3499"
replace income_n = 4 if income_bracket == "3500_4999"
replace income_n = 5 if income_bracket == "gte_5000"
replace income_n = 6 if income_bracket == "prefer_not"
label define lbl_inc ///
    1 "< €1,500" 2 "€1,500–€2,499" 3 "€2,500–€3,499" ///
    4 "€3,500–€4,999" 5 "≥ €5,000" 6 "Prefer not to say"
label values income_n lbl_inc
label variable income_n "Income bracket (numeric)"

* norm region (stored as: flanders / wallonia; missing for control)
gen norm_region_n = .
replace norm_region_n = 1 if norm_region == "flanders"
replace norm_region_n = 2 if norm_region == "wallonia"
label define lbl_norm_region 1 "Flanders" 2 "Wallonia"
label values norm_region_n lbl_norm_region
label variable norm_region_n "Norm region shown (numeric)"

* belief update direction (stored as integer -2 to 2)
label define lbl_belief_update -2 "Much less than expected" -1 "Somewhat less than expected" ///
    0 "About as expected" 1 "Somewhat more than expected" 2 "Much more than expected"
label values belief_update_direction lbl_belief_update

* norm_recall_bracket — create ordered numeric copy for regressions
gen norm_recall_bracket_n = .
replace norm_recall_bracket_n = 1 if norm_recall_bracket == "lt100"
replace norm_recall_bracket_n = 2 if norm_recall_bracket == "100_200"
replace norm_recall_bracket_n = 3 if norm_recall_bracket == "200_300"
replace norm_recall_bracket_n = 4 if norm_recall_bracket == "300_400"
replace norm_recall_bracket_n = 5 if norm_recall_bracket == "gt400"
replace norm_recall_bracket_n = 6 if norm_recall_bracket == "no_figure"
label define lbl_recall_bracket ///
    1 "< €100" 2 "€100–€200" 3 "€200–€300" 4 "€300–€400" 5 "> €400" 6 "Did not see figure"
label values norm_recall_bracket_n lbl_recall_bracket
label variable norm_recall_bracket_n "Recalled norm bracket (numeric)"

* binary variables
label define lbl_yesno 0 "No" 1 "Yes"
label values treat_norm treat_norm_flanders treat_norm_wallonia ///
             ingroup_norm looked_up_info recall_correct attention_check_passed ///
             filler_donated_recently lbl_yesno


* ── 4. Order variables logically ─────────────────────────────────────────────

order participant_code session_code participant_id_in_session ///
      region region_n province ///
      gender gender_n age_group age_group_n education_level education_n ///
      income_bracket income_n ///
      prior_belief identity_strength outgroup_closeness attention_check_passed ///
      filler_giving_importance filler_donated_recently filler_others_give ///
      norm_condition treat_norm treat_norm_flanders treat_norm_wallonia ///
      norm_region norm_region_n norm_score ingroup_norm ///
      donation ///
      looked_up_info norm_page_time ///
      norm_recall_bracket norm_recall_bracket_n recall_correct ///
      norm_credibility belief_update_direction


********************************************************************************
* Variable list (30 exported + 7 numeric copies = 37 working columns)
*
* PRE-TREATMENT
*   region, province, gender, age_group, education_level, income_bracket
*   prior_belief           — stated avg annual Belgian donation (euros)
*   identity_strength      — ingroup identification (0–10)
*   outgroup_closeness     — outgroup closeness (0–10)
*   attention_check_passed — exclusion criterion (0/1)
*   filler_giving_importance — personal importance of charitable giving (0–10)
*   filler_donated_recently  — donated in past 12 months (0/1)
*   filler_others_give       — belief about others giving (0–10)
*
* TREATMENT
*   norm_condition, norm_region, norm_score
*   treat_norm          — main treatment dummy (0/1)
*   treat_norm_flanders — Flanders arm (0/1)
*   treat_norm_wallonia — Wallonia arm (0/1)
*   ingroup_norm        — in-group indicator (0/1, treated only)
*
* OUTCOME
*   donation            — 0–100 euros
*   norm_page_time      — seconds on norm display / decision page
*
* POST-EXPERIMENT
*   looked_up_info         — honesty flag (0/1)
*   norm_recall_bracket    — recalled norm bracket (string code, treated only)
*   norm_recall_bracket_n  — recalled norm bracket (numeric, treated only)
*   recall_correct         — 1 = bracket spans €301–€309 (0/1, treated only)
*   norm_credibility       — credibility of norm info (0–10, treated only)
*   belief_update_direction — directional belief update (-2 to 2, treated only)
********************************************************************************
