## End To End Neural Network

Running Process:

1.  It scrapes the data for available houses to rent from "https://apartments.gaijinpot.com/en/rent" website (user can insert how many houses the wish to scrape)
2.  Save the scraped data in a Mongo database with dbname='apartments' and collection_name='apartment'
3.  Runs a Neural Network and saves the model.
4.  Runs a GUI to get user input and returns the prediction to the user.

# How to run
To install the libraries:      pip install -r requirements.txt
After installation:
Run the following command in the base directory of project:

*  python automation.py <number of items to scrape>   =>    python scrape 10000

This command initiates scraping andd scrape the number of items you have passed in it and save them all in a Mongo database, then it initiates the neural network model training, train and saves the model alongside the preprocessor object in a folder called "data", and lastly runs the GUI for user input and makes prediction based on the created model.

