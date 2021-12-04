This code is designed to handle raw data output by the labView code I have written for taking acoustic data.

The new data is output as a single raw file that contains multipe set of repeated data over the same time points.

Instead of trying to average these data points in real time (LabView is clunky and I am not well versed in this),
I just export a single file containing all repeatd data. This code will then seperate and average these data points
so that each time point will now have a unique data point associated with it.
