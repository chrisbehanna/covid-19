#!/usr/bin/env python3

import argparse
import math

args = None


def compute_risk():
    #
    # Baseline risk is for a female aged 10-19 with no comorbidies:  0.2% CFR
    #
    # Source:  Business Insider graph presenting flu vs. COVID-19 CFRs by age.
    # Other discussion I ran across suggested this was data from Hebei, before
    # the outbreak became a pandemic.
    #
    baseline_risk = 0.002

    #
    # Age-related odds ratios.  We use these to compute the baseline CFR for a
    # female of a given age with no comorbidities.
    #
    # Data is from table 2 in
    # "Estimation of risk factors for COVID-19 mortality - preliminary results"
    # by Caramelo, Ferreira, and Oliveiros, Feb. 2020, availalbe here:
    # https://www.researchgate.net/publication/339505988_Estimation_of_risk_factors_for_COVID-19_mortality_-_preliminary_results
    #
    age = {
        10: 1.00,
        20: 0.2017,
        30: 0.3271,
        40: 5.6030,
        50: 6.7626,
        60: 18.8161,
        70: 43.7291,
        80: 86.8680
    }

    #
    # Age distribution from Hebei province.  We don't actually use it, but note
    # it here because it's interesting.  Source:
    # https://www.statista.com/statistics/1095024/china-age-distribution-of-wuhan-coronavirus-covid-19-patients/
    #
    age_n = {
        10: 0.012,
        20: 0.081,
        30: 0.17,
        40: 0.192,
        50: 0.224,
        60: 0.192,
        70: 0.088,
        80: 0.032
    }

    #
    # Odds ratios and weights.  Unused for now.  It's simpler to do a
    # probability combination than to try to combine odds ratios, which I do not
    # completely understand how to do.  It's supposedly the exponentiation of
    # the weighted average of the logs of the odds ratios, but when I do that, I
    # clearly do it wrong because I end up with nonsense, such as my risk of
    # dying being lower than that of a female of the same age.
    #
    male_or = 1.8518
    male_n = 0.5143

    hypertension = 7.4191
    hypertension_n = 0.1274

    diabetes = 9.0329
    diabetes_n = 0.0462

    cardiac_disease = 12.8328
    cardiac_n = 0.0347

    chronic_respiratory_disease = 7.7925
    respiratory_n = 0.0195

    cancer = 6.8845
    cancer_n = 0.0039

    #
    # Overall CFRs (Case Fatality Rates).  We use these to compute the combined
    # probabilities for people having more than one risk factor.  The assumption
    # here is that the probabilities are independent for each risk factor, thus
    # we can simply multiply the probability of survival with each condition
    # together independently to come up with the predicted CFR given multiple
    # risk factors.
    #
    # Data is from table 1 in
    # "Estimation of risk factors for COVID-19 mortality - preliminary results"
    # by Caramelo, Ferreira, and Oliveiros, Feb. 2020, available here:
    # https://www.researchgate.net/publication/339505988_Estimation_of_risk_factors_for_COVID-19_mortality_-_preliminary_results
    #
    male = 0.0275
    hypertensive = 0.0574
    diabetic = 0.0678
    cardiac = 0.0897
    respiratory = 0.0597
    cancer = 0.0537

    #
    # From Michael Olsterholm's comments on Joe Rogan #1439, male smokers
    # over age 65 died at 5x the rate of female non-smokers of the same age.
    # Given the OR for males, we deduce the risk factor for smoking on its own,
    # maybe.  This is admittedly fudged a bit to make the math work out for the
    # 60-69 decile:  we take the factor of five, multiply it by the overall CFR
    # divided by the CFR for males, and then multiply it by the ratio of males
    # to females.
    #
    smoker = 5.00 * 0.022 / 0.0275 * 0.5143 / (1-0.5143)

    #
    # Compute the risk.  We multiply the probabilities of survival for each
    # of the risk factors (1 - CFR for each risk factor) and then return 1 minus
    # the result as the predicted risk of dying.
    #

    age_group = round(args.age, -1)
    
    if age_group > 80:
        age_group = 80

    age_group_baseline_risk = baseline_risk * age[age_group]

    if args.smoker:
        age_group_baseline_risk *= smoker

    age_group_survival = 1.00 - age_group_baseline_risk

    survival = age_group_survival

    if args.male:
        survival *= (1.00 - male)

    if args.hypertensive:
        survival *= (1.00 - hypertensive)

    if args.diabetic:
        survival *= (1.00 - diabetic)

    if args.cardiac:
        survival *= (1.00 - cardiac)

    if args.respiratory:
        survival *= (1.00 - respiratory)

    if args.cancer:
        survival *= (1.00 - cancer)

    return (1.00 - survival)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--smoker',
        dest="smoker",
        action="store_true",
        default=False,
        help="stir in the risk for a smoker"
    )

    parser.add_argument(
        '-m', '--male',
        dest="male",
        action="store_true",
        default=False,
        help="stir in the risk for a male (default is female)"
    )

    parser.add_argument(
        '-H','--hypertensive',
        dest='hypertensive',
        action="store_true",
        default=False,
        help="stir in the risk for having hypertension"
    )

    parser.add_argument(
        '-d', '--diabetic',
        dest='diabetic',
        action="store_true",
        default=False,
        help="stir in the risk for diabetes"
    )

    parser.add_argument(
        '-c', '--cardiac-disease',
        dest='cardiac',
        action="store_true",
        default=False,
        help="stir in the risk for cardiac disease"
    )

    parser.add_argument(
        '-r', '--chronic-respiratory-disease',
        dest='respiratory',
        action="store_true",
        default=False,
        help="stir in the risk for chronic respiratory problems"
    )

    parser.add_argument(
        '-C', '--cancer',
        dest='cancer',
        action="store_true",
        default=False,
        help="stir in the risk for having cancer of any kind"
    )

    parser.add_argument(
        "age",
        metavar="AGE",
        type=int,
    )

    args = parser.parse_args()

    risk = compute_risk()

    print(
        "You have a {:.4%} risk of dying if you contract COVID-19.".format(risk)
    )
