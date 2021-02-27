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
