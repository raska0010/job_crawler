# Culture Jobs Search

I've created this scraper when I was still looking for jobs in the culture industry which can be tedious sometimes. There are only a couple of small websites that pusblish job ads and as there are not that many jobs in the area new ads aren't published for a while.

The scraper visits the respective pages and extracts the relevant data, i.e. the title and short description of the job ad and the link to the full ad. It then creates an html file containing the ad text and the link.

For now, the scraper returns only jobs in Köln and Bonn as these are the areas that I was interested in.

I plan to include a feature that will only return jobs that have been published since the last search.

The packages I use are: Beautiful Soup, Regular Expression and Request.

