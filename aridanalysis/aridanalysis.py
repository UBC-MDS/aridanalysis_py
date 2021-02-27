def arid_linreg(df, response, features = [], estimator = None, regularization = None):
    """
    Function that performs a linear regression on continuous response data. 
    This function will fit a linear regression model on the input .

    Parameters
    ----------
    df : pandas.Dataframe
        A dataframe that contains the data to be analized
    response : string
        A column name of the response variable
    features : list (optional)
        A list of the chosen explanatory feature columns
    estimator : function (optional)
        The function used to fit the linear regression model The default is OLS
    regularization : string (optional)
        What level of regularization to use in the model values:
        * L1 * L2 * L1L2 *
        
    Returns
    -------
    pandas.DataFrame
        A pandas dataframe with a list of features, and their coefficients 

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_linreg(df, income)
    """
    return None

def arid_countreg():
    """
    Function that performs linear regression on counting data, when the response
    is restricted to be positive and natural. This function will perform count 
    regression to the specified columns of a dataframe in function of the response, 
    and return a substantial inferential analysis.

    Parameters
    ----------
    df : pandas.Dataframe
      A dataframe that contains the data to be analized
     : string
      A column name of the response variable
    c : list
    
    polynomial: boolean
      Wheter the model should consider polynomial degree of 2 in the linear combination or not.
    additive: 
      
     
    
    

    Returns
    -------

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_countreg(df, income, features)
    """
    x=4
    print(x)
    return x