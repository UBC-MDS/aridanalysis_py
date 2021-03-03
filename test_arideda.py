import pytest
import altair as alt
import pandas as pd
from vega_datasets import data
from aridanalysis import arideda


def test_arideda_return():
    '''
    Test return data type
    '''

    out = arideda(data.iris())
    assert isinstance(out, alt.VConcatChart)


def test_arideda_features():
    """
    Test calling with valid features list
    """
    out = explore_feature_map(data.iris(), ['sepalLength', 'sepalWidth'])
    assert isinstance(out, alt.VConcatChart)


def test_arideda_numfeature():
    """
    Test calling with features list containing non-numeric feature
    """
    with pytest.raises(ValueError, match='features are non-numeric'):
        explore_feature_map(data.iris(), ['sepalLength', 'species'])

def test_arideda_feature_exists()
    """
    Test passing non-existent feature in features list
    """
    with pytest.raises(ValueError, match='Non-existent features'):
        explore_feature_map(data.iris(), ['petalWidth', 'fakeHeight'])

def test_arideda_empty_df():
    """
    Test passing empty data frame
    """
    with pytest.raises(ValueError, match='Empty dataframe'):
        explore_feature_map(pd.DataFrame())
