#!/usr/bin/env bash
# Auto-Generated .sh files from the original .md by Sparkle 0.8.8

## Algorithm Selection

# Sparkle also offers various tools to apply algorithm selection, where we, given an objective, train another algorithm to determine which solver is best to use based on an instance. 

# These steps can also be found as a Bash script in `Examples/selection.sh`

### Initialise the Sparkle platform

sparkle initialise

### Add instances
# First, we add instance files (in this case in CNF format) to the platform by specifying the path.

sparkle add instances Examples/Resources/Instances/PTN/

### Add solvers

# Now we add solvers to the platform as possible options for our selection. Each solver directory should contain the solver wrapper.

sparkle add solver Examples/Resources/Solvers/CSCCSat/
sparkle add solver Examples/Resources/Solvers/PbO-CCSAT-Generic/
sparkle add solver Examples/Resources/Solvers/MiniSAT/

### Add feature extractor
# To run the selector, we need certain features to represent our instances. To that end, we add a feature extractor to the platform that creates vector representations of our instances.


sparkle add feature extractor Examples/Resources/Extractors/SAT-features-competition2012_revised_without_SatELite_sparkle/

### Compute features
# Now we can run our features with the following command:

sparkle compute features

### Run the solvers
# Similarly, we can now also compute our objective values for our solvers, in this case PAR10. Note that we can at this point still specifiy multiple objectives by separating them with a comma, or denote them in our settings file.

sparkle run solvers --objective PAR10

### Construct a portfolio selector
# To make sure feature computation and solver performance computation are done before constructing the portfolio use the `wait` command

sparkle wait


# Now we can construct a portfolio selector, using the previously computed features and the results of running the solvers. The `--selector-timeout` argument determines for how many seconds we will train our selector for. We can set the flag `--solver-ablation` for actual marginal contribution computation later.

sparkle construct portfolio selector --selector-timeout 1000 --solver-ablation
sparkle wait  # Wait for the constructor to complete its computations

### Generate a report

# Generate an experimental report detailing the experimental procedure and performance information; this will be located at `Output/Selection/Sparkle_Report.pdf`

sparkle generate report

### Run the portfolio selector

#### Run on a single instance

# Run the portfolio selector on a *single* testing instance; the result will be printed to the command line

sparkle run portfolio selector Examples/Resources/Instances/PTN2/plain7824.cnf

### Run on an instance set

# Run the portfolio selector on a testing instance *set*

sparkle run portfolio selector Examples/Resources/Instances/PTN2/
sparkle wait  # Wait for the portfolio selector to be done running on the testing instance set

#### Generate a report including results on the test set

# Generate an experimental report that includes the results on the test set, and as before the experimental procedure and performance information; this will be located at `Output/Selection/Sparkle_Report_For_Test.pdf`

sparkle generate report

# By default the `generate_report` command will create a report for the most recent instance set. To generate a report for an older instance set, the desired instance set can be specified with: `--test-case-directory Test_Cases/PTN2/`


### Comparing against SATZilla 2024

# If you wish to compare two feature extractors against one another, you need to remove the previous extractor from the platform (Or create a new platform from scratch) by running:

sparkle remove feature extractor SAT-features-competition2012_revised_without_SatELite_sparkle

# Otherwise, Sparkle will interpret adding the other feature extractor as creating a combined feature vector per instance from all present extractors in Sparkle. Now we can add SATZilla 2024 from the Examples directory
# Note that this feature extractor requires GCC (any version, tested with 13.2.0) to run.


sparkle add feature extractor Examples/Resources/Extractors/SAT-features-competition2024

# We can also investigate a different data set, SAT Competition 2023 for which Sparkle has a subset.

sparkle remove instances PTN
sparkle remove instances PTN2
sparkle add instances Examples/Resources/Instances/SATCOMP2023_SUB

# We compute the features for the new extractor and new instances.

sparkle compute features
sparkle wait  # Wait for it to complete before continuing

# Now we can train a selector based on these features.

sparkle construct portfolio selector --selector-timeout 1000
sparkle wait  #Wait for the computation to be done

# And generate the report. When running on the PTN/PTN2 data sets, you can compare the two to see the impact of different feature extractors.

sparkle generate report
