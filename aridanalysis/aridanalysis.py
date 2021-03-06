import pandas as pd
import pandas.api.types as ptypes
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import PoissonRegressor
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../aridanalysis')
import error_strings as errors

print(f"Invalid dataframe: {errors.INVALID_DATAFRAME}")

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
def arid_linreg(df, response, features=[], regularization=None, alpha=1):
    
    assert isinstance(df, pd.DataFrame), errors.INVALID_DATAFRAME
    assert not df.empty , errors.EMPTY_DATAFRAME
    assert response in df.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert ptypes.is_numeric_dtype(df[response].dtype), errors.INVALID_RESPONSE_DATATYPE
    assert regularization in [None, "L1", "L2", "L1L2"], errors.INVALID_REGULARIZATION_INPUT
    assert ptypes.is_numeric_dtype(type(alpha)), errors.INVALID_ALPHA_INPUT
    
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

    assert len(feature_list) > 0, errors.NO_VALID_FEATURES    
    print(f"Feature list: {feature_list}")
    
    X = df[feature_list]
    y = df[response]
    
    X = sm.add_constant(X)
    if regularization == "L1":
        skl_model = Lasso(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 1, 
                                                alpha = alpha,
                                                refit = True)
    elif regularization == "L2":
        skl_model = Ridge(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0, 
                                                alpha = alpha,
                                                refit = True)
    elif regularization == "L1L2":
        skl_model = ElasticNet(alpha).fit(X, y)
        sm_model = sm.OLS(y, X).fit_regularized(L1_wt = 0.5, 
                                                alpha = alpha,
                                                refit = True)
    else:
        skl_model = LinearRegression().fit(X, y)
        sm_model = sm.OLS(y, X).fit()
        
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

def arid_countreg(data_frame, response, con_features=[], cat_features=[], model="additive", alpha=1):
    """
    Function that performs a count regression on a numerical discete response data,
    using both an sklearn and statsmodel model analogs (prediction and inference). 
    The function will return both models,each one with their respective insights.

    Parameters
    ----------
    data_frame : pandas.Dataframe
      The input dataframe to analyze.
    response : str
      A column name of the response variable. Because the function manipulates count data, it must be of type int.
    con_features : list
      A list of the continuous explanatory variables to be used in the analysis. Default value is None, meaning
      to use all the numerical columns in the data frame.
    cat_features : list
      A list of the categorical explanatory variables to be used in the analysis. Default value is None, meaning
      to use all the categorical columns in the data frame.
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
    >>> aridanalysis.arid_countreg(df, income, features = [feat1, feat5] ,"additive")
    """
    assert isinstance(con_features, list), "ERROR: INVALID LIST INTPUT PASSED"
    assert isinstance(cat_features, list), "ERROR: INVALID LIST INTPUT PASSED"
    
    
    #Deal with the features column
    if len(con_features) == 0:
        con_features = data_frame.drop(columns=[response]).select_dtypes('number').columns.tolist()
    if len(cat_features) == 0:
        cat_features = data_frame.drop(columns=[response]).select_dtypes(['category', 'object']).columns.tolist()
    
    
    assert isinstance(data_frame, pd.DataFrame), errors.INVALID_DATAFRAME
    assert not data_frame.empty , errors.EMPTY_DATAFRAME
    assert response in data_frame.columns.tolist(), errors.RESPONSE_NOT_FOUND
    assert all(item in data_frame.columns.tolist() for item in con_features), "ERROR: CONTINUOUS VARIABLE(S) NOT IN DATAFRAME"
    assert all(item in data_frame.columns.tolist() for item in cat_features), "ERROR: CATEGORICAL VARIABLE(S) NOT IN DATAFRAME"
    assert ptypes.is_integer_dtype(data_frame[response].dtype), "ERROR: INVALID RESPONSE DATATYPE FOR COUNT REGRESSION: MUST BE TYPE INT"
    assert model in ["additive", "interactive"], "ERROR: INVALID MODEL PASSED"
    assert ptypes.is_numeric_dtype(type(alpha)), errors.INVALID_ALPHA_INPUT
    
    
  
    #Scikit Learn Model 
    if len(cat_features) != 0:
        X_sk = data_frame[con_features + cat_features]
        y_sk = data_frame[response]
        preprocessor = make_column_transformer((OneHotEncoder(handle_unknown="ignore"), cat_features))
        pipeline = make_pipeline(preprocessor, PoissonRegressor(alpha=alpha, fit_intercept=True,))
        sk_model = pipeline.fit(X_sk,y_sk)
    else:
        X_sk = data_frame[con_features]
        y_sk = data_frame[response]
        pipeline = make_pipeline(PoissonRegressor(alpha=0, fit_intercept=True, max_iter=100))
        sk_model = pipeline.fit(X_sk,y_sk)    
    #Aditive inferential model 
    if model == "additive":
        cat_features =["C(" + i + ")" for i in cat_features]
        con_list = "".join([f"{i}" if i is con_features[0] else f" + {i}"for i in con_features])
        cat_list = "".join([f"{i}" if i is cat_features[0] else f" + {i}"for i in cat_features])
        if len(cat_list) > 0:
            formula =  f"{response} ~ {con_list} + {cat_list}"
        else:
            formula =  f"{response} ~ {con_list}"
        glm_count= smf.glm(formula=formula, data=data_frame, family=sm.families.Poisson()).fit()
        print(glm_count.summary())   
    else :
        cat_features =["C(" + i + ")" for i in cat_features]
        con_list = "".join([f"{i}" if i is con_features[0] else f" + {i}"for i in con_features])
        cat_list = "".join([f"{i}" if i is cat_features[0] else f" + {i}"for i in cat_features])
        interact_list = "".join([f"{i} * {j}" if j is cat_features[0] and i is con_features[0] 
                         else f" + {i} * {j}" for i in con_features for j in cat_features])
        equal = set()
        cont_interaction = ""
        for i in con_features[0:]:
            for j in con_features[1:]:
                if i is con_features[0] and j is con_features[1]:
                    cont_interaction = f"{i} * {j}" 
                    equal.update([(i,j)])
                    if len(equal)>0:
                        continue
                if i != j and (j, i) not in equal:
                    equal.update([(i,j)])
                    cont_interaction += f" + {i} * {j}"
        if len(cat_features) > 0 and len(cont_interaction) > 0:
            formula = f"{response} ~ {con_list} + {cat_list} + {interact_list} + {cont_interaction}"
        elif len(cat_features) == 0 and len(cont_interaction) > 0:
            formula = f"{response} ~ {con_list} + {cont_interaction}"
        elif len(cat_features) > 0 and len(cont_interaction)  == 0:
            formula = f"{response} ~ {con_list} + {cat_list} + {interact_list}"
        else:
            formula = f"{response} ~ {con_list}"
        glm_count= smf.glm(formula=formula, data=data_frame, family=sm.families.Poisson()).fit()
        print(glm_count.summary())  
        
    return (sk_model, glm_count)
