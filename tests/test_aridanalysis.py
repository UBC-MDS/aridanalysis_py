from aridanalysis import __version__
from aridanalysis import aridanalysis as aa

import pytest

import pandas as pd
import sklearn

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

def test_linreg_input_errors(simple_frame):
    '''
    Test linear regression input argument validation
    '''
    with pytest.raises(AssertionError, match="ERROR: INVALID DATAFRAME INPUT"):
        aa.arid_linreg(6, 'y')
    with pytest.raises(AssertionError, match="ERROR: EMPTY DATAFRAME INPUT"):
        aa.arid_linreg(pd.DataFrame(), 'y')
    with pytest.raises(AssertionError, match="ERROR: INVALID RESPONSE INPUT"):
        aa.arid_linreg(simple_frame, 'z')
    with pytest.raises(AssertionError, match="ERROR: INVALID RESPONSE DATATYPE"):
        aa.arid_linreg(simple_frame, 'x4')
    with pytest.raises(AssertionError, match="ERROR: INVALID REGULARIZATION INPUT"):
        aa.arid_linreg(simple_frame, 'y', regularization = "L3")
    with pytest.raises(AssertionError, match="ERROR: INVALID ALPHA INPUT"):
        aa.arid_linreg(simple_frame, 'y', alpha = 'b')

def test_linreg_input_features(simple_frame):
    '''
    Test linear regression input feature arguments
    '''
    with pytest.raises(AssertionError, match="ERROR: NO VALID FEATURES"):
        aa.arid_linreg(simple_frame[['y']], 'y')
    with pytest.raises(AssertionError, match="ERROR: NO VALID FEATURES"):
        aa.arid_linreg(simple_frame[['x4', 'y']], 'y')
    with pytest.raises(AssertionError, match="ERROR: NO VALID FEATURES"):
        aa.arid_linreg(simple_frame, 'y', features=['b'])
    with pytest.raises(AssertionError, match="ERROR: NO VALID FEATURES"):
        aa.arid_linreg(simple_frame, 'y', features=['x4'])
    assert len(aa.arid_linreg(simple_frame, 'y').coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=simple_frame.columns).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3']).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3','x4']).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1']).coef_) == 1
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x2']).coef_) == 1

def test_linreg_model_types(simple_frame):
    assert type(aa.arid_linreg(simple_frame, 'y')) == sklearn.linear_model._base.LinearRegression
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L1')) == sklearn.linear_model._coordinate_descent.Lasso
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L2')) == sklearn.linear_model._ridge.Ridge
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')) == sklearn.linear_model._coordinate_descent.ElasticNet