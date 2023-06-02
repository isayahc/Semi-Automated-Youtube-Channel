import os
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import pandas as pd
import datetime
from typing import List, Optional

def validate_inputs(keywords: List[str], timeframe: str) -> None:
    """
    Validate the inputs for the get_trends function.

    Parameters
    ----------
    keywords : list of str
        List of keywords to get trends data for.
    timeframe : str
        Timeframe for the trends data.
    """
    if not isinstance(keywords, list):
        raise ValueError("Keywords should be a list of strings.")
    
    valid_timeframes = ['now 1-H', 'now 4-H', 'now 1-d', 'now 7-d', 'today 1-m', 'today 3-m', 'today 12-m', 'today 5-y', 'all']
    if timeframe not in valid_timeframes:
        raise ValueError("Invalid timeframe. Check the Google Trends API for valid timeframes.")

def get_trends(keywords: List[str], timeframe: str = 'today 5-y') -> pd.DataFrame:
    """
    Get Google Trends data for a list of keywords.

    Parameters
    ----------
    keywords : list of str
        List of keywords to get trends data for.
    timeframe : str, optional
        Timeframe for the trends data, defaults to 'today 5-y'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with the trends data.
    """
    validate_inputs(keywords, timeframe)
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
    trend_data = pytrends.interest_over_time()
    return trend_data

def plot_trends(trend_data: pd.DataFrame, save: bool = False, filename: Optional[str] = None) -> None:
    """
    Plot Google Trends data.

    Parameters
    ----------
    trend_data : pandas.DataFrame
        DataFrame with the trends data.
    save : bool, optional
        Whether to save the plot as a PNG image, defaults to False.
    filename : str, optional
        Filename for the PNG image, defaults to None.
    """
    plt.figure(figsize=(14, 8))
    for keyword in trend_data.columns[:-1]:  # Exclude the 'isPartial' column
        plt.plot(trend_data.index, trend_data[keyword], label=keyword)
    plt.xlabel('Date')
    plt.ylabel('Trends Index')
    plt.title('Google Search Trends over time')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    if save:
        if filename is None:
            # Create filename with current datetime if not specified
            filename = f"graph_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(filename, format='png')  # Save the plot as a PNG image

def main() -> None:
    """
    Main function to get and plot Google Trends data.
    """
    # List of keywords to get trends data for
    keywords = ['Blockchain', 'pizza', 'Australian Cattle Dog','AI',"Chinese Food"]

    # Get the trends data
    trend_data = get_trends(keywords)

    # Plot the trends data
    plot_trends(trend_data)

if __name__ == "__main__":
    main()
