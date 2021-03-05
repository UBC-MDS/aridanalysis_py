from aridanalysis import __version__
from aridanalysis import aridanalysis as aa
import pytest

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def simple_frame(): 
    tdf = pd.DataFrame({'x1': [1, 0, 0], 
                        'x2': [0, 1.0, 0], 
                        'x3': [0, 0, 1],
                        'x4': ['a', 'a', 'b'],
                        'y': [1, 3, -1.0]})
    return tdf

def test_linreg_input_errors():
    assert aa.arid_linreg(6, 'y') == AssertionError
    assert aa.arid_linreg(pd.DataFrame(), 'y') == AssertionError
    assert aa.arid_linreg(simple_frame, 'z') == AssertionError
    assert aa.arid_linreg(simple_frame, 'x1') == AssertionError
    assert aa.arid_linreg(simple_frame, 'y', regularization = "L3") == AssertionError
    assert aa.arid_linreg(simple_frame, 'y', alpha = 'b') == AssertionError

def test_linreg_features():
    assert aa.arid_linreg(simple_frame['y'], 'y') == AssertionError
    assert aa.arid_linreg(simple_frame['x4', 'y'], 'y') == AssertionError
    assert len(aa.arid_linreg(simple_frame, 'y').coef_) == 3
    assert aa.arid_linreg(simple_frame, 'y', features=['b']) == AssertionError
    assert aa.arid_linreg(simple_frame, 'y', features=['x4']) == AssertionError
    assert len(aa.arid_linreg(simple_frame, 'y', features=simple_frame.columns).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3']).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1','x2','x3','x4']).coef_) == 3
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x1']).coef_) == 1
    assert len(aa.arid_linreg(simple_frame, 'y', features=['x2']).coef_) == 1

def test_linreg_model_types():
    assert type(aa.arid_linreg(simple_frame, 'y')) == sklearn.linear_model._base.LinearRegression
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L1')) == sklearn.linear_model._coordinate_descent.Lasso
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L2')) == sklearn.linear_model._ridge.Ridge
    assert type(aa.arid_linreg(simple_frame, 'y', regularization = 'L1L2')) == sklearn.linear_model._coordinate_descent.ElasticNet