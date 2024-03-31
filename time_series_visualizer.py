# IMPORTING MODULES AND DATA
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

"""
    -> In this file, we define three plotting functions 
    -> The first draw_line_plot <- this creates a line plot of the data 
    -> The second is draw_bar_plot <- this creates a bar plot 
    -> The third is draw_box_plot <- This creates a box plot 
    -> Modules are first imported 
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importing data and parsing dates, setting index column to 'date'
"""
    -> This section of code imports file data
    -> We are provided this data in a CSV file 
    -> This contains a time series for the number of page views to a given webpage 
    -> We read this CSV data using the pandas .read_csv() method and store it in the `df` variable 
    -> The data in the "date" column is then converted into a datetime type, using the pandas .to_datetime method <- we are converting 
        them into daytime objects 
    -> We change the index of this to "date" using the .sex_index pandas method so that it can be queried based on dates  
    -> We then remove outliers from the data <- we are removing extreme datapoints, either which fall above the 97.5th percentile 
        or below the 0.025th percentile in the set 
"""
df = pd.read_csv("./fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Cleaning data by removing outliers
df = df[(df["value"] > df["value"].quantile(0.025)) & (df["value"] < df["value"].quantile(0.975))]

# DEFINING LINE PLOT FUNCTION
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
	-> This block of code is a plotting function which produces a line plot for the data
	-> Subplots are first setup and stored in the `fig` and `ax` variables 
	-> Axis labels are then set for the x, y axes and title of the plot
	-> The plot is then created using the sns lineplot method 
	-> We set the date for this equal to the data stored in the data frame previously imported in
	-> The function then returns the figure in `fig`
"""

def draw_line_plot():
    # Drawing line plot
    fig, ax = plt.subplots(figsize=(16, 5), dpi=100)
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    sns.lineplot(data=df, legend=False)

    # Saving image and returning fig
    fig.savefig('line_plot.png')
    return fig

# DEFINING THE BAR PLOT FUNCTION
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def draw_bar_plot():
    # Copying and modifying data for monthly bar plot
    df_bar = df.copy()
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    fig = df_bar.plot.bar(legend=True, figsize=(10, 10), xlabel="Years", ylabel="Average Page Views").figure
    plt.legend(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    # Saving image and returning fig
    fig.savefig('bar_plot.png')
    return fig

# DEFINING THE BOX PLOT FUNCTION
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def draw_box_plot():
    # Preparing data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Drawing box plots using Seaborn
    fig, axes = plt.subplots(1, 2, figsize=(16, 5), dpi=100)

    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_title("Year-wise Box Plot (Trend)")

    months_in_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=months_in_order, ax=axes[1])
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")

    # Saving image and returning fig
    fig.savefig('box_plot.png')
    return fig

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%