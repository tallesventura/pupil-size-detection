# pupil-size-detection

#Description
This project aims to automate part of the process of pupil detection and pupil area measurement that is used for detecting some diseases such as alzheimer and the use of cocaine. For each patient, the input is a set of videos with different combinations of light intensity and frequency each. For each video, one frame is captured and saved every x seconds and then the baseline area is calculated using the first x samples of the video. For each image, the percentage of baseline area is calculated using the found baseline area. The output is a graph of percentage of baseline area vs time containing all the different light exposures (see here).

The different steps of the process are usually done using a set of different tools. Some of then are very time consuming and require a lot of human assistance. This project aims to centralize the steps in one app and automate most of the steps in order to decrease the time needed to complete the process as well as simplifying it.

#Dependencies
In order to the application to run, your computer has to have the following packages installed:
* Anaconda Python 3.5 distribution
* OpenCV3 Python library

The Anaconda Python 3.5 distribution can be downloaded [here](https://www.continuum.io/downloads). Choose the version according to your Operating System.  
After you have installed Anaconda, you need to install the OpenCV3 package into your Anaconda environment. It has to be installed via command line. You can follow the steps bellow according to the operating system you are using.

##Windows
1 - Open a command prompt window, you can do that by either searching for `command prompt` on the search box or by pressing 'windows buttom + R'. When you do that a window with a text box will pop up. Type `cmd` on it and press Enter.

2 - Type ```conda install -c menpo opencv3=3.1.0``` and press Enter


##Mac
1 - Open a command line terminal window, you can do that by pressing 'command + space' and then searching for 'terminal'. Select the 'terminal' application.

2 - Type ```conda install -c menpo opencv3=3.1.0``` and press Enter

##Linux
1 - Open the default terminal 

2 - Type ```conda install -c menpo opencv3=3.1.0``` and press Enter

#Wiki
The wiki page can be accessed [here](https://github.com/tallesventura/pupil-size-detection/wiki)

#Contributors
##Developers
Talles Alves - <https://github.com/tallesventura>  
Marcos Motta - <https://github.com/marcosfmmota>  
Arnaldo Sales - <https://github.com/arnaldosales>  
##Other
Dr. Mark Albert, from Loyola University Chicago, Department of Computer Science  
Dr. Bruce Gaynes, from Loyola University Chicago  
Adnaan Zaffer

