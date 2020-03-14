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

1. Overall CFRs by comorbidity, from table 1 in ["Estimation of risk factors for
COVID-19 mortality - preliminary
results"](https://www.researchgate.net/publication/339505988_Estimation_of_risk_factors_for_COVID-19_mortality_-_preliminary_results),
February 2020, by Caramelo, Ferreira, and Oliveiros.

1. Odds ratios by age group, from table 2, Caramelo, Ferreira, Oliveiros, _op.
cite_.

1. A remark from Michael Olsterholm during his appearance on [episode 1439 of
the Joe Rogan Experience](https://www.youtube.com/watch?v=E3URhJx0NSw), in which
he states that the deaths in Hebei Province in China are dominated by men over
age 65 who smoke.  He goes on to state that most men in that age group smoke,
whereas most women in that age group do not, and the men are dying at five times
the rate of the women.  Olsterholm is an expert in infectious disease and
epidemiology, and is Regents Professor, McKnight Presidential Endowed Chair in
Public Health, the director of the Center for Infectious Disease Research and
Policy (CIDRAP), Distinguished Teaching Professor in the Division of
Environmental Health Sciences, School of Public Health, a professor in the
Technological Leadership Institute, College of Science and Engineering, and an
adjunct professor in the Medical School, all at the University of Minnesota.

## Examples

What is the risk of dying for a 44-year-old woman?

```
./risk.py 44
You have a 1.12% risk of dying if you contract COVID-19.
```

What is the risk of dying for a 74-year-old man who smokes?

```
./risk.py --smoker --male 74
You have a 38.77% risk of dying if you contract COVID-19.
```

What if he also has high blood pressure?

```
./risk.py --hypertensive --smoker --male 74
You have a 42.29% risk of dying if you contract COVID-19.
```

The risks appear to pile up rather alarmingly, especially with age, which is the
greatest single morbidity factor.

## Caveats

* This is a work in progress.  I am not a statistician by trade, nor am I a
medical professional or researcher.  I have a Bachelor's degree in physics from
Carnegie Mellon, I completed my education nearly thirty years ago, and I
have worked as a computer programmer since then.  That is to say, my math is
_rusty_ and, not having ventured deeply into statistics, teasing apart a
multivariate dataset like this is a stretch.  I welcome (gentle) correction.

* Caramelo _et al_ state a number of limitations of their work, as described in
the section "Discussion and conclusion," beginning in the third paragraph.
Users of this tool would do well to read and understand those limitations.  To
wit:  the situation is still evolving; thus, the CFRs are going to change, there
is more than one way to compute CFR, and the authors assumed homogeneous
distribution of gender and comorbidity by age.  If that assumption is wrong,
then this tool will also be wrong, although I hope by only a small amount.

* Caramelo _et al_ do not discuss smoking as a risk factor.  In an attempt to
tease it out independently to match Osterholm's remark about male smokers over
age 65 dying at five times the rate of female nonsmokers of the same age, given
Caramelo's discovered odds ratio of 1.85 for simply being male, I fudged around
a little bit to try to make `risk.py -s -m 65` come out to about 5x `risk.py
65`.  I didn't _completely_ do this _ex recto_:  I took the factor of five,
multiplied it by the overall CFR divided by the CFR for males, and then
multiplied it by the ratio of males to females.  The resultant figure gets
multiplied by the computed risk for females of a given age and is then fed to
the product of probabilities of survival for the given risk factors.
