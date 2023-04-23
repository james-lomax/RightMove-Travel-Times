This is a hacky project to scrape data from rightmove and annotate with useful travel information.

## Scraping

Scraping is done by scrapestorm, outputting a CSV file.

## journeys/

Python code to processing the CSV data resulting from scrapestorms run into relevant details, compute journey times to configured destinations and output the annotated data.

Run `python journeys.py` to turn apartments.csv into output.json. Note the local caching used here means subsequent runs require fewer requests.

## frontend/

Vue.js/veutify frontend to view the sorted lists of apartments.

Start web server to provide outputs.json:

```
cd journeys
python cors_server.py 3095
```

Then run with:

```
yarn dev
```
