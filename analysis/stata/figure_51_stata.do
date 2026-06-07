**# ============================================================
**# Figure 5.1 — Donation distribution by treatment arm
**# Generates the real density plot from the analysis sample.
**# Insert this block after Section 1.2 in the main do-file,
**# or run it standalone after loading thesis_data.dta.
**# ============================================================

* Set graph scheme for clean black-and-white output suitable for LaTeX.
set scheme s1mono

* Load anonymized analysis data when the script is run standalone.
capture confirm variable donation
if _rc {
    use "../../data/thesis_data.dta", clear
}

* Build a single categorical variable for the legend.
gen byte arm = .
replace arm = 1 if analysis_sample == 1 & treat_norm == 0
replace arm = 2 if analysis_sample == 1 & ingroup_norm_recipient == 1
replace arm = 3 if analysis_sample == 1 & outgroup_norm_recipient == 1

label define arm_lbl 1 "Control" 2 "In-group norm" 3 "Out-group norm"
label values arm arm_lbl
label variable arm "Treatment arm"

* Three overlaid kernel densities. bwidth chosen to smooth without erasing
* the bunching at 0 and 100. Replicate the figure with different bandwidths
* if needed.
twoway ///
    (kdensity donation if arm == 1, bwidth(8) lcolor(black) lwidth(medthick) lpattern(solid)) ///
    (kdensity donation if arm == 2, bwidth(8) lcolor(black) lwidth(medthick) lpattern(dash)) ///
    (kdensity donation if arm == 3, bwidth(8) lcolor(black) lwidth(medthick) lpattern(shortdash)) ///
    , ///
    xtitle("Donation amount (EUR out of 100)") ///
    ytitle("Density") ///
    xlabel(0(20)100) ///
    legend(order(1 "Control (N=115)" 2 "In-group norm (N=102)" 3 "Out-group norm (N=84)") ///
           ring(0) position(2) cols(1) region(lstyle(none))) ///
    graphregion(color(white)) plotregion(color(white)) ///
    name(donation_dist, replace)

* Export to PDF (LaTeX-ready). If you prefer EPS or PNG, change accordingly.
graph export "../../outputs/donation_distribution.pdf", replace as(pdf)

* Cleanup
drop arm
label drop arm_lbl
