def arid_eda(data_frame, response, features):
    """Function to create summary statistics and basic EDA plots.
    
    Given a data frame, this function outputs general exploratory 
    analysis plots as well as basic statistics summarizing trends 
    in the features of the input data. 
    
    Parameters
    ----------
    data_frame : DataFrame
        A description of param1.
    response : str
        Column name of response variable
    features : list
    A list of the feature names to perform EDA on
    
    Returns
    -------
    altair.Chart
        Plots relevant to the exploratory data analysis
    
    DataFrame
        A dataframe containing summary statistics relevant to the 
        selected feature and response variable.
    Examples
    --------
    >>> arid_eda(house_prices, 'price', ['rooms', 'age','garage'])
    """
    return None

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
    
def arid_logreg(data_frame, response, features=[], type="binomial", model="additive", polynomial=False, alpha=0.05):
    """Function to fit a logistic regression for a binomial or multinomial classification.
    
    Given a data frame, a response variable and explanatory variables (features), 
    this function fits a logistic regression and outputs the statistical summary
    including the interpretation.
    
    Parameters
    ----------
    data_frame : DataFrame
        A description of param1.
    response : str
        Column name of response variable
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
    DataFrame
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
      A dataframe that contains the data to be analized.
    response : String
      A column name of the response variable
    features : list
      A list of the explanatory variables to be used in the analysis. Default value is None, meaning
      to use all the features in the data frame
    polynomial: boolean
      Wheter the model should consider polynomial degree in the linear combination or not.
    model: string
      Model type. Either "additive" or "interactive"
    alpha: float
     Significance level
      

    Returns
    -------
    DataFrame
      Data frame with 4 columns: 'features', 'p-value', 'significant', 'interpretation'
    String
      Which family was used in the generalized linear regression model based on an overdispersion and fitting analysis
      

    Examples
    --------
    >>> from aridanalysis import aridanalysis
    >>> aridanalysis.arid_countreg(df, income, features,"additiv")
    """
    return None