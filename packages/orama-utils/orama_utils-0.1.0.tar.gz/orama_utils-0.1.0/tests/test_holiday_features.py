"""
Tests for the holiday features module.
"""

import pytest
import pandas as pd
from orama_utils.holiday_features import add_holiday_features

def test_add_holiday_features_basic():
    """Test basic functionality with Spanish holidays."""
    # Create test data
    df = pd.DataFrame({
        'date': ['2019-01-01', '2019-01-06', '2019-02-28'],
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-MD', 'ES-MD', 'ES-AN']
    })
    
    # Apply holiday features
    result = add_holiday_features(df)
    
    # Check results
    assert result['is_public_holiday'].tolist() == [True, True, False]
    assert result['is_local_holiday'].tolist() == [False, False, True]
    assert result['many_counties_holiday'].tolist() == [False, False, False]

def test_add_holiday_features_italy():
    """Test handling of Italian holidays (currently empty)."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['IT'],
        'county': ['IT-25']
    })
    
    result = add_holiday_features(df)
    assert not result['is_public_holiday'].iloc[0]
    assert not result['is_local_holiday'].iloc[0]
    assert not result['many_counties_holiday'].iloc[0]

def test_add_holiday_features_mixed_countries():
    """Test handling of mixed country codes."""
    df = pd.DataFrame({
        'date': ['2019-01-01', '2019-01-01'],
        'country': ['ES', 'IT'],
        'county': ['ES-MD', 'IT-25']
    })
    
    result = add_holiday_features(df)
    assert result['is_public_holiday'].tolist() == [True, False]

def test_add_holiday_features_invalid_country():
    """Test error handling for invalid country codes."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['FR'],  # Invalid country code
        'county': ['FR-01']
    })
    
    with pytest.raises(ValueError, match=r"Invalid country codes found:.*"):
        add_holiday_features(df)

def test_add_holiday_features_missing_columns():
    """Test error handling for missing required columns."""
    # Missing date column
    df1 = pd.DataFrame({
        'country': ['ES'],
        'county': ['ES-MD']
    })
    with pytest.raises(ValueError, match=r"Date column.*not found"):
        add_holiday_features(df1)
    
    # Missing country column
    df2 = pd.DataFrame({
        'date': ['2019-01-01'],
        'county': ['ES-MD']
    })
    with pytest.raises(ValueError, match=r"Country column.*not found"):
        add_holiday_features(df2)

def test_add_holiday_features_custom_column_names():
    """Test using custom column names."""
    df = pd.DataFrame({
        'fecha': ['2019-01-01'],
        'pais': ['ES'],
        'region': ['ES-MD']
    })
    
    result = add_holiday_features(
        df,
        date_column='fecha',
        country_column='pais',
        county_column='region'
    )
    assert result['is_public_holiday'].iloc[0]

def test_add_holiday_features_without_county():
    """Test functionality when county column is not provided."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['ES']
    })
    
    result = add_holiday_features(df)
    assert result['is_public_holiday'].iloc[0]
    assert not result['is_local_holiday'].iloc[0]

def test_add_holiday_features_county_threshold():
    """Test the county threshold functionality."""
    df = pd.DataFrame({
        'date': ['2019-04-18'],  # Maundy Thursday - many regions
        'country': ['ES'],
        'county': ['ES-MD']
    })
    
    # Test with default threshold (3)
    result1 = add_holiday_features(df)
    assert result1['many_counties_holiday'].iloc[0]
    
    # Test with higher threshold
    result2 = add_holiday_features(df, county_threshold=10)
    assert result2['many_counties_holiday'].iloc[0]
    
    # Test with very high threshold
    result3 = add_holiday_features(df, county_threshold=20)
    assert not result3['many_counties_holiday'].iloc[0]

def test_add_holiday_features_invalid_threshold():
    """Test error handling for invalid county threshold."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['ES'],
        'county': ['ES-MD']
    })
    
    with pytest.raises(ValueError, match="county_threshold must be a positive integer"):
        add_holiday_features(df, county_threshold=0)
    
    with pytest.raises(ValueError, match="county_threshold must be a positive integer"):
        add_holiday_features(df, county_threshold=-1) 