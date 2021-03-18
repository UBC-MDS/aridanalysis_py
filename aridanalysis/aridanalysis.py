import pandas as pd
import pandas.api.types as ptypes
import numpy as np
import altair as alt
from sklearn.linear_model import (
    LinearRegression,
    Lasso,
    Ridge,
    ElasticNet,
    LogisticRegression,
)
import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.linear_model import PoissonRegressor
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline

import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../aridanalysis')
import error_strings as errors # noqa E402   
import warnings                # noqa E402


def arid_eda(df, response, response_type, features=[]):
    """
    Function to create summary statistics and basic EDA plots. Given a data
    frame, this function outputs general exploratory analysis plots as well
    as basic statistics summarizing trends in the features of the input data.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to analyze
    response : str
        A column name of the response variable
    response_type: str
        Input either 'categorical' or 'continous to indicate response type
    features : list
        A list of the feature names to perform EDA on

    Returns
    -------
    altair.Chart
        Plots relevant to the exploratory data analysis

    pandas.DataFrame
        A dataframe containing summary statistics relevant to the
        selected feature and response variable.

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> dataframe, plots = arid_eda(house_prices,
                                    'price',
                                    'continuous,
                                    ['rooms', 'age','garage'])

    >>> dataframe, plots = arid_eda(iris_data,
                                    'species',
                                    categorical,
                                    ['petalWidth', 'sepalWidth','petalLength'])

    """
    #########################################################################

    assert type(df) == pd.core.frame.DataFrame, \
        'Input data must be a Pandas DataFrame'

    assert response in df.columns, \
        'Response variable is not contained within dataframe'

    for feat in features:
        assert feat in df.columns, \
            f'{feat} is not contained within dataframe'

    assert response not in features, \
        'Response variable must be distinct from features'

    if df[response].dtype == np.dtype('O'):
        assert response_type == 'categorical', \
            'Current response variable is not continuous'

    if df[response].dtype != np.dtype('O'):
        assert response_type == 'numeric', \
            'Current response variable is not categorical'

    assert response_type in ['categorical', 'continuous'], \
        'Response must be categorical or continuous'

    ###########################################################################

    chartlist = []
    corr_plot_width = 70*len(set(features))
    corr_plot_height = 70*len(set(features))
    filter_df = df.loc[:, features]

    if response_type == "categorical":
        for feat in features:  # Creates density plots for each feature
            chart = (
                alt.Chart(df, title=(feat + " Distribution"))
                .transform_density(
                    feat, as_=[feat, "density"], groupby=[response]
                )
                .mark_area(interpolate="monotone", opacity=0.7)
                .encode(y="density:Q", x=alt.X(feat), color=response)
            )
            chartlist.append(chart)

    elif response_type == 'continuous':
        for feat in features:  # Creates histograms for each feature
            chart = (
                alt.Chart(df, title=(feat + " Distribution"))
                .mark_bar()
                .encode(  # only works currently if response is continuous
                    y="count()", x=alt.X(feat, bin=alt.Bin(), title=feat)
                )
                .properties(width=200, height=200)
            )
            chartlist.append(chart)

#      for i in range(len(chartlist)):
#         if i == 0:
#             dist_output = chartlist[i]
#         elif i == 1:
#             dist_output = alt.hconcat(dist_output, chartlist[i])
#         elif i % 2 == 1:
#             dist_output = alt.vconcat(dist_output, chartlist[i])

    row_list = []  # output feature distributions as a square
    first_row = True
    for i in range(len(chartlist)):
        if i == 0:
            current_row = chartlist[i]
        elif i % 2 != 0:
            current_row = alt.hconcat(current_row, chartlist[i])
        elif i % 2 == 0:
            row_list.append(current_row)
            current_row = chartlist[i]

    row_list.append(current_row)

    for row in row_list:
        if first_row:
            dist_output = row
            first_row = False
        else:
            dist_output = alt.vconcat(dist_output, row)

    corr_df = filter_df.corr('spearman').stack().reset_index(name='corr')
    corr_df.loc[corr_df['corr'] == 1, 'corr'] = 0
    corr_df['corr_label'] = corr_df['corr'].map('{:.2f}'.format)
    corr_df['abs'] = corr_df['corr'].abs()

    base = alt.Chart(corr_df, title='Feature Correlation').encode(
            x=alt.X('level_0', axis=alt.Axis(title='')),
            y=alt.Y('level_1', axis=alt.Axis(title=''))
        ).properties(width=corr_plot_width, height=corr_plot_height)

    text = base.mark_text().encode(
        text='corr_label',
        color=alt.value('white')
    )

    cor_sq = base.mark_rect().encode(
        color=alt.Color('corr', scale=alt.Scale(scheme='blueorange'))
    )

    corr_plot = cor_sq + text
    return_df = pd.DataFrame(filter_df.describe())

    return return_df, dist_output | corr_plot


def arid_linreg(df, response, features=[], regularization=None, alpha=1):
    """
    Function that performs a linear regression on continuous response data,
    using both an sklearn and statsmodel model analogs. These models are
    optimized for prediction and inference, respectively.

    Parameters
    ----------
    data_frame : pandas.Dataframe
        The input dataframe to analyze
    response : str
        A column name of the response variable
    features : list (optional)
        A list of the chosen explanatory feature columns
    regularization : str (optional)
        What level of regularization to use in the model values:
        * L1 * L2 * L1L2
    alpha : float
        The regularization weight strength

    Returns
    -------
    sklearn.linear_model
        A fitted sklearn model configured with the chosen input parameters
    statsmodels.regression.linear_model
        A fitted statsmodel configured with the chosen input parameters
    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_linreg(df, income)
    """
    # Validate input arguments
    assert isinstance(df, pd.DataFrame), errors.INVALID_DATAFRAME
    assert not df.empty, errors.EMPTY_DATAFRAME
    assert response in df.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert ptypes.is_numeric_dtype(df[response].dtype), \
        errors.INVALID_RESPONSE_DATATYPE
    assert regularization in [None, "L1", "L2", "L1L2"], \
        errors.INVALID_REGULARIZATION_INPUT
    assert ptypes.is_numeric_dtype(type(alpha)), errors.INVALID_ALPHA_INPUT

    # Isolate numeric features from dataframe
    feature_df = df.drop(response, axis=1)
    feature_list = feature_df.select_dtypes(['number']).columns

    # Report features that have been discarded to the user
    if len(feature_df.columns) != len(feature_list):
        non_numeric_features = [
            feature for feature in feature_df.columns if not (feature in feature_list) # noqaE501
        ]
        warnings.warn(
            f"These features are non-numeric and will be discarded: {non_numeric_features}" # noqaE501
        )

    # Create a subset of user selected features if supplied
    if len(features) > 0:
        feature_list = set(features).intersection(feature_list)
        # Report any user selected features that were not found
        if len(feature_list) != len(features):
            missing_features = [
                feature for feature in features if not (feature in feature_list) # noqaE501
            ]
            warnings.warn(
                f"These user-selected features are not present in data: {missing_features}" # noqaE501
            )

    # Assert that there are still features available to perform regression
    assert len(feature_list) > 0, errors.NO_VALID_FEATURES
    print(f"Feature list: {feature_list}")

    # Formally define our features and response
    X = df[feature_list]
    y = df[response]

    # Create and fit analagous models in sklearn and statsmodels
    if regularization == "L1":
        skl_model = Lasso(alpha, fit_intercept=False).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt=1, alpha=alpha)
    elif regularization == "L2":
        skl_model = Ridge(alpha, fit_intercept=False).fit(X, y)
        # No idea why statsmodels L2 alpha requires the division by 3, but it
        # was tested empirically and coefficients/predictions match...
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt=0, alpha=alpha/3)
    elif regularization == "L1L2":
        skl_model = ElasticNet(alpha, fit_intercept=False).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt=0.5,
                                                alpha=alpha)
    else:
        skl_model = LinearRegression(fit_intercept=False).fit(X, y)
        sm_model = sm.OLS(y, X).fit()

    # Display model coefficients to user
    print(pd.DataFrame({'statsmodel coefficients': sm_model.params,
                        'sklearn coefficients': skl_model.coef_}, index=feature_list)) # noqa E501

    return skl_model, sm_model


def arid_logreg(df, response, features=[], type="binomial"):
    """Function to fit a binomial or multinomial logistic regression.

    Function that performs a binomial or multinomial logistic regression
    using both an sklearn and statsmodel model analogs. These models are
    optimized for prediction and inference, respectively, and returns the
    statistical summary.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to analyze
    response : str
        A column name of the response variable
    features : list
        A list of the column names as explanatory variables
    type : str
        Classification type. Either "binomial" or "multinomial"

    Returns
    -------
    sklearn.linear_model
        A fitted logistic regression sklearn model configured with
        the chosen input parameters
    statsmodels.discrete.discrete_model
        A fitted Logit statsmodel configured with the chosen input parameters

    Examples
    --------
    >>> aridanalysis.arid_logreg(df,
                                'Target',
                                ['feat1', 'feat2', 'feat3'],
                                type="binomial")
    """
    # Validate input arguments
    assert isinstance(df, pd.DataFrame), errors.INVALID_DATAFRAME
    assert not df.empty, errors.EMPTY_DATAFRAME
    assert response in df.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert type in ["binomial", "multinomial"], errors.INVALID_TYPE_INPUT

    # Get features list from df
    feature_df = df.drop(response, axis=1)
    feature_list = feature_df.select_dtypes(['number']).columns

    # Report features that have been discarded to the user
    if len(feature_df.columns) != len(feature_list):
        non_numeric_features = [feature for feature in feature_df.columns if not (feature in feature_list)] # noqaE501
        warnings.warn(f"These features are non-numeric and will be discarded: {non_numeric_features}") # noqaE501

    # Create a subset of user selected features if supplied
    if len(features) > 0:
        feature_list = set(features).intersection(feature_list)
        # Report any user selected features that were not found
        if len(feature_list) != len(features):
            missing_features = [feature for feature in features if not (feature in feature_list)] # noqaE501
            warnings.warn(f"These user-selected features are not present in data: {missing_features}") # noqaE501

    # Assert that there are still features available to perform classification
    assert len(feature_list) > 0, errors.NO_VALID_FEATURES

    # Formally define our features and response
    X = df[feature_list]
    y = df[response]

    # Create and fit analagous models in sklearn and statsmodels
    if type == "binomial":
        skl_model = LogisticRegression(penalty='none', fit_intercept = False, multi_class='ovr').fit(X, y) # noqaE501
        sm_model = sm.Logit(y, X).fit(method="bfgs")

    else:
        skl_model = LogisticRegression(penalty='none', fit_intercept = False, multi_class='multinomial').fit(X, y) # noqaE501
        sm_model = sm.MNLogit(y, X).fit()

    # Display model coefficients to user
    print(pd.DataFrame(skl_model.coef_, columns=feature_list))
    print(sm_model.summary())

    return skl_model, sm_model


def arid_countreg(data_frame, response, con_features=[], cat_features=[], model="additive", alpha=1): # noqaE501
    """
    Function that performs a count regression on a numerical discete response
    data, using both an sklearn and statsmodel model analogs (prediction and
    inference). The function will return both models,each one with their
    respective insights.

    Parameters
    ----------
    data_frame : pandas.Dataframe
      The input dataframe to analyze.
    response : str
      A column name of the response variable. Because the function manipulates
      count data, it must be of type int.
    con_features : list
      A list of the continuous explanatory variables to be used in the
      analysis. Default value is None, meaning to use all the numerical
      columns in the data frame.
    cat_features : list
      A list of the categorical explanatory variables to be used in the
      analysis.Default value is None, meaning to use all the categorical
      columns in the data frame.
    model: str
      Model type. Either "additive" or "interactive"
    alpha: float
      Constant the controls regularization strength in predictive model

    Returns
    -------
    sklearn.linear_model
        A fitted sklearn model configured with the chosen input parameters
    statsmodels.regression.linear_model
        A fitted statsmodel configured with the chosen input parameters

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_countreg(df,
                                  income,
                                  features=[feat1, feat5],
                                  "additive")
    """
    assert isinstance(con_features, list), "ERROR: INVALID LIST INTPUT PASSED"
    assert isinstance(cat_features, list), "ERROR: INVALID LIST INTPUT PASSED"

    # Deal with the features column
    if len(con_features) == 0:
        con_features = (
            data_frame.drop(columns=[response]).select_dtypes("number")
            .columns.tolist()
        )
    if len(cat_features) == 0:
        cat_features = (
            data_frame.drop(columns=[response])
            .select_dtypes(["category", "object"])
            .columns.tolist()
        )

    assert isinstance(data_frame, pd.DataFrame), errors.INVALID_DATAFRAME
    assert not data_frame.empty, errors.EMPTY_DATAFRAME
    assert response in data_frame.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert all(item in data_frame.columns.tolist() for item in con_features), \
        "ERROR: CONTINUOUS VARIABLE(S) NOT IN DATAFRAME"
    assert all(item in data_frame.columns.tolist() for item in cat_features), \
        "ERROR: CATEGORICAL VARIABLE(S) NOT IN DATAFRAME"
    assert ptypes.is_integer_dtype(data_frame[response].dtype), \
        "ERROR: INVALID RESPONSE DATATYPE FOR COUNT REGRESSION: MUST BE TYPE INT" # noqaE501
    assert model in ["additive", "interactive"], "ERROR: INVALID MODEL PASSED"
    assert ptypes.is_numeric_dtype(type(alpha)), errors.INVALID_ALPHA_INPUT

    # Scikit Learn Model
    if len(cat_features) != 0:
        X_sk = data_frame[con_features + cat_features]
        y_sk = data_frame[response]
        preprocessor = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore"), cat_features)
        )
        pipeline = make_pipeline(
            preprocessor,
            PoissonRegressor(
                alpha=alpha,
                fit_intercept=True,
            ),
        )
        sk_model = pipeline.fit(X_sk, y_sk)
    else:
        X_sk = data_frame[con_features]
        y_sk = data_frame[response]
        pipeline = make_pipeline(
            PoissonRegressor(alpha=0, fit_intercept=True, max_iter=100)
        )
        sk_model = pipeline.fit(X_sk, y_sk)

    # Aditive inferential model
    if model == "additive":
        cat_features = ["C(" + i + ")" for i in cat_features]
        con_list = "".join(
            [f"{i}" if i is con_features[0] else f" + {i}" for i in con_features] # noqaE501
        )
        cat_list = "".join(
            [f"{i}" if i is cat_features[0] else f" + {i}" for i in cat_features] # noqaE501
        )
        if len(cat_list) > 0:
            formula = f"{response} ~ {con_list} + {cat_list}"
        else:
            formula = f"{response} ~ {con_list}"
        glm_count = smf.glm(
            formula=formula, data=data_frame, family=sm.families.Poisson()
        ).fit()
        print(glm_count.summary())
    else:
        cat_features = ["C(" + i + ")" for i in cat_features]
        con_list = "".join(
            [f"{i}" if i is con_features[0] else f" + {i}" for i in con_features] # noqaE501
        )
        cat_list = "".join(
            [f"{i}" if i is cat_features[0] else f" + {i}" for i in cat_features] # noqaE501
        )
        interact_list = "".join(
            [
                f"{i} * {j}"
                if j is cat_features[0] and i is con_features[0]
                else f" + {i} * {j}"
                for i in con_features
                for j in cat_features
            ]
        )
        equal = set()
        cont_interaction = ""
        for i in con_features[0:]:
            for j in con_features[1:]:
                if i is con_features[0] and j is con_features[1]:
                    cont_interaction = f"{i} * {j}"
                    equal.update([(i, j)])
                    if len(equal) > 0:
                        continue
                if i != j and (j, i) not in equal:
                    equal.update([(i, j)])
                    cont_interaction += f" + {i} * {j}"
        if len(cat_features) > 0 and len(cont_interaction) > 0:
            formula = f"{response} ~ {con_list} + {cat_list} + {interact_list} + {cont_interaction}" # noqaE501
        elif len(cat_features) == 0 and len(cont_interaction) > 0:
            formula = f"{response} ~ {con_list} + {cont_interaction}"
        elif len(cat_features) > 0 and len(cont_interaction) == 0:
            formula = f"{response} ~ {con_list} + {cat_list} + {interact_list}"
        else:
            formula = f"{response} ~ {con_list}"
        glm_count = smf.glm(formula=formula,
                            data=data_frame,
                            family=sm.families.Poisson()).fit()
        print(glm_count.summary())

    return (sk_model, glm_count)
