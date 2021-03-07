from aridanalysis import __version__
from aridanalysis import aridanalysis as aa
import pytest
import pandas as pd
import numpy as np
import sklearn
from vega_datasets import data
import altair as alt
import statsmodels 
import warnings

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../aridanalysis')
import error_strings as errors

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def simple_frame(): 
    '''
    Create a basic test dataframe for linear regression tests
    '''
    tdf = pd.DataFrame({'x1': [1, 0, 0], 
                        'x2': [0, 1.0, 0], 
                        'x3': [0, 0, 1],
                        'x4': ['a', 'a', 'b'],
                        'y': [1, 3, -1.0]})
    return tdf

def test_arideda_return():
    """
    Test return data type
    """
    _ , out = aa.arid_eda(data.iris(), 'species', 'categorical', ['sepalLength', 'sepalWidth'])
    assert isinstance(out, alt.HConcatChart)


def test_arideda_features():
    """
    Test calling with valid features list
    """
    out, _ = aa.arid_eda(data.iris(), 'species', 'categorical', ['sepalLength', 'sepalWidth'])
    assert isinstance(out, pd.core.frame.DataFrame)


def test_arideda_numfeature():
    """
    Ensure data frame is appropriate size according to features
    """
    features = ['sepalLength', 'sepalWidth']
    out, _ = aa.arid_eda(data.iris(), 'species', 'categorical', features)
    assert out.shape == (8,len(features))

def test_arideda_returns_tuple():
    """
    Check that function returns two items
    """
    assert len(aa.arid_eda(data.iris(), 'species', 'categorical', ['sepalLength', 'sepalWidth'])) == 2


def test_arideda_empty_df():
    """
    Test if error occurs when repsonse type is not categorical or continuous
    """
    with pytest.raises(KeyError):
        aa.arid_eda(data.iris(), 'species', 'ORDINAL', ['sepalLength', 'sepalWidth'])

def test_response_type_incorrect():
    """
    Test if an error occurs when wrong response type is given
    """
    with pytest.raises(KeyError):
        aa.arid_eda(data.iris(), 'petalLength', 'categorical', ['sepalLength', 'sepalWidth'])

def test_linreg_input_errors(simple_frame):
    '''
    Test linear regression input argument validation
    '''
    with pytest.raises(AssertionError, match=errors.INVALID_DATAFRAME):
        aa.arid_linreg(6, 'y')
    with pytest.raises(AssertionError, match=errors.EMPTY_DATAFRAME):
        aa.arid_linreg(pd.DataFrame(), 'y')
    with pytest.raises(AssertionError, match=errors.RESPONSE_NOT_FOUND):
        aa.arid_linreg(simple_frame, 'z')
    with pytest.raises(AssertionError, match=errors.INVALID_RESPONSE_DATATYPE):
        aa.arid_linreg(simple_frame, 'x4')
    with pytest.raises(AssertionError, match=errors.INVALID_REGULARIZATION_INPUT):
        aa.arid_linreg(simple_frame, 'y', regularization = "L3")
    with pytest.raises(AssertionError, match=errors.INVALID_ALPHA_INPUT):
        aa.arid_linreg(simple_frame, 'y', alpha = 'b')

def test_linreg_input_features(simple_frame):
    '''
    Test linear regression input feature arguments
    '''
    with pytest.raises(AssertionError, match=errors.NO_VALID_FEATURES):
        aa.arid_linreg(simple_frame[['y']], 'y')
    with pytest.raises(AssertionError, match=errors.NO_VALID_FEATURES):
        aa.arid_linreg(simple_frame[['x4', 'y']], 'y')
    with pytest.raises(AssertionError, match=errors.NO_VALID_FEATURES):
        aa.arid_linreg(simple_frame, 'y', features=['b'])
    with pytest.raises(AssertionError, match=errors.NO_VALID_FEATURES):
        aa.arid_linreg(simple_frame, 'y', features=['x4'])
    with pytest.warns(UserWarning):
        aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3','x4'])
    with pytest.warns(UserWarning):
        aa.arid_linreg(simple_frame, 'y', features=['x1','b'])
    assert len((aa.arid_linreg(simple_frame, 'y'))[0].coef_) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=simple_frame.columns))[0].coef_) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3']))[0].coef_) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3','x4']))[0].coef_) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1']))[0].coef_) == 1
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2']))[0].coef_) == 2
    assert len((aa.arid_linreg(simple_frame, 'y'))[1].params) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=simple_frame.columns))[1].params) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3']))[1].params) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3','x4']))[1].params) == 3
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1']))[1].params) == 1
    assert len((aa.arid_linreg(simple_frame, 'y', features=['x1','x2']))[1].params) == 2

def test_linreg_model_types(simple_frame):
    '''
    Test linear regression output model types
    '''
    assert type((aa.arid_linreg(simple_frame, 'y'))[0]) == \
        sklearn.linear_model._base.LinearRegression
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L1'))[0]) == \
        sklearn.linear_model._coordinate_descent.Lasso
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L2'))[0]) == \
        sklearn.linear_model._ridge.Ridge
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2'))[0]) == \
        sklearn.linear_model._coordinate_descent.ElasticNet
    assert type((aa.arid_linreg(simple_frame, 'y'))[1]) == \
        statsmodels.regression.linear_model.RegressionResultsWrapper
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L1'))[1]) == \
        statsmodels.base.elastic_net.RegularizedResultsWrapper
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L2'))[1]) == \
        statsmodels.base.elastic_net.RegularizedResults
    assert type((aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2'))[1]) == \
        statsmodels.base.elastic_net.RegularizedResultsWrapper

def test_linreg_model_coefficients(simple_frame):
    '''
    Test linear regression output statsmodel and sklearn model coefficients match
    '''
    assert aa.arid_linreg(simple_frame, 'y')[0].coef_.all() == \
           (aa.arid_linreg(simple_frame, 'y')[1].params).to_numpy().all()
    assert aa.arid_linreg(simple_frame, 'y', regularization = 'L1')[0].coef_.all() == \
           (aa.arid_linreg(simple_frame, 'y', regularization = 'L1')[1].params).to_numpy().all()
    assert aa.arid_linreg(simple_frame, 'y', regularization = 'L2')[0].coef_.all() == \
           (aa.arid_linreg(simple_frame, 'y', regularization = 'L2')[1].params).all()
    assert aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')[0].coef_.all() == \
           (aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')[1].params).to_numpy().all()

def test_linreg_model_predictions(simple_frame):
    '''
    Test linear regression output statsmodel and sklearn model predictions match
    '''
    assert round(aa.arid_linreg(simple_frame, 'y')[0].predict(np.array([[1,4,3]]))[0], 3) == \
           round((aa.arid_linreg(simple_frame, 'y')[1].predict(np.array([[1,4,3]])))[0], 3)
    assert round(aa.arid_linreg(simple_frame, 'y', regularization = 'L1')[0].predict(np.array([[1,4,3]]))[0], 3) == \
           round((aa.arid_linreg(simple_frame, 'y', regularization = 'L1')[1].predict(np.array([[1,4,3]])))[0], 3)
    assert round(aa.arid_linreg(simple_frame, 'y', regularization = 'L2')[0].predict(np.array([[1,4,3]]))[0], 3) == \
           round((aa.arid_linreg(simple_frame, 'y', regularization = 'L2')[1].predict(np.array([[1,4,3]])))[0], 3)
    assert round(aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')[0].predict(np.array([[1,4,3]]))[0], 3) == \
           round((aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')[1].predict(np.array([[1,4,3]])))[0], 3)

@pytest.fixture
def log_df(): 
    '''
    Create a basic test dataframe for logistic regression tests
    '''
    data = [[32, "male", 80, 0], 
            [26, "female", 65, 1], 
            [22, "female", 75, 1], 
            [36, "male", 85, 0], 
            [45, "male", 82, 1], 
            [18, "female", 57, 0], 
            [57, "male", 60, 1]] 
    log_df = pd.DataFrame(data, columns = ['Age', 'Sex', 'Weight', 'Target']) 
    return log_df

def test_logreg_model_inputs(log_df):
    with pytest.raises(AssertionError, match=errors.INVALID_INPUT_LIST):
        aa.arid_logreg(log_df, response="Target", features="Age", type="binomial")
    with pytest.raises(AssertionError, match=errors.INVALID_DATAFRAME):
        aa.arid_logreg(17, response="Target", features=["Age", "Sex"], type="binomial")
    with pytest.raises(AssertionError, match=errors.EMPTY_DATAFRAME):
        aa.arid_logreg(pd.DataFrame(), response="Target", features=["Age", "Sex"], type="binomial")
    with pytest.raises(AssertionError, match=errors.RESPONSE_NOT_FOUND):
        aa.arid_logreg(df=log_df, response="targ", features=["Age", "Sex"], type="binomial")    
    with pytest.raises(AssertionError, match=errors.INVALID_TYPE):
        aa.arid_logreg(log_df, response="Target", features=["Age", "Sex"], type="ordinal")   

def test_logreg_model_outputs(log_df):
    assert round((aa.arid_logreg(df=log_df, response="Target", features=[], type="binomial")[0].coef_)[0][0], 3) == 0.091
    assert round((aa.arid_logreg(log_df, response="Target", features=["Age"], type="binomial")[0].coef_)[0][0], 3) == 0.015
    assert round((aa.arid_logreg(log_df, response="Target", features=["Weight"], type="binomial")[0].coef_)[0][0], 3) == 0.003
    assert type(aa.arid_logreg(df=log_df, response="Target", features=[], type="binomial")[1]) == statsmodels.discrete.discrete_model.BinaryResultsWrapper 
def health_df(): 
    '''
    Create a basic test dataframe for linear regression tests
    '''
    health_df = pd.read_csv("tests/toy_data/badhealth.csv").drop(columns=["Unnamed: 0"])
    health_df["badh"] = health_df["badh"].astype('category')
    health_df["badh"] = health_df.badh.replace({0: 'bad', 1 : 'good'})
    return health_df


def test_countreg_model_inputs(health_df):
    with pytest.raises(AssertionError, match="ERROR: INVALID LIST INTPUT PASSED"):
        aa.arid_countreg(health_df, response="numvisit", con_features="age", cat_features=["badh"], model="additive")
    with pytest.raises(AssertionError, match="ERROR: INVALID LIST INTPUT PASSED"):
        aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features="badh", model="additive")
    with pytest.raises(AssertionError, match=errors.INVALID_DATAFRAME):
        aa.arid_countreg(17, response="numvisit", con_features=["age"], cat_features=["badh"], model="additive")
    with pytest.raises(AssertionError, match=errors.EMPTY_DATAFRAME):
        aa.arid_countreg(pd.DataFrame(), response="numvisit", con_features=["age"], cat_features=["badh"], model="additive")
    with pytest.raises(AssertionError, match=errors.RESPONSE_NOT_FOUND):
        aa.arid_countreg(data_frame=health_df, response="num", con_features=["age"], cat_features=["badh"], model="additive")    
    with pytest.raises(AssertionError, match="ERROR: INVALID RESPONSE DATATYPE FOR COUNT REGRESSION: MUST BE TYPE INT"):
        aa.arid_countreg(data_frame=health_df, response="badh", con_features=["age"], cat_features=[], model="additive")
    with pytest.raises(AssertionError, match="ERROR: INVALID MODEL PASSED"):
        aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features=[], model="additives")
    with pytest.raises(AssertionError, match=errors.INVALID_ALPHA_INPUT):
        aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features=[], model="additive",alpha="san")
        
def test_countreg_model_outputs(health_df):
    assert len(aa.arid_countreg(data_frame = health_df, response="numvisit", con_features=["age"], cat_features=["badh"], model="additive")[0][1].coef_) == 2
    assert len(aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features=["badh"], model="interactive")[0][1].coef_) == 2
    #In scikit learn interactions do not change the number of coefficients, this a weighted depening con correlation with other features
    assert len(aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features=["badh"], model="additive")[1].params) == 3
    assert len(aa.arid_countreg(health_df, response="numvisit", con_features=["age"], cat_features=["badh"], model="interactive")[1].params) == 4
    assert str(type(aa.arid_countreg(data_frame = health_df, response="numvisit", 
                                model="additive")[0])) == "<class 'sklearn.pipeline.Pipeline'>"
    assert str(type(aa.arid_countreg(data_frame = health_df, response="numvisit", 
                                    model="interactive")[1])) == "<class 'statsmodels.genmod.generalized_linear_model.GLMResultsWrapper'>"


    

    

