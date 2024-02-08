## End To End Neural Network

Running Process:

1.  It scrapes the data for available houses to rent from "https://apartments.gaijinpot.com/en/rent" website (user can insert how many houses the wish to scrape)
2.  Save the scraped data in a Mongo database with dbname='apartments' and collection_name='apartment'
3.  Runs a Neural Network and saves the model.
4.  Runs a GUI to get user input and returns the prediction to the user.


