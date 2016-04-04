# Twitter Hashtag Graph - Average Connections
## Introduction
This repository will act as my submission to Insight Data Engineering's Coding Challenge. 

This challenge requires me to:

Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. I will thus be calculating the average degree over a 60-second sliding window. 

I have chosen to implement my solution using Python.

## Modules and Python Libraries
The following custom modules were used:

1. tweet.py
2. time_window.py
3. tools.py

These modules are found within the src/modules directory and are automatically linked to within the appropriate scripts. No efforts are required by the user.

The following Python libraries were utilized:

1. json
2. datetime
3. dateutil
4. sys



## Installation and Running the Program

1. Clone the repository to your system
2. Load tweet.txt file into the tweet_input directory
3. To run the program, enter the following command from the main directory:  
  
   sh run.sh
4. The output will be stored to tweet_output/output.txt


## Tests

Simple tests can be found within the insight_testsuite directory witin the parent directory.

To run the tests, navigate to the insight_testsuite/ directory and enter the following command:
    sh run_tests.sh

To add new tests, create a new directory within the insight_testsuite/tests directory, making sure to include tweet_input and tweet_output directories within the new test directory. In the tweet_input directory, include a file titled "tweets.txt" that contains desired test tweet data. In the tweet_output directory, include a file titled "output.txt" with the correct sequence of outputs that will be checked against the output of your program.

Running run_tests.sh will yield PASS or FAIL to indicate the success of the test.






