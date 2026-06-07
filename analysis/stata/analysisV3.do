/* ============================================================
   MASTER ANALYSIS FILE (V3 — final thesis analysis)
   Belgian Regional Identity & Charitable Giving
   Master's Thesis — Experimental Economics
   ============================================================
   
   Core analysis specification:
   - Models 3 and 4 re-parameterized with direct in-group/out-group
     indicators (ingroup_norm_recipient, outgroup_norm_recipient)
     in place of the Norm × Ingroup interaction.
   - H2 and H4 are now tested by linear (Wald) restrictions on
     coefficient differences rather than single-coefficient tests.
   - Brussels participants are excluded from Models 3 and 4.
   - IV specification removed; attention is now a covariate in
     supplementary checks.
   - norm_page_time exclusion criterion dropped (kept descriptive).
   - Norm intensity (% of income) robustness check added.
   - Brussels-inclusion robustness check added.
   
   Variable reference:
     donation                : outcome, integer 0-100
     treat_norm              : 1 = received any norm (binary)
     treat_norm_flanders     : 1 = received Flanders norm
     treat_norm_wallonia     : 1 = received Wallonia norm
     ingroup_norm            : 1 = norm region matches participant region
                               0 = out-group; null if control or Brussels
     identity_strength       : 0-10, pre-treatment, centered below
     prior_belief            : stated belief about avg Belgian donation (€/yr)
     norm_recall             : recalled norm figure (treated only)
     recall_correct          : 1 if norm_recall within ±5€ of true norm
     norm_credibility        : 0-10 credibility rating (treated only)
     manipulation_surprise   : 0-10, how surprising was the norm
     norm_page_time          : seconds spent on norm display page (descriptive)
     looked_up_info          : 1 = searched external info during experiment
     attention_check_passed  : 1 = passed embedded attention check
     region                  : flanders / wallonia / brussels
     gender, age_group, education_level, income_bracket : demographics
   
   Derived variables (created in Section 0.3):
     ingroup_norm_recipient  : 1 if treated AND ingroup_norm == 1, 0 otherwise
                               null for Brussels in primary spec
     outgroup_norm_recipient : 1 if treated AND ingroup_norm == 0, 0 otherwise
                               null for Brussels in primary spec
     id_centered             : identity_strength centered at sample mean
     ing_x_id, out_x_id      : interactions for Model 4
     delta_belief            : |prior_belief - norm_score|, treated only
     norm_score              : 309 for FL, 301 for WA, . for control
     norm_percent            : 1.24 for FL, 1.37 for WA (% of regional income)
   ============================================================ */


/* ============================================================
   0. SETUP AND DATA PREPARATION
   ============================================================ */

clear all
set more off
capture log close
log using "analysis_log.txt", text replace

* Load anonymized analysis data from the replication package.
use "../../data/thesis_data.dta", clear


/* ---- 0.1 Encode string variables ---- */

encode region,            into(region_n)
encode gender,            into(gender_n)
encode age_group,         into(age_group_n)
encode education_level,   into(educ_n)
encode income_bracket,    into(income_n)
encode norm_condition,    into(norm_condition_n)
encode norm_region,       into(norm_region_n)


/* ---- 0.2 Sample exclusions (pre-registered criteria) ---- */
/* Two exclusion criteria. norm_page_time is descriptive only,
   not an exclusion (no defensible threshold).               */

* Flag exclusions without dropping — allows sensitivity checks
gen excluded = 0
gen exclusion_reason = ""

replace excluded = 1 if attention_check_passed == 0
replace exclusion_reason = "failed_attention" if attention_check_passed == 0

replace excluded = 1 if looked_up_info == 1
replace exclusion_reason = "looked_up_info" if looked_up_info == 1 & excluded == 0

* Report exclusion counts
tab exclusion_reason
di "Total excluded: " _N - sum(excluded==0) " of " _N

* Working sample
preserve
keep if excluded == 0


/* ---- 0.3 Derived and centered variables ---- */

* Center identity_strength at sample mean
sum identity_strength
gen id_centered = identity_strength - r(mean)
label variable id_centered "Identity strength (mean-centered)"

* Distance between prior belief and actual norm
* norm_score: 309 for Flanders, 301 for Wallonia, . for control
gen norm_score = .
replace norm_score = 309 if treat_norm_flanders == 1
replace norm_score = 301 if treat_norm_wallonia == 1
gen delta_belief = abs(prior_belief - norm_score) if treat_norm == 1
label variable delta_belief "Distance: prior belief to norm value (treated only)"

* Norm as percentage of average regional income (for robustness check)
gen norm_percent = .
replace norm_percent = 1.24 if treat_norm_flanders == 1
replace norm_percent = 1.37 if treat_norm_wallonia == 1
label variable norm_percent "Norm as % of regional income (treated only)"

* Direct in-group and out-group indicators (PRIMARY REGRESSION VARIABLES)
* These replace the Norm × Ingroup interaction in V1
* For primary specs (Flanders + Wallonia only):
*   = 1 if treated and norm matches own region (in-group)
*   = 1 if treated and norm does not match own region (out-group)
*   = 0 for control participants (omitted reference category)
*   = . for Brussels (excluded from in-group/out-group specs)

gen ingroup_norm_recipient  = .
gen outgroup_norm_recipient = .

* Flanders and Wallonia: code based on ingroup_norm
replace ingroup_norm_recipient = 1 if treat_norm == 1 & ingroup_norm == 1 ///
    & inlist(region, "flanders", "wallonia")
replace ingroup_norm_recipient = 0 if treat_norm == 1 & ingroup_norm == 0 ///
    & inlist(region, "flanders", "wallonia")
replace ingroup_norm_recipient = 0 if treat_norm == 0 ///
    & inlist(region, "flanders", "wallonia")

replace outgroup_norm_recipient = 1 if treat_norm == 1 & ingroup_norm == 0 ///
    & inlist(region, "flanders", "wallonia")
replace outgroup_norm_recipient = 0 if treat_norm == 1 & ingroup_norm == 1 ///
    & inlist(region, "flanders", "wallonia")
replace outgroup_norm_recipient = 0 if treat_norm == 0 ///
    & inlist(region, "flanders", "wallonia")

label variable ingroup_norm_recipient  "1 = treated, in-group norm"
label variable outgroup_norm_recipient "1 = treated, out-group norm"

* Interactions with centered ID for Model 4
gen ing_x_id = ingroup_norm_recipient  * id_centered
gen out_x_id = outgroup_norm_recipient * id_centered

* Brussels indicator (always out-group when treated, by design)
* Used only in robustness check
gen brussels = (region == "brussels")

* Income bracket midpoints for heterogeneity analysis
gen income_mid = .
replace income_mid = 1000  if income_bracket == "lt_1500"
replace income_mid = 2000  if income_bracket == "1500_2499"
replace income_mid = 3000  if income_bracket == "2500_3499"
replace income_mid = 4250  if income_bracket == "3500_4999"
replace income_mid = 6000  if income_bracket == "gte_5000"


/* ---- 0.4 Global macros for controls and options ---- */

global controls "i.gender_n i.age_group_n i.educ_n i.income_n"
global vce      "vce(robust)"
global ingoutsample "if inlist(region, \"flanders\", \"wallonia\")"


/* ============================================================
   1. DESCRIPTIVE STATISTICS
   ============================================================ */

/* ---- 1.1 Sample composition ---- */

di "=== SAMPLE COMPOSITION ==="
tab region
tab norm_condition
tab region norm_condition, row

/* ---- 1.2 Outcome distribution ---- */

di "=== OUTCOME: DONATION ==="
sum donation, detail
hist donation, bin(20) freq title("Distribution of donation amounts") ///
    xtitle("Donation (€ out of 100)") saving("hist_donation.gph", replace)

* Check for bunching at corners
di "Share donating 0:   " %5.1f 100*mean(donation==0) "%"
di "Share donating 100: " %5.1f 100*mean(donation==100) "%"

* Donation by treatment arm
table norm_condition, statistic(mean donation) statistic(sd donation) ///
    statistic(count donation)

/* ---- 1.3 Key variable summaries ---- */

sum identity_strength prior_belief manipulation_surprise norm_page_time
sum donation if treat_norm == 0
sum donation if ingroup_norm_recipient  == 1
sum donation if outgroup_norm_recipient == 1


/* ============================================================
   2. RANDOMISATION CHECK (Table 1)
   ============================================================ */

di "=== RANDOMISATION CHECK ==="

* Regress treatment on all pre-treatment covariates
* Should find no significant predictors

reg treat_norm i.region_n i.gender_n i.age_group_n i.educ_n ///
    i.income_n identity_strength prior_belief, $vce
estimates store rand_check_pooled
di "F-test joint significance:"
test i.region_n i.gender_n i.age_group_n i.educ_n i.income_n ///
    identity_strength prior_belief

* Repeat for each arm separately
reg treat_norm_flanders i.region_n i.gender_n i.age_group_n i.educ_n ///
    i.income_n identity_strength prior_belief, $vce

reg treat_norm_wallonia i.region_n i.gender_n i.age_group_n i.educ_n ///
    i.income_n identity_strength prior_belief, $vce

* Balance table: means by treatment arm
table norm_condition, statistic(mean identity_strength) ///
    statistic(mean prior_belief) statistic(mean income_mid)


/* ============================================================
   3. MANIPULATION AND TREATMENT CHECKS
   ============================================================ */

di "=== MANIPULATION CHECKS ==="

/* ---- 3.1 Norm recall (attention to stimulus) ---- */

* Recall rate by arm
tab recall_correct if treat_norm == 1
tab recall_correct treat_norm_flanders if treat_norm == 1

* Regression: does recall vary by arm or demographics?
reg recall_correct treat_norm_flanders i.gender_n i.age_group_n ///
    i.educ_n i.income_n if treat_norm == 1, $vce
di "Target recall rate > 70%"
di "Achieved: " %5.1f 100*mean(recall_correct==1 & treat_norm==1) "%"

/* ---- 3.2 Norm credibility ---- */

sum norm_credibility if treat_norm == 1, detail
* Test whether credibility differs by in-group vs out-group (Flanders + Wallonia)
reg norm_credibility ingroup_norm_recipient i.region_n i.gender_n ///
    if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
di "H0: credibility equal across in-group and out-group conditions"

/* ---- 3.3 Norm page exposure time (descriptive) ---- */

sum norm_page_time if treat_norm == 1, detail
di "Note: norm_page_time is descriptive only, not an exclusion criterion."

/* ---- 3.4 Surprise check ---- */

* Higher surprise = more informative norm = larger delta_belief expected
reg manipulation_surprise delta_belief i.region_n ///
    if treat_norm == 1, $vce
di "Expected: surprise increases with distance between prior and norm"

/* ---- 3.5 Belief channel check (informational surprise) ---- */
* Auxiliary specification — keeps pooled Norm indicator because the
* hypothesis here is informational surprise, not identity contrast

reg donation treat_norm delta_belief c.treat_norm#c.delta_belief ///
    $controls, $vce
di "Positive interaction = informational channel active"


/* ============================================================
   4. ATTRITION ANALYSIS
   ============================================================ */

di "=== ATTRITION ANALYSIS ==="

* Need full sample including excluded obs — restore then re-restrict
restore
preserve

* Binary completion indicator (1 = completed full experiment)
gen completed = !missing(donation)

* Test differential attrition by treatment (pooled)
reg completed treat_norm i.region_n i.gender_n i.age_group_n ///
    i.educ_n i.income_n, $vce

* Test differential attrition by arm (Flanders / Wallonia)
reg completed treat_norm_flanders treat_norm_wallonia ///
    i.region_n i.gender_n i.age_group_n i.educ_n i.income_n, $vce

* Test by in-group/out-group recipient status (Flanders + Wallonia only)
reg completed ingroup_norm_recipient outgroup_norm_recipient ///
    i.region_n i.gender_n ///
    if inlist(region, "flanders", "wallonia"), $vce

di "H0: no differential attrition across treatment arms"

restore
* Back to analysis sample (excluded == 0)
keep if excluded == 0


/* ============================================================
   5. PRIMARY OLS MODELS
   ============================================================ */

di "=== PRIMARY OLS MODELS ==="

/* ---- Model 1: Baseline OLS ---- */
* D_i = alpha + beta1*Norm_i + beta2*X_i + eps_i
* Tests: H1 — beta1 > 0 (norm compliance)
* Sample: full analysis sample (Flanders + Wallonia + Brussels)

reg donation treat_norm $controls, $vce
estimates store m1
di "Model 1 — Baseline:"
di "  beta1 (pooled norm effect): " _b[treat_norm]
di "H1: beta1 > 0 (norm compliance)"
test treat_norm


/* ---- Model 2: Disaggregated treatment arms ---- */
* D_i = alpha + beta1*NormFL + beta2*NormWA + beta3*X_i + eps_i
* Tests: beta1 = beta2 (equal norm effects before introducing identity)
* Sample: full analysis sample

reg donation treat_norm_flanders treat_norm_wallonia $controls, $vce
estimates store m2
di "Model 2 — Disaggregated:"
di "  Test of equality: beta1 = beta2"
test treat_norm_flanders = treat_norm_wallonia


/* ---- Model 3: In-group and out-group norm effects (CORE) ---- */
* D_i = alpha + beta1*IngroupNorm + beta2*OutgroupNorm + beta3*X + eps
* Direct-indicator specification with control as omitted category.
* Sample: Flanders + Wallonia only (Brussels excluded — see Section 2.6).
*
* Hypothesis tests:
*   H1: beta1 and beta2 jointly significant (or pooled in Model 1)
*   H2: beta1 - beta2 > 0 (in-group premium, Wald test)
*   H3: beta2 < 0 (out-group resistance, one-sided)

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    $controls if inlist(region, "flanders", "wallonia"), $vce
estimates store m3

di "Model 3 — In-group and out-group:"
di "  beta1 (in-group effect):  " _b[ingroup_norm_recipient]
di "  beta2 (out-group effect): " _b[outgroup_norm_recipient]

di "Test H2 — differential compliance (beta1 - beta2 > 0):"
test ingroup_norm_recipient = outgroup_norm_recipient
lincom ingroup_norm_recipient - outgroup_norm_recipient

di "Test H3 — out-group resistance (beta2 < 0):"
test outgroup_norm_recipient = 0


/* ---- Model 4: Identification strength moderation (CORE) ---- */
* D_i = alpha + beta1*IngroupNorm + beta2*OutgroupNorm + beta3*ID
*       + beta4*(IngroupNorm × ID) + beta5*(OutgroupNorm × ID)
*       + beta6*X + eps
* Sample: Flanders + Wallonia only.
*
* Hypothesis test:
*   H4: beta4 - beta5 > 0 (identification widens in-group/out-group gap)

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    id_centered ing_x_id out_x_id ///
    $controls if inlist(region, "flanders", "wallonia"), $vce
estimates store m4

di "Model 4 — Moderation by identification strength:"
di "  beta1 (in-group at mean ID):  " _b[ingroup_norm_recipient]
di "  beta2 (out-group at mean ID): " _b[outgroup_norm_recipient]
di "  beta3 (ID main effect):       " _b[id_centered]
di "  beta4 (in-group × ID):        " _b[ing_x_id]
di "  beta5 (out-group × ID):       " _b[out_x_id]

di "Test H4 — identity moderation (beta4 - beta5 > 0):"
test ing_x_id = out_x_id
lincom ing_x_id - out_x_id

di "Note: Model 4 is exploratory — interaction tests have substantially"
di "lower power than main effect tests at this sample size."


/* ---- Output table: Models 1-4 ---- */
esttab m1 m2 m3 m4 using "table_ols.rtf", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("OLS Regression Results") ///
    mtitles("Baseline" "Disaggregated" "In/Out-group" "Moderation") ///
    keep(treat_norm treat_norm_flanders treat_norm_wallonia ///
         ingroup_norm_recipient outgroup_norm_recipient ///
         id_centered ing_x_id out_x_id) ///
    addnotes("Robust standard errors in parentheses." ///
             "Models 3 and 4 estimated on Flanders + Wallonia only." ///
             "Controls: gender, age group, education, income bracket.")


/* ============================================================
   6. QUANTILE REGRESSION (Primary alternative estimator)
   ============================================================ */

di "=== QUANTILE REGRESSION ==="
* Sample: Flanders + Wallonia only (matches Models 3 and 4)

/* ---- 6.1 Model 3 at three quantiles ---- */

foreach q in 25 50 75 {
    qreg donation ingroup_norm_recipient outgroup_norm_recipient ///
        $controls if inlist(region, "flanders", "wallonia"), ///
        quantile(`q'/100) vce(robust, reps(200))
    estimates store qr3_q`q'
    di "Quantile `q'%:"
    di "  beta1 (in-group):  " _b[ingroup_norm_recipient]
    di "  beta2 (out-group): " _b[outgroup_norm_recipient]
    test ingroup_norm_recipient = outgroup_norm_recipient
}

/* ---- 6.2 Model 4 at three quantiles ---- */

foreach q in 25 50 75 {
    qreg donation ingroup_norm_recipient outgroup_norm_recipient ///
        id_centered ing_x_id out_x_id ///
        $controls if inlist(region, "flanders", "wallonia"), ///
        quantile(`q'/100) vce(robust, reps(200))
    estimates store qr4_q`q'
    di "Quantile `q'% — beta4 - beta5: "
    lincom ing_x_id - out_x_id
}

/* ---- 6.3 Test equality of coefficients across quantiles ---- */
* Tests whether the in-group / out-group effects are uniform or
* concentrated at specific parts of the distribution

sqreg donation ingroup_norm_recipient outgroup_norm_recipient ///
    $controls if inlist(region, "flanders", "wallonia"), ///
    quantile(.25 .50 .75) reps(200)

di "Test: in-group effect equal at Q25 and Q75"
test [q25]ingroup_norm_recipient = [q75]ingroup_norm_recipient

di "Test: out-group effect equal at Q25 and Q75"
test [q25]outgroup_norm_recipient = [q75]outgroup_norm_recipient

/* ---- 6.4 Output tables: Quantile regression ---- */
esttab qr3_q25 qr3_q50 qr3_q75 using "table_qreg_m3.rtf", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Quantile Regression — Model 3") ///
    mtitles("Q25" "Q50" "Q75") ///
    keep(ingroup_norm_recipient outgroup_norm_recipient) ///
    addnotes("Bootstrap standard errors (200 reps)." ///
             "Sample: Flanders + Wallonia." ///
             "Controls: gender, age group, education, income bracket.")

esttab qr4_q25 qr4_q50 qr4_q75 using "table_qreg_m4.rtf", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Quantile Regression — Model 4") ///
    mtitles("Q25" "Q50" "Q75") ///
    keep(ingroup_norm_recipient outgroup_norm_recipient ///
         id_centered ing_x_id out_x_id) ///
    addnotes("Bootstrap standard errors (200 reps)." ///
             "Sample: Flanders + Wallonia." ///
             "Controls: gender, age group, education, income bracket.")


/* ============================================================
   7. FALSIFICATION TESTS
   ============================================================ */

di "=== FALSIFICATION TESTS ==="

/* ---- 7.1 Placebo norm source test ---- */
* Control group only (Flanders + Wallonia)
* Assign pseudo in-group based on random fictitious norm region
* If significant effect appears, pre-existing group differences
* are contaminating the in-group/out-group classification.

set seed 12345
gen pseudo_norm_region = "flanders" if runiform() > 0.5 & treat_norm == 0
replace pseudo_norm_region = "wallonia" ///
    if pseudo_norm_region == "" & treat_norm == 0
gen pseudo_ingroup = (pseudo_norm_region == region) ///
    if treat_norm == 0 & inlist(region, "flanders", "wallonia")

reg donation pseudo_ingroup $controls ///
    if treat_norm == 0 & inlist(region, "flanders", "wallonia"), $vce
estimates store placebo

di "Placebo test — pseudo_ingroup coefficient should be ~0:"
test pseudo_ingroup


/* ---- 7.2 Prior belief as outcome (should not be treatment-predicted) ---- */
* Prior belief is collected before treatment.
* Treatment should not predict prior belief.
* Significant result = randomisation or ordering problem.

reg prior_belief treat_norm_flanders treat_norm_wallonia ///
    $controls, $vce
di "H0: treatment does not predict prior belief (collected pre-treatment)"
test treat_norm_flanders treat_norm_wallonia


/* ============================================================
   8. ROBUSTNESS CHECKS
   ============================================================ */

di "=== ROBUSTNESS CHECKS ==="

/* ---- 8.1 Norm magnitude control (€ value) ---- */
* norm_score is 309 for FL, 301 for WA — small absolute difference.
* Add norm_score as covariate among treated to partial out any
* magnitude confound.

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    norm_score $controls ///
    if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
estimates store m3_normscore
di "Norm magnitude: norm_score coefficient should be small and non-significant"


/* ---- 8.2 Norm intensity control (% of income) ---- */
* The Walloon norm appears as 1.37% of regional income while the
* Flemish norm appears as 1.24%. Add norm_percent as covariate to
* check whether estimates are stable.

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    norm_percent $controls ///
    if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
estimates store m3_normpercent
di "Norm intensity: in-group/out-group estimates should be stable"
di "after controlling for the displayed percentage value."


/* ---- 8.3 Brussels-inclusion check ---- */
* Primary specifications exclude Brussels participants.
* This check re-estimates Models 3 and 4 with Brussels participants
* coded as out-group recipients (since by design no Brussels norm
* is presented). If estimates are stable, the exclusion choice does
* not materially affect the conclusions.

* Construct Brussels-inclusive variants of the indicators
gen ingroup_brussels  = ingroup_norm_recipient
gen outgroup_brussels = outgroup_norm_recipient
* Brussels treated participants: by design always out-group
replace outgroup_brussels = 1 if treat_norm == 1 & region == "brussels"
replace ingroup_brussels  = 0 if treat_norm == 1 & region == "brussels"
* Brussels controls: zero on both
replace ingroup_brussels  = 0 if treat_norm == 0 & region == "brussels"
replace outgroup_brussels = 0 if treat_norm == 0 & region == "brussels"

* Brussels-inclusive interactions for Model 4
gen ing_x_id_br = ingroup_brussels  * id_centered
gen out_x_id_br = outgroup_brussels * id_centered

reg donation ingroup_brussels outgroup_brussels $controls, $vce
estimates store m3_brussels
di "Brussels included as out-group:"
di "  beta1 (in-group):  " _b[ingroup_brussels]
di "  beta2 (out-group): " _b[outgroup_brussels]

reg donation ingroup_brussels outgroup_brussels id_centered ///
    ing_x_id_br out_x_id_br $controls, $vce
estimates store m4_brussels


/* ---- 8.4 Attention as covariate (instead of exclusion) ---- */
* Supplementary: re-estimate Models 3 and 4 with recall_correct as
* an additional covariate. Cautionary note: recall is post-treatment,
* so this introduces post-treatment bias and is reported as a
* supplementary diagnostic only (Montgomery, Nyhan and Torres, 2018).

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    recall_correct $controls ///
    if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
estimates store m3_attention

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    id_centered ing_x_id out_x_id recall_correct $controls ///
    if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
estimates store m4_attention

di "Attention covariate: post-treatment, supplementary diagnostic only"


/* ---- 8.5 Lee bounds for differential attrition ---- */
* Reports treatment effect bounds under worst-case attrition selection.
* Implemented via leebounds (ssc install leebounds).
* Run only if attrition is statistically significant in Section 4.

* Uncomment if needed:
* leebounds donation treat_norm if inlist(region, "flanders", "wallonia"), ///
*     cieffect


/* ============================================================
   9. HETEROGENEITY ANALYSES (Secondary)
   ============================================================ */

di "=== HETEROGENEITY ANALYSES ==="

/* ---- 9.1 By credibility of norm ---- */
* Among treated participants, does credibility moderate response?
* Credibility is post-treatment — descriptive only.

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    c.norm_credibility ///
    c.ingroup_norm_recipient#c.norm_credibility ///
    c.outgroup_norm_recipient#c.norm_credibility ///
    $controls if treat_norm == 1 & inlist(region, "flanders", "wallonia"), $vce
di "Does norm credibility moderate treatment response?"


/* ---- 9.2 By income bracket ---- */

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    c.income_mid ///
    c.ingroup_norm_recipient#c.income_mid ///
    c.outgroup_norm_recipient#c.income_mid ///
    $controls if inlist(region, "flanders", "wallonia"), $vce


/* ---- 9.3 By region ---- */
* Separate estimates for Flemish and Walloon participants.
* Consistency check — effects should be directionally similar.

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    $controls if region == "flanders", $vce
estimates store m3_FL

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    $controls if region == "wallonia", $vce
estimates store m3_WA

esttab m3_FL m3_WA, b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Flanders" "Wallonia") ///
    keep(ingroup_norm_recipient outgroup_norm_recipient)


/* ============================================================
   10. SENSITIVITY ANALYSES
   ============================================================ */

di "=== SENSITIVITY ANALYSES ==="

/* ---- 10.1 Main results without demographic controls ---- */

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    if inlist(region, "flanders", "wallonia"), $vce
estimates store m3_nocontrols

reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    id_centered ing_x_id out_x_id ///
    if inlist(region, "flanders", "wallonia"), $vce
estimates store m4_nocontrols


/* ---- 10.2 Sample including excluded participants ---- */
* Check sensitivity of main estimates to exclusion criteria.

restore
preserve
reg donation ingroup_norm_recipient outgroup_norm_recipient ///
    $controls if inlist(region, "flanders", "wallonia"), $vce
estimates store m3_fullsample
restore
keep if excluded == 0


/* ============================================================
   11. SUMMARY OUTPUT
   ============================================================ */

di "=== FINAL SUMMARY TABLE ==="

esttab m1 m2 m3 m4 using "table_main.rtf", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Main Results: Effect of Regional Norm on Charitable Giving") ///
    mtitles("(1) Baseline" "(2) Disaggregated" ///
            "(3) In/Out-group" "(4) Moderation") ///
    keep(treat_norm treat_norm_flanders treat_norm_wallonia ///
         ingroup_norm_recipient outgroup_norm_recipient ///
         id_centered ing_x_id out_x_id) ///
    stats(N r2, labels("Observations" "R-squared")) ///
    addnotes("Robust standard errors in parentheses." ///
             "* p<0.10, ** p<0.05, *** p<0.01." ///
             "Models 3 and 4 estimated on Flanders + Wallonia only." ///
             "Controls: gender, age group, education, income bracket." ///
             "identity_strength centered at sample mean.")

esttab m3 m3_brussels m3_normscore m3_normpercent m3_attention ///
    using "table_robustness_m3.rtf", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Robustness Checks for Model 3") ///
    mtitles("Main" "+Brussels" "+NormScore" "+NormPercent" "+Recall") ///
    keep(ingroup_norm_recipient outgroup_norm_recipient ///
         ingroup_brussels outgroup_brussels) ///
    addnotes("Robust standard errors in parentheses." ///
             "Recall column is supplementary (post-treatment).")

log close
