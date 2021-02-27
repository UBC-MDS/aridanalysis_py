# aridanalysis 

![](https://github.com/ansarusc/aridanalysis/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ansarusc/aridanalysis/branch/main/graph/badge.svg)](https://codecov.io/gh/ansarusc/aridanalysis) ![Release](https://github.com/ansarusc/aridanalysis/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/aridanalysis/badge/?version=latest)](https://aridanalysis.readthedocs.io/en/latest/?badge=latest)

## Python Package for Inferential Regression and EDA Analysis!

For the function creation part of the project,  we based our selection criteria on the DRY principle. From experience we have gathered throughout the program, both the Exploratory Data Analysis and the Inferential Regression Statistical Analysis are two widespread procedures a Data Scientist faces daily. Yet, every time we face these tasks, we start the process from scratch, wasting both time and effort. With this into consideration,  this project's goal is to create a package with four reproducible and shareable functions that perform these routine tasks.

### First Function: EDA

The first function will deal with the basic EDA, similar to the output provided by Pandas profiling (although faster and much smaller), to understand the overall behaviour of the data over the response and its individual distributions. The inputs for this initial function are a data frame, the response column and a list of the explanatory variables presented in the representative data structure. In addition, the output of this function will provide a correlation matrix, scatterplots between the different features and the response, a distributional study of each component, either with histograms or density plots, and a visual representation of missing data.

### Second Function: Linear Regression

Furthermore, the second function will create a conditional linear regression model for the unrestricted responses. As inputs, this function will require a data frame with the data to analyze, the explanatory columns, both continuous and categorical (as different inputs) and whether interactive and polynomial models are required. The body and outputs will provide a multicollinearity analysis, the statistically significant variables with their respective interpretation over the response, and if the error or bias term's distributional assumptions were met.

 ### Third Function: Logistic Regression

Moreover, the third function will create a generalized linear model of logistic regression for categorical dependent variables. The proposed inputs are a data frame of the data, the response column, two lists of the explanatory continuous and categorical variables, the flavour of logistic regression to be performed dependent on the data (binomial, ordinal or multinomial) and whether to consider interactive and polynomial models. As a response, the function will return the statistically significant features and their respective interpretation of probability odds.

### Fourth Function: Regression for Counting Data

Finally, the fourth and final function will perform an Inferential Regression Analysis on counting data. Like the previous functions, the required inputs for this correction function are a data frame, the response column, two lists or character vectors of the continuous and categorical explanatory variables, whether the model should be additive of interactive, and the polynomial degree of the linear combination conditioned on the response. For this instance, the family for creating the link function in the generalized linear model will not be chosen by the user and selected by the algorithm using overdispersion criteria. It is expected that the function returns both a list of the statistically significant features, their respective interpretations and the distribution family utilized for establishing the regression model.

## Python Ecosystem Role

This package will build off the EDA and statistical analysis provided by the [Pandas](https://pypi.org/project/pandas/) and [SKLearn](https://scikit-learn.org/stable/) Python packages to streamline data visualization and model analysis functionality. There are some existing packages that help you with this, however the `aridanalysis` package aims to ease the job of going through pandas profiling as well as providing different regression analysis interpretations. 

### Related Packages

- [Edapython](https://github.com/UBC-MDS/edapython): This package is similar to Pandas profiling without creating an HTML report as an output. Our package aims to gather the best of Pandas profiling with missing values analysis and most important visualization including a correlation heatmap.
- [regression](https://github.com/makr3la/regression) ([PyPI](https://pypi.org/project/regression/)): This package is a web app for loading tabular data to perform regression analysis. It differs from our package in that it only performs the regression modelling without any analysis or EDA.
- [mlinsights](https://github.com/sdpython/mlinsights/) ([PyPI](https://pypi.org/project/mlinsights/)): This package is an extension to SKLearn and implements a number of specialized models such as quantile regression. Unlike our package, it does not combine any EDA or analysis, and is meant to simply mimic the SKLearn environment while adding additional modelling features.

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
