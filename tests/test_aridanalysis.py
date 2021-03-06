from aridanalysis import __version__
from aridanalysis import aridanalysis as aa

import pytest

import pandas as pd
import sklearn

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../aridanalysis')
import error_strings as errors

def test_version():
    assert __version__ == '0.1.0'

health_df = pd.read_csv("badhealth.csv").drop(columns=["Unnamed: 0"])
health_df["badh"] = health_df["badh"].astype('category')