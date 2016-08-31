ScrapyG
=======
ScrapyG uses Selenium and Scrapy in order to scrape information from the GH website.

To run, you will need to install Python, Scrapy and all  of its dependencies as mentioned in the <a href="http://doc.scrapy.org/en/latest/intro/install.html#intro-install">Scrapy Installation guide</a>. In addition, you will need Selenium and Selenium server. For help on installation, reference the <a href="http://selenium-python.readthedocs.org/installation.html">Selenium Python Documentation</a>. Lastly, Selenium will be working with Firefox, so you need to make sure that is installed on your computer as well.

Currently confirmed to be running on Selenium 2.53.6 & Firefox 46.0. (Prior versions of Firefox may not work due to the website's browser version control)

To run: first we must launch the <code>selenium.jar</code> file <b>in a separate command line window</b> (Have JDK installed & set as a PATH variable) using <code>java -jar selenium.jar</code>. This launches the Selenium standalone server. Then, initiate the spider in the second command line window by typing <code>scrapy crawl gh -o [filename].csv -t csv</code> in the root directory.

Note... If it becomes necessary to shut down the Selenium server, simply type into the browser:

<code>http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer</code>

Phantomjs can be used for headless testing by launching <code>phantomjs --webdriver=4444</code> after it is installed and located in <code>PATH</code>.
