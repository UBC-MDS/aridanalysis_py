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