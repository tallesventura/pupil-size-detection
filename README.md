# pupil-size-detection

This project aims to automate part of the process of pupil detection and pupil area measurement that is used for detecting some diseases such as alzheimer and the use of cocaine.
For each patient there are 4 videos with diferent combinations of light intensity and frequency each. For each video samples are taken and saved every x given seconds. The baseline area is calculated using the first x samples of the corresponding video. For each image the percentage of baseline area is calculated using the found baseline area, then a graph of percentage of baseline area vs time is plotted.

The different steps of the process were done using different tools, and some of then were very time consuming and required a lot of human assistance. This project aims to centralize the steps in one app and automate most of the steps in order to decrease the time needed to complete the process.
