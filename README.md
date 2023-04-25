This is a hacky project to scrape data from rightmove and annotate with useful travel information.

Data is scraped, and a workflow is used to compute journey times and publish the web app and journey times content to github pages.

## Scraping

Scraping is done by Browse AI, data is pulled using the REST API.

## journeys/

Python code to processing the CSV data resulting from scrapestorms run into relevant details, compute journey times to configured destinations and output the annotated data.

Run `python journeys.py` to turn apartments.csv into output.json. Note the local caching used here means subsequent runs require fewer requests.

Note you will need to configure the following environment variables:

```
export CITYMAPPER_API_KEY=...
export GOOGLE_MAPS_API_KEY=...
export BROWSE_AI_API_KEY=...
export BROWSE_AI_ROBOT_ID=...
```

## frontend/

Vue.js/veutify frontend to view the sorted lists of apartments.

To test locally, build the output.json file and copy to rm-cm-frontend/public, then run:

```
yarn dev
```
