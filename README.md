# aridanalysis 

![](https://github.com/ansarusc/aridanalysis/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ansarusc/aridanalysis/branch/main/graph/badge.svg)](https://codecov.io/gh/ansarusc/aridanalysis) ![Release](https://github.com/ansarusc/aridanalysis/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/aridanalysis/badge/?version=latest)](https://aridanalysis.readthedocs.io/en/latest/?badge=latest)

## Python Package for Inferential Regression and EDA Analysis!

As Data Scientists, being able to perform Exploratory Data Analysis as well as Regression Analysis are paramount to the process of analyzing trends in data. Moreover, following the DRY (Do Not Repeat Yourself) priciple is regarded as a majory priority for maximizing code quality. Yet, often times Data Scientists facing these tasks will start the entire process from scratch, wasting both time and effort while compromising code quality. The aridanalysis package strives to remedy this problem by giving users an easy-to-implement EDA function alongside 3 robust statistical tests that will simplify these analytical processes and produce an easy to read interpretation of the input data. Users will no longer have to write many lines of code to explore their data effectively. 

## Package Functions

### arid_eda 

This function takes in the data frame of interest and generates summary statistics as well as basic exploratory data analysis plots to helps users understand the overall behaviour of the explanatory and response variables. 

### arid_linreg

This function takes in the data frame of interest and performs a regular linear regression. The function then outputs an interpretation of statistically significant variables alongside additional information pertaining to distributional assumptions. 

### arid_logreg

This function takes in a data frame and performs different flavours of logistic regression based on user inputs. The function then outputs an interpretation (probability odds) of statistically significant variables alongside additional information pertaining to distributional assumptions. 

### arid_poisson (Probably not a good name but dry fish sounds funny)

This function takes a data frame and performs an Inferential Regression Analysis with count data; the flavour of this analysis will depend on several user inputs. The function will then reutn a list of statistically significant features alongside their interpretations as well as the distribution family. 

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ aridanalysis
```

## Features

- TODO

## Dependencies

- TODO

## Usage

- TODO

## Documentation

The official documentation is hosted on Read the Docs: https://aridanalysis.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/ansarusc/aridanalysis/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
