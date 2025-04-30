"""
Tests for the date_features module.
"""

import pandas as pd
import numpy as np
import pytest
from orama_utils.date_features import add_date_features


def test_add_date_features_basic():
    """Test the basic functionality of add_date_features."""
    # Create a sample dataframe
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'value': [10, 20, 30, 40, 50]
    })
    
    # Add all date features
    result = add_date_features(df)
    
    # Check that the original dataframe is unchanged
    assert len(df.columns) == 2
    
    # Check that the result contains the expected columns
    expected_columns = [
        'date', 'value', 'date_year', 'date_month', 'date_day', 
        'date_day_of_week', 'date_day_of_year', 'date_week_of_year', 
        'date_quarter', 'date_is_weekend', 'date_is_month_start', 
        'date_is_month_end', 'date_is_quarter_start', 'date_is_quarter_end', 
        'date_is_year_start', 'date_is_year_end', 'date_season'
    ]
    assert set(expected_columns).issubset(set(result.columns))
    
    # Check specific values
    assert result['date_year'].iloc[0] == 2023
    assert result['date_month'].iloc[0] == 1
    assert result['date_day'].iloc[0] == 1
    assert result['date_is_month_start'].iloc[0] == 1
    assert result['date_is_year_start'].iloc[0] == 1
    assert result['date_season'].iloc[0] == 'Winter'


def test_add_date_features_specific():
    """Test adding only specific date features."""
    # Create a sample dataframe
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'value': [10, 20, 30, 40, 50]
    })
    
    # Add only selected features
    selected_features = ['year', 'month', 'is_weekend', 'season']
    result = add_date_features(df, features=selected_features)
    
    # Check that only the selected features were added
    expected_columns = ['date', 'value', 'date_year', 'date_month', 'date_is_weekend', 'date_season']
    assert set(result.columns) == set(expected_columns)


def test_add_date_features_inplace():
    """Test adding date features inplace."""
    # Create a sample dataframe
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'value': [10, 20, 30, 40, 50]
    })
    
    # Add features inplace
    result = add_date_features(df, features=['year', 'month'], inplace=True)
    
    # Check that the original dataframe was modified
    assert 'date_year' in df.columns
    assert 'date_month' in df.columns
    
    # Check that the function returns the modified dataframe
    assert id(result) == id(df)


def test_add_date_features_custom_column():
    """Test adding date features with a custom column name."""
    # Create a sample dataframe
    df = pd.DataFrame({
        'custom_date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'value': [10, 20, 30, 40, 50]
    })
    
    # Add features with custom column name
    result = add_date_features(df, date_column='custom_date', features=['year', 'month'])
    
    # Check that the features use the custom column name prefix
    assert 'custom_date_year' in result.columns
    assert 'custom_date_month' in result.columns


def test_add_date_features_errors():
    """Test error handling in add_date_features."""
    # Create a sample dataframe without a date column
    df = pd.DataFrame({
        'not_date': [1, 2, 3],
        'value': [10, 20, 30]
    })
    
    # Test error when column doesn't exist
    with pytest.raises(ValueError, match="not found in the DataFrame"):
        add_date_features(df)
    
    # Test error with invalid feature
    df_with_date = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=3, freq='D')
    })
    with pytest.raises(ValueError, match="Invalid features"):
        add_date_features(df_with_date, features=['invalid_feature'])


def test_add_date_features_string_conversion():
    """Test conversion of string date column to datetime."""
    # Create a dataframe with string dates
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'value': [10, 20, 30]
    })
    
    # Add date features
    result = add_date_features(df, features=['year', 'month'])
    
    # Check that conversion worked
    assert result['date_year'].iloc[0] == 2023
    assert result['date_month'].iloc[0] == 1 