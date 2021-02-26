# aridanalysis 

![](https://github.com/ansarusc/aridanalysis/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ansarusc/aridanalysis/branch/main/graph/badge.svg)](https://codecov.io/gh/ansarusc/aridanalysis) ![Release](https://github.com/ansarusc/aridanalysis/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/aridanalysis/badge/?version=latest)](https://aridanalysis.readthedocs.io/en/latest/?badge=latest)

## Python Package for Inferential Regression and EDA Analysis!

For the function creation part of the project,  we based our selection criteria on the DRY principle. From experience we have gathered throughout the program, both the Exploratory Data Analysis and the Inferential Regression Statistical Analysis are two widespread procedures a Data Scientist faces daily. Yet, every time we face these tasks, we start the process from scratch, wasting both time and effort. With this into consideration,  this project's goal is to create a package with four reproducible and shareable functions that perform these routine tasks.

### First Function: EDA

The first function will deal with the basic EDA, similar to the output provided by Pandas profiling (although faster and much smaller), to understand the overall behaviour of the data over the response and its individual distributions. The inputs for this initial function are a data frame, the response column and a list of the explanatory variables presented in the representative data structure. In addition, the output of this function will provide a correlation matrix, scatterplots between the different features and the response, a distributional study of each component, either with histograms or density plots, and a visual representation of missing data.

### Second Function: Linear Regression

Furthermore, the second function will create a conditional linear regression model for the unrestricted responses. As inputs, this function will require a data frame with the data to analyze, the explanatory columns, both continuous and categorical (as different inputs) and whether interactive and polynomial models are required. The body and outputs will provide a multicollinearity analysis, the statistically significant variables with their respective interpretation over the response, and if the error or bias term's distributional assumptions were met.




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
