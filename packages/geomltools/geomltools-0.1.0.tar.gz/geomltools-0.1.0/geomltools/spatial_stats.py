import numpy as np
from scipy.stats import norm
from scipy.spatial.distance import cdist


def calculate_pvalue(observed_statistic, shuffled_statistics):
    """
    Calculate the p-value of an observed statistic using shuffled statistics.
    
    Parameters:
        observed_statistic (float): The observed value of the statistic.
        shuffled_statistics (np.array): Array of statistics calculated from shuffled data.
    
    Returns:
        pvalue (float): The p-value.
    """
    # Calculate the p-value using SciPy's percentileofscore
    z_score = (observed_statistic - np.array(shuffled_statistics).mean() ) / np.array(shuffled_statistics).std()
    p_value = 2 * (1 - norm.cdf(np.abs(z_score)))
    return p_value

def permutation_test(sdf, variable, observed_statistic, statistic_function, n_permutations=99, **kwargs):
    """
    Perform a permutation test to calculate the statistical significance of a spatial statistic.
    
    Parameters:
        sdf (pd.DataFrame): Spatially Enabled DataFrame with a 'SHAPE' column.
        variable (str): Name of the variable to analyze.
        observed_statistic (float): The observed value of the statistic.
        statistic_function (callable): Function to calculate the spatial statistic.
        n_permutations (int): Number of permutations (default: 999).
        **kwargs: Additional keyword arguments to pass to the statistic_function.
    
    Returns:
        pvalue (float): The p-value.
        shuffled_statistics (np.array): Array of statistics from shuffled data.
    """
    # Initialize an array to store shuffled statistics
    shuffled_statistics = np.zeros(n_permutations)
    
    # Perform permutations
    for i in range(n_permutations):
        # Shuffle the variable values while keeping the spatial structure intact
        shuffled_values = np.random.permutation(sdf[variable].values)
        shuffled_sdf = sdf.copy()
        shuffled_sdf[variable] = shuffled_values
        
        # Calculate the statistic for the shuffled data
        shuffled_statistics[i] = statistic_function(shuffled_sdf, variable, **kwargs)
    
    # Calculate the p-value
    pvalue = calculate_pvalue(observed_statistic, shuffled_statistics)
    
    return pvalue, shuffled_statistics

def spatial_variance_ratio(sdf, variable, max_distance=10000):
    """
    Calculate the Spatial Variance Ratio (SVR) using a grid-based approach.
    
    Parameters:
        sdf (pd.DataFrame): Spatially Enabled DataFrame with a 'SHAPE' column.
        variable (str): Name of the variable to analyze.
        max_distance (float): Size of the grid cells (default: 10000).
    
    Returns:
        svr (float): Spatial Variance Ratio.
    """
    # Create grid indices
    sdf['q'] = sdf['SHAPE'].apply(lambda shape: int(shape.x // max_distance))
    sdf['r'] = sdf['SHAPE'].apply(lambda shape: int(shape.y // max_distance))
    sdf['grid_id'] = sdf['q'].astype(str) + '_' + sdf['r'].astype(str)
    
    # Calculate local statistics
    local_stats = sdf.groupby('grid_id')[variable].agg(['count', 'mean', 'var']).reset_index()
    
    # Exclude empty grid cells
    local_stats = local_stats[local_stats['count'] > 0]
    
    # Calculate overall variance
    overall_variance = sdf[variable].var()
    
    # Calculate average local variance
    average_local_variance = local_stats['var'].mean()
    
    # Calculate Spatial Variance Ratio (SVR)
    svr = average_local_variance / overall_variance

    
    return svr

def morans_i(sdf, variable, max_distance=10000):
    """
    Calculate Moran's I for spatial autocorrelation using a grid-based approach.
    
    Parameters:
        sdf (pd.DataFrame): Spatially Enabled DataFrame with a 'SHAPE' column.
        variable (str): Name of the variable to analyze.
        max_distance (float): Maximum distance for spatial weights (default: 10000).
    
    Returns:
        I (float): Moran's I statistic.
    """
    # Extract coordinates
    coords = np.array(sdf['SHAPE'].apply(lambda shape: (shape.x, shape.y)).tolist())
    
    # Calculate pairwise distances
    distances = cdist(coords, coords, metric="euclidean")
    
    # Create binary spatial weights matrix
    W = (distances <= max_distance).astype(int)
    np.fill_diagonal(W, 0)  # Exclude self-neighbors
    
    # Row-standardize the weights matrix
    row_sums = W.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    W_std = W / row_sums[:, np.newaxis]
    
    # Extract the variable values
    X = np.array(sdf[variable])
    n = X.shape[0]
    
    # Handle edge case where all values are identical
    X_std = np.std(X)
    if X_std == 0:
        raise ValueError("All values are identical. Moran's I cannot be calculated.")
    
    # Calculate Moran's I
    X_mean = np.mean(X)
    X_diff = X - X_mean
    numerator = np.sum(W_std * np.outer(X_diff, X_diff))
    denominator = np.sum(X_diff ** 2)
    S0 = np.sum(W_std)
    I = (n / S0) * (numerator / denominator)
    
    return I