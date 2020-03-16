# COVID-19 Fatality Risk Calculator

This is a naïve attempt to piece together various risk factors and compute the
risk of death for a given individual from COVID-19 given what is known at the
time of this writing.

## Usage

```
usage: risk.py [-h] [-s] [-m] [-H] [-d] [-c] [-r] [-C] AGE

positional arguments:
  AGE

optional arguments:
  -h, --help            show this help message and exit
  -s, --smoker          stir in the risk for a smoker
  -m, --male            stir in the risk for a male (default is female)
  -H, --hypertensive    stir in the risk for having hypertension
  -d, --diabetic        stir in the risk for diabetes
  -c, --cardiac-disease
                        stir in the risk for cardiac disease
  -r, --chronic-respiratory-disease
                        stir in the risk for chronic respiratory problems
  -C, --cancer          stir in the risk for having cancer of any kind
```

## Sources

The tool is a python3 script containing data from a couple of sources:

1. Overall CFR (Case Fatality Rates) by age from Hebei (Wuhan) for the flu vs.
COVID-19, as published in _[Business
Insider](https://www.businessinsider.com/coronavirus-compared-to-flu-mortality-rates-2020-3)_.
The fatality rate there is higher than it is in South Korea; however, the
number of cases is also far larger, perhaps giving greater statistical
significance?  The model in the paper cited below also operates on this data, so
it makes sense to use it.  I used the chart in this source for the baseline CFR
for age 10-19.

2. Overall CFRs by comorbidity, from table 1 in ["Estimation of risk factors for
COVID-19 mortality - preliminary
results"](https://www.researchgate.net/publication/339505988_Estimation_of_risk_factors_for_COVID-19_mortality_-_preliminary_results),
February 2020, by Caramelo, Ferreira, and Oliveiros.

3. Odds ratios by age group, from table 2, Caramelo, Ferreira, Oliveiros, _op.
cite_.

4. <strike>A remark from Michael Olsterholm during his appearance on [episode
1439 of the Joe Rogan Experience](https://www.youtube.com/watch?v=E3URhJx0NSw),
in which he states that the deaths in Hebei Province in China are dominated by
men over age 65 who smoke.  He goes on to state that most men in that age group
smoke, whereas most women in that age group do not, and the men are dying at
five times the rate of the women.  Olsterholm is an expert in infectious disease
and epidemiology, and is Regents Professor, McKnight Presidential Endowed Chair
in Public Health, the director of the Center for Infectious Disease Research and
Policy (CIDRAP), Distinguished Teaching Professor in the Division of
Environmental Health Sciences, School of Public Health, a professor in the
Technological Leadership Institute, College of Science and Engineering, and an
adjunct professor in the Medical School, all at the University of Minnesota.
</strike>

5. Update to risk factor from being a current smoker:  "Clinical course and risk
factors for mortality of adult inpatients with COVID-19 in Wuhan, China: a
retrospective cohort study", Zhou, Yu, Dou, Fan, Liu _et al_, published in [The
Lancet](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30566-3/fulltext),
2020 March 11.  They show an odds ratio of death for being a current smoker vs.
being a non-smoker of 2.23 in Table 3.

## Examples

What is the risk of dying for a 44-year-old woman?

```
./risk.py 44
You have a 1.12% risk of dying if you contract COVID-19.
```

What is the risk of dying for a 74-year-old man who smokes?

```
./risk.py --smoker --male 74
You have a 21.72% risk of dying if you contract COVID-19.
```

What if he also has high blood pressure?

```
./risk.py --hypertensive --smoker --male 74
You have a 26.21% risk of dying if you contract COVID-19.
```

The risks appear to pile up rather alarmingly, especially with age, which is the
greatest single morbidity factor.

## Caveats

* This is a work in progress.  I am not a statistician by trade, nor am I a
medical professional or researcher.  I have a Bachelor's degree in physics from
Carnegie Mellon, I completed my education awhile ago, and I have worked as a
computer programmer since then.  That is to say, my math is _rusty_ and, not
having ventured deeply into statistics, teasing apart a multivariate dataset
like this is a stretch.  I welcome (gentle) correction.

* Per the above, I have assumed that all of the comorbidities listed in Caramelo
 _et al_ are independent; thus, I can simply take the product of the individual
 chance of survival for each risk factor in order to deduce the overall risk of
 death when more than one risk factor is present.

* Caramelo _et al_ state a number of limitations of their work, as described in
the section "Discussion and conclusion," beginning in the third paragraph.
Users of this tool would do well to read and understand those limitations.  To
wit:  the situation is still evolving; thus, the CFRs are going to change, there
is more than one way to compute CFR, and the authors assumed homogeneous
distribution of gender and comorbidity by age.  If that assumption is wrong,
then this tool will also be wrong, although I hope by only a small amount.

* Caramelo _et al_ do not discuss smoking as a risk factor.  What I've done is
to take the odds ratio from Zhou _et al_ in _The Lancet_ (cited _supra_ under
sources) and multiply it by the computed baseline risk for the specified age
group, and then combine probabilities as described in the second bullet,
_supra_.
