# ZiMuZuCrawler
A web crawler for you to automatically check-in and download latest TV series from zimuzu.tv

Before start:

1. Check if you have Python 3 installed. If not, you can use homebrew to install it:

brew intall Python3

2. Check if you have BeautifulSoup4 installed. If not, you can use pip3 to install it:

pip3 install beautifulsoup4

3. Check if you have requests installed. If not, you can use pip3 to install it:

pip3 install requests

4. Create a file named ZiMuZuHistory under the same directory of ZiMuZuCrawler.py, to allow it to store the shows downloaded (only the latest version will be recorded).

5. Change the 'account' and 'password' in the ZiMuZuCrawler.py to your own.


Recommendations:

1. You can run it directly in terminal with: Python3 ZiMuZuCrawler.py or

2. Use Crontab to run it automatically, for example:

	  45 7-8,19-21 * * * /usr/local/bin/Python3 /Users/.../ZimuZu/zimuzu.py >> /Users/.../ZiMuZu/dialog.log
	
Remember using absolute path in Crontab.

Donation:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/DonggeLiu)




