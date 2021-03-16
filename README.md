# aridanalysis 

DRY out your regression analysis!

[![build](https://github.com/UBC-MDS/aridanalysis_py/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/aridanalysis_py/actions/workflows/build.yml) [![codecov](https://codecov.io/gh/UBC-MDS/aridanalysis_py/branch/main/graph/badge.svg?token=JGT4Z519QD)](https://codecov.io/gh/UBC-MDS/aridanalysis_py) [![Release](https://github.com/UBC-MDS/aridanalysis_py/actions/workflows/release.yml/badge.svg)](https://github.com/UBC-MDS/aridanalysis_py/actions/workflows/release.yml) [![Documentation Status](https://readthedocs.org/projects/aridanalysis/badge/?version=latest)](https://aridanalysis.readthedocs.io/en/latest/?badge=latest)

## Python Package for Inferential Regression and EDA Analysis!

As Data Scientists, being able to perform Exploratory Data Analysis as well as Regression Analysis are paramount to the process of analyzing trends in data. Moreover, following the DRY (Do Not Repeat Yourself) principle is regarded as a majority priority for maximizing code quality. Yet, often times Data Scientists facing these tasks will start the entire process from scratch, wasting both time and effort while compromising code quality. The aridanalysis package strives to remedy this problem by giving users an easy-to-implement EDA function alongside 3 robust statistical tests that will simplify these analytical processes and produce an easy to read interpretation of the input data. Users will no longer have to write many lines of code to explore their data effectively. 

## Package Functions

### `arid_eda`

This function takes in the data frame of interest and generates summary statistics as well as basic exploratory data analysis plots to helps users understand the overall behaviour of the explanatory and response variables. 

### `arid_linreg`

This function takes in the data frame of interest and performs a regular linear regression with the given regularization and features. The function then outputs an sklearn regression model for prediction and an equivalent statsmodel regression model to provide inference. 

### `arid_logreg`

This function takes in a data frame and performs either binomial or multinomial classification based on user inputs. The function then outputs an sklearn logistic regression model for prediction and an equivalent statsmodel logit regression model to provide inference.  

### `arid_countreg`

This function takes a dataframe, its categorical and continuous variables and other user inputs to perform a Poisson regression. The function will return a sklearn Poisson regressor model for prediction and a wrapper statsmodel for inference purposes.

## Usage

```python
import aridanalysis as aa
from vega_datasets import data
>>> dataframe, plots = aa.arid_eda(house_prices,
                                    'price',
                                    'continuous,
                                    ['rooms', 'age','garage'])
>>> dataframe, plots = aa.arid_eda(iris_data,
                                    'species',
                                    categorical,
                                    ['petalWidth', 'sepalWidth','petalLength'])
tdf = pd.DataFrame(
    {
         "x1": [1, 0, 0],
         "x2": [0, 1.0, 0],
         "x3": [0, 0, 1],
         "x4": ["a", "a", "b"],
         "y": [1, 3, -1.0],
    }
)
>>> aa.arid_linreg(tdf, y) 

df = pd.DataFrame(
    {
        "x1": [1, 0, 0],
        "x2": [0, 1.0, 0],
        "x3": [0, 0, 1],
        "x4": ["a", "a", "b"],
        "y": [1, 0, 0],
    }
)
>>> aa.arid_logreg(df, y)

df = pd.DataFrame(
    {
        "x1": ["bad", "good", "bad"],
        "x2": [34.56, 34. 21, 19.57],
        "y": [6,8,14,],
    }
)
>>> aa.arid_countreg(df, y, con_features=[x2], cat_features=[x1], model="additive", alpha=1)

```

## Python Ecosystem Role

This package will build off the EDA and statistical analysis provided by the [Pandas](https://pypi.org/project/pandas/), [SKLearn](https://scikit-learn.org/stable/) and [Statsmodels](https://www.statsmodels.org/stable/user-guide.html#regression-and-linear-models) Python packages to streamline data visualization and model analysis functionality. There are some existing packages that help you with this, however the `aridanalysis` package aims to ease the job of going through pandas profiling as well as providing different regression analysis interpretations. 

### Related Packages

- [Edapython](https://github.com/UBC-MDS/edapython): This package is similar to Pandas profiling without creating an HTML report as an output. Our package aims to gather the best of Pandas profiling with missing values analysis and most important visualization including a correlation heatmap.
- [regression](https://github.com/makr3la/regression) ([PyPI](https://pypi.org/project/regression/)): This package is a web app for loading tabular data to perform regression analysis. It differs from our package in that it only performs the regression modelling without any analysis or EDA.
- [mlinsights](https://github.com/sdpython/mlinsights/) ([PyPI](https://pypi.org/project/mlinsights/)): This package is an extension to SKLearn and implements a number of specialized models such as quantile regression. Unlike our package, it does not combine any EDA or analysis, and is meant to simply mimic the SKLearn environment while adding additional modelling features.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple aridanalysis
```

## Dependencies

- python = "^3.7"
- pandas = "^1.2.2"
- scikit-learn = "^0.24.1"
- altair = "^4.1.0"
- seaborn = "^0.11.1"
- statsmodels = "^0.12.2"
- vega-datasets = "^0.9.0"
- pytest = "^6.2.2"

## Documentation

The official documentation is hosted on Read the Docs: https://aridanalysis.readthedocs.io/en/latest/

## Contributors

Group 8 Members:  
Craig McLaughlin              : @cmmclaug  
Daniel Ortiz Nunez            : @danielon-5  
Neel Phaterpekar              : @nphaterp  
Santiago Rugeles Schoonewolff : @ansarusc  

We welcome and recognize all contributions. You can see a list of all current contributors in the [contributors tab](https://github.com/ansarusc/aridanalysis/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
