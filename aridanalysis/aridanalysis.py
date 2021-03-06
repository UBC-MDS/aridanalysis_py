import pandas as pd
import pandas.api.types as ptypes
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
import statsmodels.api as sm

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../aridanalysis')
import error_strings as errors
import warnings

def arid_eda(df, response, response_type, features=[]):
    """
    
    Function to create summary statistics and basic EDA plots. Given a data frame,
    this function outputs general exploratory analysis plots as well as basic 
    statistics summarizing trends in the features of the input data. 
    
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
    >>> dataframe, plots = arid_eda(house_prices, 'price', 'continuous, ['rooms', 'age','garage'])
    >>> dataframe, plots = arid_eda(iris_data, 'species', categorical,  ['petalWidth', 'sepalWidth','petalLength'])
    
    """
    
    
    ############################ Exception Handling #####################################
    if type(df) != pd.core.frame.DataFrame:
        raise KeyError('Input data must be a Pandas DataFrame')

    if response not in df.columns:
        raise KeyError('Response variable is not contained within dataframe')
    
    for feat in features:
        if feat not in df.columns: 
            raise KeyError(f'{feat} is not contained within dataframe')
    
    if response in features:
        raise KeyError('Response variable must be distinct from features')
    
    if df[response].dtype == np.dtype('O') and response_type == 'continuous':
        raise KeyError('Current response variable is not continuous')
    
    if df[response].dtype != np.dtype('O') and response_type == 'categorical':
        raise KeyError('Current response variable is not categorical')
    
    if response_type not in ['categorical', 'continuous']:
        raise KeyError('Response must be categorical or continuous')
    
    #####################################################################################
 
    chartlist = []
    corr_plot_width = 70*len(set(features))
    corr_plot_height = 70*len(set(features))
    filter_df = df.loc[:,features]
    
    
    if response_type == 'categorical':
        for feat in features:                                    # This function creates density plots for each feature 
            chart = alt.Chart(df, title=(feat + ' Distribution')).transform_density(     # only works currently if response is categorical 
                feat,
                as_=[feat, 'density'],
                groupby=[response]
                ).mark_area(interpolate='monotone', opacity=0.7).encode(
                y = 'density:Q',
                x = alt.X(feat),
                color=response) 
            chartlist.append(chart)
    
    elif response_type == 'continuous':
    
        for feat in features:                                     # This function creates histograms for each feature
            chart = alt.Chart(df, title=(feat + ' Distribution')).mark_bar().encode(      # only works currently if response is continuous 
                y = 'count()',
                x = alt.X(feat, bin=alt.Bin(), title = feat)
            ).properties(width=200, height=200)
            chartlist.append(chart)
    
#      for i in range(len(chartlist)):  
#         if i == 0:
#             dist_output = chartlist[i]
#         elif i == 1:
#             dist_output = alt.hconcat(dist_output, chartlist[i])
#         elif i % 2 == 1:
#             dist_output = alt.vconcat(dist_output, chartlist[i])

    row_list = []
    first_row = True
    row_len = (len(set(features))**(1/2))//1
    for i in range(len(chartlist)):  
        print(i)
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
    using both an sklearn and statsmodel model analogs. These models are optimized
    for prediction and inference, respectively.

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
    assert not df.empty , errors.EMPTY_DATAFRAME
    assert response in df.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert ptypes.is_numeric_dtype(df[response].dtype), errors.INVALID_RESPONSE_DATATYPE
    assert regularization in [None, "L1", "L2", "L1L2"], errors.INVALID_REGULARIZATION_INPUT
    assert ptypes.is_numeric_dtype(type(alpha)), errors.INVALID_ALPHA_INPUT
    
    # Isolate numeric features from dataframe
    feature_df = df.drop(response, axis=1)
    feature_list = feature_df.select_dtypes(['number']).columns
    
    # Report features that have been discarded to the user
    if len(feature_df.columns) != len(feature_list):
        non_numeric_features = [feature for feature in feature_df.columns if not (feature in feature_list)]
        warnings.warn(f"These features are non-numeric and will be discarded: {non_numeric_features}")
    
    # Create a subset of user selected features if supplied
    if len(features) > 0:
        feature_list = set(features).intersection(feature_list)
        # Report any user selected features that were not found
        if len(feature_list) != len(features):
            missing_features = [feature for feature in features if not (feature in feature_list)]
            warnings.warn(f"These user-selected features are not present in data: {missing_features}")

    # Assert that there are still features available to perform regression
    assert len(feature_list) > 0, errors.NO_VALID_FEATURES    
    print(f"Feature list: {feature_list}")
    
    # Formally define our features and response
    X = df[feature_list]
    y = df[response]
    
    # Create and fit analagous models in sklearn and statsmodels
    if regularization == "L1":
        skl_model = Lasso(alpha, fit_intercept = False).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 1, 
                                                    alpha = alpha)
    elif regularization == "L2":
        skl_model = Ridge(alpha, fit_intercept = False).fit(X, y)
        # No idea why statsmodels L2 alpha requires the division by 3, but it
        # was tested empirically and coefficients/predictions match...
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0, 
                                                    alpha = alpha/3)
    elif regularization == "L1L2":
        skl_model = ElasticNet(alpha, fit_intercept = False).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0.5, 
                                                alpha = alpha)
    else:
        skl_model = LinearRegression(fit_intercept = False).fit(X, y)
        sm_model = sm.OLS(y, X).fit()
     
    # Display model coefficients to user
    print(pd.DataFrame({'statsmodel coefficients' : sm_model.params,
                        'sklearn coefficients' : skl_model.coef_}, index = feature_list))
        
        
    return skl_model, sm_model
    
def arid_logreg(data_frame, response, features=[], type="binomial", model="additive", polynomial=False, alpha=0.05):
    """Function to fit a logistic regression for a binomial or multinomial classification.
    
    Given a data frame, a response variable and explanatory variables (features), 
    this function fits a logistic regression and outputs the statistical summary
    including the interpretation.
    
    Parameters
    ----------
    data_frame : pandas.DataFrame
        The input dataframe to analyze
    response : str
        A column name of the response variable
    features : list
        A list of the column names as explanatory variables
    type : str
        Classification type. Either "binomial", "ordinal" or "multinomial"
    model : str
        Model type. Either "additive" or "interactive"
    polynomial : bool
        Whether polynomial features should be considered or not
    alpha : float
        Significance level for analysis
    
    Returns
    -------
    pandas.DataFrame
        Data frame with 4 columns: 'features', 'p-value', 'significant', 'interpretation'
    
    Examples
    --------
    >>> aridanalysis.arid_logreg(df, 'target', ['feat1', 'feat2', 'feat3'], type="multinomial", 
    model="interactive", polynomial=True, alpha=0.01)
    """
    return None

def arid_countreg(data_frame, response, features=[], model="additive", polynomial=False, alpha=0.05):
    """
    A function that performs linear regression on counting data when the response is 
    restricted to be positive and natural. This function will perform count regression 
    to the specified columns    of a data frame and return a substantial inferential analysis.

    Parameters
    ----------
    data_frame : pandas.Dataframe
      The input dataframe to analyze
    response : str
      A column name of the response variable
    features : list
      A list of the explanatory variables to be used in the analysis. Default value is None, meaning
      to use all the features in the data frame
    polynomial: bool
      Whether the model should consider polynomial degree in the linear combination or not.
    model: str
      Model type. Either "additive" or "interactive"
    alpha: float
      Significance level for analysis
      

    Returns
    -------
    pandas.DataFrame
      Data frame with 4 columns: 'features', 'p-value', 'significant', 'interpretation'
    String
      Which family was used in the generalized linear regression model based on an overdispersion and fitting analysis
      

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_countreg(df, income, features = [feat1, feat5] ,"additive")
    """
    return None
