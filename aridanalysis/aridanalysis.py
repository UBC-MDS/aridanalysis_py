import pandas as pd
import pandas.api.types as ptypes
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
import statsmodels.api as sm

def arid_eda(data_frame, response, features=[]):
    """
    
    Function to create summary statistics and basic EDA plots. Given a data frame,
    this function outputs general exploratory analysis plots as well as basic 
    statistics summarizing trends in the features of the input data. 
    
    Parameters
    ----------
    data_frame : pandas.DataFrame
        The input dataframe to analyze
    response : str
        A column name of the response variable
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
    >>> arid_eda(house_prices, 'price', ['rooms', 'age','garage'])
    """
    return None

def arid_linreg(data_frame, response, features=[], estimator=None, regularization=None):
    """
    Function that performs a linear regression on continuous response data. 
    This function will fit a linear regression model on the input dataframe
    using the response supplied and all or optionally specified features given.

    Parameters
    ----------
    data_frame : pandas.Dataframe
        The input dataframe to analyze
    response : str
        A column name of the response variable
    features : list (optional)
        A list of the chosen explanatory feature columns
    estimator : function (optional)
        The function used to fit the linear regression model The default is OLS
    regularization : str (optional)
        What level of regularization to use in the model values:
        * L1 * L2 * L1L2
        
    Returns
    -------
    pandas.DataFrame
        A pandas dataframe with a list of features, and their coefficients 

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_linreg(df, income)
    """
def arid_linreg(df, response, features=[], regularization=None, alpha=1):
    
    assert isinstance(df, pd.DataFrame), "NOT A DATAFRAME"
    assert not df.empty , "EMPTY DATAFRAME"
    assert response in df.columns.tolist(), "RESPONSE NOT PRESENT"
    assert ptypes.is_numeric_dtype(df[response].dtype), "RESPONSE INCORRECT DATATYPE"
    assert regularization in [None, "L1", "L2", "L1L2"], "INVALID REGULARIZATION VALUE"
    assert ptypes.is_numeric_dtype(type(alpha)), "INVALID ALPHA VALUE"
    
    feature_df = df.drop(response, axis=1)
    feature_list = feature_df.select_dtypes(['number']).columns
    
    if len(feature_df.columns) != len(feature_list):
        non_numeric_features = [feature for feature in feature_df.columns if not (feature in feature_list)]
        print(f"Lost non-numeric features: {non_numeric_features}")
    
    if len(features) > 0:
        feature_list = set(features).intersection(feature_list)
        if len(feature_list) != len(features):
            missing_features = [feature for feature in features if not (feature in feature_list)]
            print(f"Missing features: {missing_features}")

    assert len(feature_list) > 0, "NO VALID FEATURES"    
    print(f"Feature list: {feature_list}")
    
    X = df[feature_list]
    y = df[response]
    
    if regularization == "L1":
        skl_model = Lasso(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 1, alpha = alpha)
    elif regularization == "L2":
        skl_model = Ridge(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0, alpha = alpha)
    elif regularization == "L1L2":
        skl_model = ElasticNet(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0.5, alpha = alpha)
    else:
        skl_model = LinearRegression().fit(X, y)
        sm_model = sm.OLS(y, X).fit()
        
    return skl_model
    
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
