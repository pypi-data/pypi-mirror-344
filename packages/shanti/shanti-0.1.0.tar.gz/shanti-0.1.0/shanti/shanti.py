"""
create SHarable, interactive, stANdalone html dashboard from Tabular proteomIcs data

This library provides tools for loading proteomics data in Excel format and creating interactive
Bokeh visualizations with filtering capabilities.

No server or software installation is required to interact with dashboard.

Copyright: Nara Marella, CeMM, 2025.04.29

"""

import os
import pandas as pd
import numpy as np
from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, CustomJS, DataTable, TableColumn, RangeSlider, HoverTool, TapTool, BoxSelectTool, MultiSelect, LinearColorMapper, ColorBar, BasicTicker, Paragraph
from bokeh.models.widgets import TextInput, Button
from bokeh.layouts import column, row, gridplot, Spacer
from bokeh.embed import file_html
from bokeh.resources import CDN, INLINE


from scipy.stats import f as f_distribution


# Define the main module structure
class DataProcessor:
    """Internal class for processing Excel data and performing statistical calculations"""

    def __init__(self):
        """Initialize the data processor"""
        pass

    def get_s0(self, fc_lim=0.5, alpha=0.05, dfn=10, dfd=10, loc=0, scale=1, two_sided=False, **kwargs):
        """
        Calculates the s0 value given a log2 fold change limit and an alpha value.
        This is based on the two-tailed SAM test analysis transferred two F-test.

        Parameters
        ----------
        fc_lim : float or array of floats
            fold-change limit asymptote (x) in log2. Controls how far the threshold curve extends on x-axis.
        alpha : float or array of floats
            alpha threshold limit asymptote (y). Between 0 and 1. Controls significance threshold.
        dfn : float or array of floats
            degrees of freedom of nominator for the f-distribution. Higher values make curve steeper.
        dfd : float or array of floats
            degrees of freedom of denominator for the f-distribution. Higher values make curve steeper.
        loc : float or array of floats
            location parameter for the f-distribution. Controls horizontal shift of curve.
        scale : float or array of floats
            scaling parameter for the f-distribution. Controls vertical scaling of curve.
        two_sided : bool, optional
            if a two-sided test is performed. Default is False. When True, uses alpha/2 for threshold.
        **kwargs : dict, optional
            Additional keyword arguments not used directly but passed through function calls.

        Returns
        -------
        s0 : float
            fudge factor s0 that determines curvature of significance threshold
        """
        # Convert to vectorized form and check input
        fc_lim, alpha = np.asarray(fc_lim), np.asarray(alpha)
        if np.any((alpha < 0) | (alpha > 1)):
            raise ValueError(f'alpha value(s) must be between 0 and 1.')
        # Using the F = T**2 equality for 2 groups (max vs. min plateau), SAM analysis can be performed with f-distribution
        if two_sided:
            alpha_lim = np.sqrt(f_distribution.ppf(1 - (alpha / 2), dfn=dfn, dfd=dfd, loc=loc, scale=scale))
        else:
            alpha_lim = np.sqrt(f_distribution.ppf(1 - alpha, dfn=dfn, dfd=dfd, loc=loc, scale=scale))
        # Calculate S0 in vectorized form
        alpha_lim = np.asarray(alpha_lim)
        alpha_lim[alpha_lim < 0] = 0.0  # Guard against negative values
        s0 = abs(fc_lim) / alpha_lim
        return s0

    def map_fc_to_pvalue_cutoff(self, x, alpha=0.05, s0=1.45, dfn=10, dfd=10, loc=0, scale=1, two_sided=False, **kwargs):
        """
        This function maps input fold changes to the respective p-values given statistic type, chosen alpha value,
        fudge factor s0, and degrees of freedom. It is based on the SAM test with some modifications (see comments).

        Parameters
        ----------
        x : pd.Series
            log2 fold change values to map to p-value thresholds
        alpha : float
            alpha threshold limit asymptote (y). Between 0 and 1. Controls overall significance level.
        s0 : float
            fudge factor, which determines the transition between both fold-change and p-value asymptotes.
            Higher values create more curved threshold lines.
        dfn : int
            degrees of freedom of nominator for the f-distribution. Controls shape of threshold curve.
        dfd : int
            degrees of freedom of denominator for the f-distribution. Controls shape of threshold curve.
        loc : float
            location parameter for the f-distribution. Shifts threshold curve horizontally.
        scale : float
            scaling parameter for the f-distribution. Scales threshold curve vertically.
        two_sided : bool, optional
            if a two-sided test is performed. By default False. When True, results in symmetrical thresholds.
        **kwargs : dict, optional
            Additional keyword arguments not used directly.

        Returns
        -------
        y : pd.Series
            p-value cutoffs for each input log2-fold change x-value.

        Comments
        --------
        Adapted from:
        https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/10.1002/pmic.201600132
        R Code in the supplement
        FPB addition: use the f_distribution for calculation of a f-statistic under assumption F = T**2 for two group analysis
        """

        # Added on 2025.04.17
        if not isinstance(x, pd.Series):
            x = pd.Series(x)  # Convert to pandas Series if not already


        if (len(x) == 0) or type(pd.Series([0])) is not pd.Series:
            raise ValueError(f'Fold change array needs to be a pd.Series object with at least 1 value.')
        if not 0 <= alpha <= 1:
            raise ValueError(f'Alpha value must be between 0 and 1, but it was {alpha}.')
        # Using the F = T**2 equality for 2 groups (max vs. min plateau infinity argument), SAM analysis can be performed with f-distribution
        if two_sided:
            alpha_lim = np.sqrt(f_distribution.ppf(1 - (alpha / 2), dfn=dfn, dfd=dfd, loc=loc, scale=scale))
        else:
            alpha_lim = np.sqrt(f_distribution.ppf(1 - alpha, dfn=dfn, dfd=dfd, loc=loc, scale=scale))

        # New positional limits with s0
        pos_lim = alpha_lim * s0  # Positive threshold limit
        neg_lim = -alpha_lim * s0  # Negative threshold limit

        # Mask with 0 edge case
        pos = x > pos_lim  # Mask for values above positive threshold
        neg = x < neg_lim  # Mask for values below negative threshold
        if pos_lim == neg_lim:
            pos = x >= pos_lim  # Special case when thresholds are equal

        # Calculate the fudge-modified values
        x_pos = x[pos]  # Values above positive threshold
        x_neg = x[neg]  # Values below negative threshold
        x_none = x[(~pos) & (~neg)]  # Values between thresholds (not significant)

        # Calculate modified statistics for positive threshold
        d_pos = x_pos / alpha_lim - s0
        d_pos = (s0 / d_pos)
        d_pos = alpha_lim * (1 + d_pos)

        # Calculate modified statistics for negative threshold
        d_neg = x_neg / (-alpha_lim) - s0
        d_neg = (s0 / d_neg)
        d_neg = alpha_lim * (1 + d_neg)

        # Calculate to p-values.
        # Revert to F-test with F = T**2
        # Log survival function to have more accurate p value calculations: - np.log10[(1 - dist.cdf(x, dfn, dfd))]
        y_pos = - f_distribution.logsf(d_pos**2, dfn=dfn, dfd=dfd, loc=loc, scale=scale) * np.log10(np.e)
        y_neg = - f_distribution.logsf(d_neg**2, dfn=dfn, dfd=dfd, loc=loc, scale=scale) * np.log10(np.e)
        if two_sided:
            # Two sided p values are multiplied by two: - np.log10[(1 - dist.cdf(x, deg)) * 2]
            y_pos -= np.log10(2)
            y_neg -= np.log10(2)

        # Combine arrays for output and ensure non-negative values and convert nan to max_prob as its the least likely (for the 0 edge case for d_p/n)
        y_none = np.full(shape=len(x_none), fill_value=np.inf)  # Non-significant values get inf
        y = pd.concat([pd.Series(y_neg, index=x_neg.index), pd.Series(y_none, index=x_none.index), pd.Series(y_pos, index=x_pos.index)])
        y = y.clip(lower=0, upper=None)  # Ensure no negative values
        y = y.replace(np.nan, max(y))  # Replace NaN with maximum value
        return y[x.index]  # Return in original order

    # Function to classify points based on p-value cutoff and fold-change
    def classify_point(self, row, l2fc_col, pAdj_col, fc_lim, **kwargs):
        """
        Classify and color data points based on significance thresholds

        Parameters
        ----------
        row : pandas.Series
            A row from the dataframe containing fold-change and p-value data
        l2fc_col : str
            Column name containing log2 fold change values
        pAdj_col : str
            Column name containing adjusted p-values (as -log10 values)
        fc_lim : float
            Fold-change limit threshold for significance
        **kwargs : dict, optional
            Additional keyword arguments not used directly

        Returns
        -------
        str
            Color code for the data point: 'lightgrey' for non-significant,
            'orange' for significantly downregulated, 'blue' for significantly upregulated
        """
        x = row[l2fc_col]  # Get log2 fold change value
        y = row[pAdj_col]  # Get -log10 adjusted p-value
        y_thresh = row["y_thresh"]  # Get threshold value for this point

        # Protect against invalid values
        if pd.isna(x) or pd.isna(y):
            return "lightgrey"
        if y < y_thresh:
            return "lightgrey"  # below threshold (not significant)
        elif x < -fc_lim:
            return "orange"  # significant downregulation
        else:
            return "blue"  # significant upregulation


def load_data(file_path, sheet_name=0, alpha = 0.05, dfn = 10, dfd = 10, loc = 0, scale = 1,   two_sided=False, fc_lim = 0.5, l2fc_col = '', pAdj_col = '', hist1_col = '', hist2_col = '', hist1_name='', hist2_name=''):

    """
    Load data from Excel file and return a ColumnDataSource with processed data.

    Parameters:
    -----------
    file_path : str
        Path to the Excel file containing proteomics data
    sheet_name : int or str, default 0
        Sheet to read from the Excel file, can be sheet number or name
    alpha : float or array of floats
        alpha threshold limit asymptote (y). Between 0 and 1. Controls significance cutoff.
    dfn : float or array of floats
        degrees of freedom of nominator for the f-distribution. Controls shape of threshold curve.
    dfd : float or array of floats
        degrees of freedom of denominator for the f-distribution. Controls shape of threshold curve.
    loc : float or array of floats
        location parameter for the f-distribution. Shifts threshold curve horizontally.
    scale : float or array of floats
        scaling parameter for the f-distribution. Scales threshold curve vertically.
    two_sided : bool, optional
        if a two-sided test is performed. Default is False. When True, uses alpha/2 for threshold.
    fc_lim : float or array of floats
        fold-change limit asymptote (x) in log2. Controls how far the threshold extends on x-axis.
    l2fc_col : str
        column name containing log2 fold change values, required for volcano plot x-axis
    pAdj_col : str
        column name containing adjusted P values, required for volcano plot y-axis
    hist1_col : str
        column name containing mean (or average of all replicates) for Knock-Out(or Treatment) protein abundance values (or normalized protein abundance values). This is usually the NUMERATOR column in the fold-change (or ratio) calculation. This data is used to draw first histogram plot in the dashboard
    hist2_col : str
        column name containing mean (or average of all replicates) for Control (or Wild Type) protein abundance values (or normalized protein abundance values). This is usually the DENOMINATOR column in the fold-change (or ratio) calculation. This data is used to draw first histogram plot in the dashboard
    hist1_name : str
        name for first histogram plot. Use the NUMERATOR condition in the fold-change (ratio)
    hist2_name : str
        name for first histogram plot. Use the DENOMINATOR condition in the fold-change (ratio)

    Returns:
    --------
    ColumnDataSource
        Bokeh ColumnDataSource object containing the processed data with additional columns for visualization
    """

    # Initialize the data processor
    dp = DataProcessor()

    # Read Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Calculate -log10 of adjusted p-values with a minimum clip to avoid infinity
    df["mlog10pAdj"] = -np.log10(df[pAdj_col].clip(lower=1e-300))

    # Perform Data Processing
    # 1. Calculate s0 for the threshold curve - controls curvature of significance threshold
    s0 = dp.get_s0(fc_lim=fc_lim, alpha=alpha, dfn=dfn, dfd=dfd, two_sided=two_sided)

    # 2. Calculate y_thresh values for the threshold curve - these define the significance boundary
    df["y_thresh"] = dp.map_fc_to_pvalue_cutoff(x=df[l2fc_col], alpha=alpha, s0=s0, dfn=dfn, dfd=dfd, loc=loc, scale=scale, two_sided=two_sided)

    # 3. create color column based on threshold curve - colors points by significance and direction
    df["color"] = df.apply(lambda row: dp.classify_point(row, l2fc_col, "mlog10pAdj", fc_lim), axis=1)

    # Convert to ColumnDataSource for Bokeh visualization
    source = ColumnDataSource(df)

    return source


def make_histogram(source=None, hist_col='', width=200, height=800, visible=False, tools="", toolbar_location=None, title="", x_axis_label='', y_axis_label='', min_border=0, **kwargs):
    """
    Create a horizontal histogram visualization for protein abundance data.

    Parameters:
    -----------
    source : ColumnDataSource
        Bokeh data source containing the protein data
    hist_col : str
        Column name containing the abundance values to plot in histogram
    width : int, default 200
        Width of the histogram plot in pixels
    height : int, default 800
        Height of the histogram plot in pixels
    visible : bool, default False
        Whether the histogram should be initially visible
    tools : str, default ""
        Bokeh tools to include with the plot (e.g., "pan,zoom")
    toolbar_location : str or None, default None
        Location of the toolbar (None, "above", "below", "left", "right")
    title : str, default ""
        Title for the histogram plot
    x_axis_label : str, default ''
        Label for the x-axis (horizontal axis showing count)
    y_axis_label : str, default ''
        Label for the y-axis (vertical axis showing bins)
    min_border : int, default 0
        Minimum border size around the plot in pixels
    **kwargs : dict
        Additional keyword arguments passed to the figure function

    Returns:
    --------
    tuple
        (figure, filtered_data, bin_edges_log, bottoms, bar_height) containing:
        - Bokeh figure object of the histogram
        - Filtered data used for histogram
        - Log2 bin edges for binning
        - Bottom positions for bars
        - Height of each bar
    """
    # Convert source data to DataFrame
    df = pd.DataFrame(source.data)
    data = df[hist_col].dropna()  # Remove NaN values
    data_filtered = data[data > 0]  # Filter out non-positive values for log transformation

    # Return early if no valid data
    if len(data_filtered) == 0:
        return None, None, None, None, None, None

    # Create log2 bins for better visualization of abundance data
    log2_data = np.log2(data_filtered)  # Transform to log2 scale
    bin_edges_log = np.linspace(log2_data.min(), log2_data.max(), 21)  # Create 20 bins in log space
    bin_edges = np.power(2, bin_edges_log)  # Convert back to original scale
    hist, _ = np.histogram(data_filtered, bins=bin_edges)  # Calculate histogram

    # Set up spacing for horizontal bars
    n_bins = len(hist)
    bar_height = 1  # Height of each bar
    bar_spacing = 0.2  # Space between bars

    # Calculate positions for bars
    bottoms = np.arange(n_bins) * (bar_height + bar_spacing)  # Bottom position of each bar
    tops = bottoms + bar_height  # Top position of each bar

    # Create figure with basic settings
    p = figure(width=width, height=height, visible=visible, tools=tools, toolbar_location=toolbar_location,
               title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label, min_border=min_border)

    # Create empty figure if no column selected
    if hist_col == "":
        print(hist_col, "is empty")
        return p, None, None, None, None

    if data_filtered is None:
        print("data is empty")
        return p, None, None, None, None

    # Configure figure visibility
    p.visible = True
    p.xaxis.visible = True
    p.yaxis.visible = True
    p.grid.visible = False
    p.outline_line_color = None

    # Create histogram data source
    source_hist = ColumnDataSource(data=dict(
        left=[0] * len(hist),  # All bars start at 0
        right=hist,  # Width of each bar is the count
        bottom=bottoms,  # Bottom position for each bar
        top=tops  # Top position for each bar
    ))

    # Add bars to the plot
    p.quad(left='left', right='right', bottom='bottom', top='top',
           source=source_hist, fill_color='lightgrey', line_color='white', alpha=0.4)

    # Configure plot ranges
    p.y_range.start = 0
    p.y_range.end = tops[-1] + (tops[0] - bottoms[0]) * 0.2  # Add headroom at the top

    # Set x-axis range
    x_max = max(hist) if len(hist) > 0 else 1
    p.x_range.start = 0
    p.x_range.end = x_max * 1.2  # Add padding for appearance

    # Calculate midpoints of bins for tick positions
    midpoints = bottoms + (bar_height / 2)

    # Create tick formatter for y-axis using bin values
    bin_centers_log = (bin_edges_log[:-1] + bin_edges_log[1:]) / 2  # Centers of log2 bins
    bin_labels = [f"{value:.2g}" for value in bin_centers_log]  # Format as text

    # Set custom y-axis ticks
    p.yaxis.ticker = midpoints  # Position ticks at bin midpoints
    p.yaxis.major_label_overrides = {midpoints[i]: bin_labels[i] for i in range(len(midpoints))}  # Custom labels

    # Optional: Adjust y-axis appearance
    p.yaxis.major_label_text_font_size = "8pt"

    return p, data_filtered, bin_edges_log, bottoms, bar_height

def create_interactive_dashboard(source, peptides_file=None, l2fc_col='', pAdj_col='', html_title="Shanti Tool", color_column="color", table_columns=None, peptide_columns=None, volcano_title='', volcano_tools="pan, box_zoom, wheel_zoom, tap, box_select, reset, save", output_path="dashboard.html", plot2=None, plot3=None, hist1_data_filtered=None, hist2_data_filtered=None, hist1_bin_edges_log=None, hist2_bin_edges_log=None, hist1_bottoms=None, hist2_bottoms=None, hist1_bar_height=None, hist2_bar_height=None, hist1_col='', hist2_col=''):
    """
    Create an interactive Bokeh dashboard with multiple linked plots and filters.

    Parameters:
    -----------
    source : ColumnDataSource
        Data source for the plots, containing processed proteomics data
    peptides_file : str, optional
        Path to Excel file containing peptide-level data
    l2fc_col : str
        Column name for x-axis in main volcano plot (log2 fold change)
    pAdj_col : str
        Column name for y-axis in main volcano plot (adjusted p-value)
    html_title : str, default "Shanti Tool"
        Title for the HTML page
    color_column : str, default "color"
        Column name to use for point colors in volcano plot
    table_columns : list, default None
        List of column names to display in the protein data table
    peptide_columns : list, default None
        List of column names to display in the peptide data table
    volcano_title : str, default ''
        Title for the volcano plot
    volcano_tools : str, default "pan, box_zoom, wheel_zoom, tap, box_select, reset, save"
        Tools to include with the volcano plot
    output_path : str, default "dashboard.html"
        Path to save the HTML dashboard
    plot2 : Bokeh figure, optional
        First histogram plot (treatment/KO condition)
    plot3 : Bokeh figure, optional
        Second histogram plot (control/WT condition)
    hist1_data_filtered : array-like, optional
        Filtered data for first histogram
    hist2_data_filtered : array-like, optional
        Filtered data for second histogram
    hist1_bin_edges_log : array-like, optional
        Log2 bin edges for first histogram
    hist2_bin_edges_log : array-like, optional
        Log2 bin edges for second histogram
    hist1_bottoms : array-like, optional
        Bottom positions for bars in first histogram
    hist2_bottoms : array-like, optional
        Bottom positions for bars in second histogram
    hist1_bar_height : float, optional
        Height of each bar in first histogram
    hist2_bar_height : float, optional
        Height of each bar in second histogram
    hist1_col : str, default ''
        Column name for first histogram data
    hist2_col : str, default ''
        Column name for second histogram data

    Returns:
    --------
    str
        Path to the created HTML file
    """

    # Create a filtered copy of the source data for interactive filtering
    filtered_source = ColumnDataSource(data=source.data)

    df = pd.DataFrame(source.data)
    # df.to_csv('output.tsv', sep='\t', index=False)  # Commented out data export

    # Load peptides data if provided
    peptides_df = None
    if peptides_file:
        peptides_df = pd.read_excel(peptides_file)
        # Ensure UniProtID column exists
        if 'UniProtID' not in peptides_df.columns:
            raise ValueError("Peptides file must contain a 'UniProtID' column")

    # Create peptides source if available
    peptides_source = None
    peptides_source_all = None
    peptides_table = None
    if peptides_df is not None:
        # Store the full peptides data
        peptides_source_all = ColumnDataSource(peptides_df)
        # print(f"Peptides DataFrame loaded with {len(peptides_df)} rows")
        # print(f"Peptides columns: {peptides_df.columns.tolist()}")

        # Check if UniProtID column exists and has valid data
        if 'UniProtID' in peptides_df.columns:
            # print(f"UniProtID column exists with {peptides_df['UniProtID'].count()} non-null values")
            # print(f"Sample UniProtID values: {peptides_df['UniProtID'].iloc[:3].tolist()}")

            # Check for semicolon-separated values
            has_semicolons = peptides_df['UniProtID'].str.contains(';').any()
            # print(f"UniProtID column contains semicolon-separated values: {has_semicolons}")
        else:
            print("WARNING: UniProtID column not found in peptides data!")

        # Use all columns if not specified
        if peptide_columns is None:
            peptide_columns = list(peptides_df.columns)  # Default to all columns if not specified
        else:
            # Define column widths in order (first column = 80px, second = 120px, etc.)
            peptide_column_widths = [60, 300, 70, 40, 30, 200, 40, 60]
            default_width = 10

            # Create table columns with specified widths
            peptide_table_columns = []
            for i, col in enumerate(peptide_columns):
                # Get width from the list or use default if index exceeds list length
                width = peptide_column_widths[i] if i < len(peptide_column_widths) else default_width
                peptide_table_columns.append(TableColumn(field=col, title=col, width=width))

        # Create empty source with only selected columns for filtered peptides
        empty_peptides_data = {col: [] for col in peptide_columns}
        peptides_source = ColumnDataSource(empty_peptides_data)

        # Create the peptides table with the prepared columns
        peptides_table = DataTable(source=peptides_source, columns=peptide_table_columns,
                              width=900, height=400, index_position=None)

    # Define hover tooltips for volcano plot
    tooltips = [
        ("UniProtID", "@UniProtID"),
        ("Gene", "@Gene"),
        ("Log2 Fold Change", f"@{l2fc_col}"),
        ("p Adjusted", f"@{pAdj_col}"),
        ("-log10pAdj", "@mlog10pAdj")
    ]

    # Create the main volcano plot
    plot1 = figure(
        height=800, width=400, title=volcano_title,
        x_axis_label="filter log2 fold change values", y_axis_label="Filter -log10 adjusted p-values",
        tools=volcano_tools, toolbar_location="below", visible=True)

    # Add hover tool with tooltips
    plot1.add_tools(HoverTool(tooltips=tooltips))

    # Add scatter points to volcano plot
    plot1.scatter(x=l2fc_col, y="mlog10pAdj", source=filtered_source, color="color", size=8,
                selection_color="green", nonselection_alpha=0.5)

    # Add threshold curve lines to the volcano plot
    ylim = df["mlog10pAdj"].max() + 0.25  # Maximum y-value with padding

    # Split curve data into left and right sides for smooth rendering
    curve_left = df[(df[l2fc_col] < 0) & (df["y_thresh"] <= ylim)].sort_values(by=l2fc_col)
    curve_right = df[(df[l2fc_col] > 0) & (df["y_thresh"] <= ylim)].sort_values(by=l2fc_col)

    # Draw the significance threshold curves
    plot1.line(curve_left[l2fc_col], curve_left["y_thresh"], line_width=1, color="black")
    plot1.line(curve_right[l2fc_col], curve_right["y_thresh"], line_width=1, color="black")

    # Create data sources for horizontal lines in histograms (for showing selected proteins)
    lines_source_plot2 = ColumnDataSource(data=dict(x0=[], x1=[], y=[], color=[]))
    lines_source_plot3 = ColumnDataSource(data=dict(x0=[], x1=[], y=[], color=[]))

    # Add segment renderers to histogram plots for selected proteins
    if plot2 is not None:
        plot2.segment(x0='x0', y0='y', x1='x1', y1='y', line_color='color', line_width=1, source=lines_source_plot2)

    if plot3 is not None:
        plot3.segment(x0='x0', y0='y', x1='x1', y1='y', line_color='color', line_width=1, source=lines_source_plot3)

    # Set up slider filters for data filtering
    sliders = []
    slider_titles = ["Filter X-axis (log2 fold change)", "Filter y-axis (-log10 adjusted p-value)"]
    i = 0

    # Create sliders for both X and Y axes
    for volcano_slider in [l2fc_col, pAdj_col]:
        # Calculate min/max values for slider range
        min_val = min(source.data[volcano_slider])
        max_val = max(source.data[volcano_slider])

        # Create RangeSlider with appropriate settings
        slider = RangeSlider(
            title=f"{slider_titles[i]}",
            start=min_val,
            end=max_val,
            value=(min_val, max_val),  # Initial value is full range
            step=(max_val - min_val) / 100,  # 100 steps across the range
            width=300
        )

        i = i + 1

        # Create a JavaScript callback for the slider to filter data based on slider values
        # This callback filters the data source based on the current slider range and updates the filtered source
        slider_callback = CustomJS(
            # Pass required data sources and controls to the callback
            args=dict(source=source, filtered=filtered_source, slider=slider, column=volcano_slider),
            code="""
            // Get the current slider values
            const min_val = slider.value[0];
            const max_val = slider.value[1];

            // Get the original data
            const data = source.data;
            const column_data = data[column];

            // Create new filtered data object
            const new_data = {};
            for (const key in data) {
                new_data[key] = [];
            }

            // Filter the data
            for (let i = 0; i < column_data.length; i++) {
                if (column_data[i] >= min_val && column_data[i] <= max_val) {
                    for (const key in data) {
                        new_data[key].push(data[key][i]);
                    }
                }
            }

            // Update the filtered source
            filtered.data = new_data;
            filtered.change.emit();
            """
        )

        # Connect the callback to the slider's value change event
        slider.js_on_change('value', slider_callback)
        # Add spacing between sliders for better UI layout
        sliders.append(Spacer(width=60))
        # Add the slider to the sliders collection
        sliders.append(slider)

    # Set up search functionality with text input and button
    # TextInput widget allows users to search by specified fields
    search_input = TextInput(title="Search by UniProtID, Description, Gene", width=370)
    # Button to trigger the search
    search_button = Button(label="Go", button_type="primary", width=100)

    # Create a JavaScript callback for the search functionality
    # This callback filters data based on search text across all fields
    search_callback = CustomJS(
        # Pass required data sources and controls to the callback
        args=dict(source=source, filtered=filtered_source, search_input=search_input),
        code="""
        // Get the search text
        const search_text = search_input.value.toLowerCase();

        // Get the original data
        const data = source.data;

        // If search is empty, restore all data
        if (search_text.trim() === '') {
            filtered.data = data;
            filtered.change.emit();
            return;
        }

        // Create new filtered data object
        const new_data = {};
        for (const key in data) {
            new_data[key] = [];
        }

        // Search across all string columns
        const columns = Object.keys(data);
        for (let i = 0; i < data[columns[0]].length; i++) {
            let match = false;

            // Check each column for a match
            for (const col of columns) {
                const val = String(data[col][i]).toLowerCase();
                if (val.includes(search_text)) {
                    match = true;
                    break;
                }
            }

            // If a match is found, add all data for this row
            if (match) {
                for (const key in data) {
                    new_data[key].push(data[key][i]);
                }
            }
        }

        // Update the filtered source
        filtered.data = new_data;
        filtered.change.emit();
        """
    )

    # Connect the search callback to the button's click event
    search_button.js_on_click(search_callback)

    # Create a data source for the table that will display only the selected points
    # This source will be populated when user selects data points
    selected_source = ColumnDataSource({col: [] for col in table_columns})

    # Initialize data table to None
    data_table = None
    # Create a data table only if table columns are provided
    if table_columns:

        # Define column widths to customize the table appearance
        # Each number represents width in pixels for the corresponding column
        column_widths = [75, 75, 400, 50, 50, 50]

        # Default width for columns that exceed the defined widths list
        default_width = 100

        # Create table columns with appropriate widths
        columns = []
        for i, col in enumerate(table_columns):
            # Get width from the list or use default if index exceeds list length
            width = column_widths[i] if i < len(column_widths) else default_width
            columns.append(TableColumn(field=col, title=col, width=width))

        # Create the data table with the configured columns
        # Parameters:
        #   source: The data source for the table
        #   columns: List of table columns
        #   width/height: Dimensions of the table in pixels
        #   index_position: Set to None to hide the index column
        data_table = DataTable(source=selected_source, columns=columns, width=800, height=400, index_position=None)

    # This CustomJS callback processes user selections in the filtered data source
    # and updates related visualizations and tables
    selection_callback = CustomJS(
            # Pass all required data sources and variables to the JS callback
            args=dict(
                # Data sources
                filtered_source=filtered_source,      # Contains filtered protein data
                selected_source=selected_source,      # Will hold data for selected items
                peptides_source=peptides_source,      # Contains peptide data for selected proteins
                peptides_source_all=peptides_source_all,  # Contains all peptide data

                # Column definitions
                table_columns=table_columns,          # Columns for the protein data table
                peptide_columns=peptide_columns,      # Columns for the peptide data table

                # Plot references
                plot2=plot2,                          # Histogram plot 1
                plot3=plot3,                          # Histogram plot 2

                # Line sources for visual indicators on plots
                lines_source_plot2=lines_source_plot2,  # Lines to highlight selected items on plot2
                lines_source_plot3=lines_source_plot3,  # Lines to highlight selected items on plot3

                # Histogram 1 data
                hist1_data=hist1_data_filtered,       # Data for histogram 1
                hist1_bin_edges=hist1_bin_edges_log,  # Bin edges for histogram 1 (log scale)
                hist1_bottoms=hist1_bottoms,          # Bottom positions for histogram 1 bars
                hist1_bar_height=hist1_bar_height,    # Height of bars in histogram 1
                hist1_col=hist1_col,                  # Column name for histogram 1 data

                # Histogram 2 data
                hist2_data=hist2_data_filtered,       # Data for histogram 2
                hist2_bin_edges=hist2_bin_edges_log,  # Bin edges for histogram 2 (log scale)
                hist2_bottoms=hist2_bottoms,          # Bottom positions for histogram 2 bars
                hist2_bar_height=hist2_bar_height,    # Height of bars in histogram 2
                hist2_col=hist2_col                   # Column name for histogram 2 data
            ),
            code="""
            (function() {
                console.log("Selection callback triggered");

                var indices = filtered_source.selected.indices;
                console.log("Selected indices:", indices);

                var lines_data_plot2 = {x0: [], x1: [], y: [], color: []};
                var plot2_max_x = plot2.x_range.end;

                var lines_data_plot3 = {x0: [], x1: [], y: [], color: []};
                var plot3_max_x = plot3.x_range.end;

                var new_data = {};
                for (var i = 0; i < table_columns.length; i++) {
                    new_data[table_columns[i]] = [];
                }

                var selected_uniprotids = [];

                for (var i = 0; i < indices.length; i++) {
                    var idx = indices[i];

                    for (var j = 0; j < table_columns.length; j++) {
                        var key = table_columns[j];
                        new_data[key].push(filtered_source.data[key][idx]);
                    }

                    if ('UniProtID' in filtered_source.data) {
                        var uid = filtered_source.data['UniProtID'][idx];
                        if (selected_uniprotids.indexOf(uid) === -1) {
                            selected_uniprotids.push(uid);
                        }
                    }

                    if (filtered_source.data[hist1_col] && filtered_source.data[hist1_col][idx] > 0) {
                        var val1 = filtered_source.data[hist1_col][idx];
                        var log_val1 = Math.log2(val1);
                        for (var k = 0; k < hist1_bin_edges.length - 1; k++) {
                            if (log_val1 >= hist1_bin_edges[k] && log_val1 < hist1_bin_edges[k + 1]) {
                                var bin_bottom1 = hist1_bottoms[k];
                                var rand_offset1 = Math.random() * hist1_bar_height;
                                var y_pos1 = bin_bottom1 + rand_offset1;
                                lines_data_plot2.x0.push(0);
                                lines_data_plot2.x1.push(plot2_max_x);
                                lines_data_plot2.y.push(y_pos1);
                                lines_data_plot2.color.push('green');
                                break;
                            }
                        }
                    }

                    if (filtered_source.data[hist2_col] && filtered_source.data[hist2_col][idx] > 0) {
                        var val2 = filtered_source.data[hist2_col][idx];
                        var log_val2 = Math.log2(val2);
                        for (var k2 = 0; k2 < hist2_bin_edges.length - 1; k2++) {
                            if (log_val2 >= hist2_bin_edges[k2] && log_val2 < hist2_bin_edges[k2 + 1]) {
                                var bin_bottom2 = hist2_bottoms[k2];
                                var rand_offset2 = Math.random() * hist2_bar_height;
                                var y_pos2 = bin_bottom2 + rand_offset2;
                                lines_data_plot3.x0.push(0);
                                lines_data_plot3.x1.push(plot3_max_x);
                                lines_data_plot3.y.push(y_pos2);
                                lines_data_plot3.color.push('green');
                                break;
                            }
                        }
                    }
                }

                lines_source_plot2.data = lines_data_plot2;
                lines_source_plot2.change.emit();
                lines_source_plot3.data = lines_data_plot3;
                lines_source_plot3.change.emit();
                selected_source.data = new_data;
                selected_source.change.emit();

                console.log("Updating peptides table");

                if (!peptides_source_all || !peptides_source || !peptide_columns || !Array.isArray(peptide_columns)) {
                    console.error("Missing required peptides data sources or columns");
                    return;
                }

                if (!('UniProtID' in peptides_source_all.data)) {
                    console.error("UniProtID column not found in peptides data");
                    return;
                }

                var filtered_peptides = {};
                for (var i = 0; i < peptide_columns.length; i++) {
                    filtered_peptides[peptide_columns[i]] = [];
                }

                var matchCount = 0;
                var peptidesLength = peptides_source_all.data['UniProtID'].length;
                console.log("Total peptides rows to check:", peptidesLength);

                for (var i = 0; i < peptidesLength; i++) {
                    var peptide_uniprotid = peptides_source_all.data['UniProtID'][i];
                    if (typeof peptide_uniprotid !== 'string') {
                        continue;
                    }

                    var peptide_uniprotids = peptide_uniprotid.split(';');
                    var found = false;
                    for (var s = 0; s < selected_uniprotids.length; s++) {
                        var sel_uid = selected_uniprotids[s];
                        for (var p = 0; p < peptide_uniprotids.length; p++) {
                            if (peptide_uniprotids[p] === sel_uid) {
                                found = true;
                                break;
                            }
                        }
                        if (found) break;
                    }

                    if (found) {
                        matchCount++;
                        for (var j = 0; j < peptide_columns.length; j++) {
                            var key = peptide_columns[j];
                            if (key in peptides_source_all.data) {
                                filtered_peptides[key].push(peptides_source_all.data[key][i]);
                            } else {
                                filtered_peptides[key].push(null);
                                console.error("Column '" + key + "' not found in peptides_source_all.data");
                            }
                        }
                    }
                }

                console.log("Total peptide matches found: " + matchCount);

                var maxLength = 0;
                for (var i = 0; i < peptide_columns.length; i++) {
                    var key = peptide_columns[i];
                    if (filtered_peptides[key].length > maxLength) {
                        maxLength = filtered_peptides[key].length;
                    }
                }

                for (var i = 0; i < peptide_columns.length; i++) {
                    var key = peptide_columns[i];
                    while (filtered_peptides[key].length < maxLength) {
                        filtered_peptides[key].push(null);
                    }
                }

                peptides_source.data = filtered_peptides;
                peptides_source.change.emit();
                console.log("Peptides table update complete");
            })();
            """
        )

    """Attach the callback to the selection event"""
    # Connect the selection callback to the filtered_source's selection change event
    filtered_source.selected.js_on_change('indices', selection_callback);

    # Create the layout for the visualization
    # Add titles for the data tables
    data_table_title = Paragraph(text="Selected Protein(s)")
    peptides_table_title = Paragraph(text="Peptides of selected protein(s)")

    # Arrange sliders in a 2x2 grid
    sliders_col = column(row(sliders[0], sliders[1]), row(sliders[2], sliders[3]) )

    # Arrange search elements with spacers for layout
    filter_col =  column(row(Spacer(width=20), search_input), row(Spacer(width=20), search_button))

    # Create column layout for plot1 and sliders
    plot1_col = column(plot1, Spacer(height=20), sliders_col)

    # Place histogram plots side by side
    hist_plots = row(plot2, plot3)

    # Create column layout for histogram plots and filter components
    hist_plots_col = column(hist_plots, Spacer(height=20), filter_col)

    # Arrange data tables and their titles in a column
    tables_col = column(data_table_title, data_table, Spacer(height=20), peptides_table_title, peptides_table)

    # Combine all elements into the final layout
    # The layout is organized as: plots and histograms on the left, tables on the right
    layout = row(plot1_col, hist_plots_col, Spacer(width=20), tables_col)

    # Output to standalone HTML file
    # Parameters:
    #   output_path: Path where the HTML file will be saved
    #   html_title: Title for the HTML page
    #   mode='inline': Embeds all resources in the HTML file
    output_file(output_path, title=html_title, mode='inline')

    # Save the layout to the HTML file
    # INLINE resources parameter ensures all JavaScript and CSS is embedded in the HTML
    save(layout, resources=INLINE)

    return output_path
