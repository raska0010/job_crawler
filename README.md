# Culture Jobs Search

I've created this scraper when I was still looking for jobs in the culture industry which can be tedious sometimes. There are only a couple of small websites that pusblish job ads and as there are not that many jobs in the area new ads aren't published for a while.

The scraper visits the respective pages and extracts the relevant data, i.e. the title and short description of the job ad and the link to the full ad. It then stores the new entries in a postgres data base. For now it also returns the latest search results via the command line. In the future I plan to use Django to transform the scraper into a web application that allows to search the job entries by date.

For now, the scraper returns only jobs in Köln and Bonn as these are the areas that I was interested in.

The packages I use are: Beautiful Soup, Regular Expression, Request and SQLalchemy.

