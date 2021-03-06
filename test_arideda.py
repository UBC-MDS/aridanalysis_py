import pytest
import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data
from aridanalysis import aridanalysis as aa


def test_arideda_return():
    '''
    Test return data type
    '''
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