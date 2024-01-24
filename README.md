# Indeed Job Scraper
A Python scraper built with the Scrapy framework to extract product listings from the [Jumia store](https://www.jumia.com.ng/). 
The scraper utilizes Scrapy Pipelines for data processing, calculates discount percentages, cleans data, and stores it in MongoDB. 

A FastAPI-based API service was built around this project for customized product retrieval. Check it [HERE](https://github.com/Eben001/jumia_service)

### Features
- Scrapes product listings from Jumia store.
- Extract product detail such as product rating, seller score, discount percentge etc.
- Utilizes Scrapy Pipelines to drop duplicate items.
- Calculates discount percentage and cleans data.
- Stores data in MongoDB on the cloud.
- FastAPI-based API service for customized product retrieval.

### Installation
1. Ensure you have Python 3.x installed. Use the following command to install the required dependencies:
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
This above command will install the requirements from the requirements.txt file

### Usage
Setting up MongoDB.
- Create a MongoDB Atlas Account: If you don't have a MongoDB Atlas account, sign up for one [HERE](https://account.mongodb.com/account/login).
- Create a Cluster:
After logging in, create a new project.
Build a cluster within the project. Choose the default settings or customize them according to your preferences.
- Get Your MongoDB URI: Once the cluster is ready, click on "Connect" and then "Connect your application."
Copy the connection string (URI) provided. This string will be used to connect your scraper to the MongoDB database.

## Configuring the Scraper
- Clone the Repository:
   ```bash
    git clone https://github.com/Eben001/JumiaDiscountScraper-v1.git

- Install Dependencies:
  ```bash
    pip install -r requirements.txt

Update settings.py:
- Open the jumia_discount_scraper_v1/settings.py file.
- Locate the MONGO_URI variable.
Replace the existing placeholder with the MongoDB URI you obtained earlier.
  ```bash
  # jumia_discount_scraper_v1/settings.py
    MONGO_URI = 'your_mongo_uri_here'

- Run the Scraper:
  ```bash
  scrapy crawl spider_name

## Deploying to Zyte (formerly Scraping Hub)
Follow this [GUIDE](https://docs.zyte.com/web-scraping/tutorial/cloud.html) to deploy to Zyte


Feel free to adapt the content further based on your project's specific details or requirements.
Use it responsibly.
