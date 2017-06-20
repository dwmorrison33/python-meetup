1. I recommend that you download Python3 and Google Chrome for this Meetup https://www.google.com/chrome/browser/desktop/index.html

2. You will need the chromedriver for Selenium to work properly..Download at https://chromedriver.storage.googleapis.com/index.html?path=2.30/
Please download the correct .zip file for the operationg system that you have...

3. You will need to unzip that file in your download folder...Once you have done this, please make note of your directory with the command pwd
You will need that path for the scripts that we execute.

4. Go to your terminal and change directory to your Desktop, and execute pip3 install virtualenv
5. You want to create a virtual environment by: virtualenv myvirtualenv/python_meetup
6. Next activate your virtual environment, type source myvirtualenv/python_meetup/bin/activate

7. You will want to clone this project to whatever directory of your choice. To keep things simple, I recommend your desktop.
8. cd into project and install the necessary packages with pip -R install requirements.txt

9. Lastly, you will need to change the directory in python_meetup_scraper.py, python_meetup_scraper2.py, and selenium_test_scraper.py
from driver = webdriver.Chrome("/Users/davidmorrison/Downloads/chromedriver") to where you downloaded the chromedriver in step 3.

With that you should be able to execute these scripts prior to class, but if you are still having trouble, dont worry someone can help
at the meetup.

