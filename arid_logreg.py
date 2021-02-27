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
    >>> arid_logreg(df, 'target', ['feat1', 'feat2', 'feat3'], type="multinomial")
    """