# TriggerScraper #

`TriggerScraper` is a scraper to map out clusters of sites containing some trigger words. Built on top of `grab`.

## Requirements ## 

  1. `$ pip install pipenv`
  2. `$ brew install redis`

## Install ##

  1. `$ pipenv install`

## Run ##

  1. Run Redis locally: `$ redis-server` in a terminal window
  2. `$ pipenv run python scrape.py`

## Optional ##

  * Modify `common.py` with our triggerwords. By default it's some Swedish words strongly correlated with the alt-right strongly focused on immigration.

## Example ##

After some time, the scraper will have saved something like this to `current_findings.csv`:

```
    |  domain                                  |  ratio               |  triggered  |  n_links
----|------------------------------------------|----------------------|-------------|---------
6   |  http://avpixlat.info                    |  7.774193548387097   |  210        |  31
25  |  http://petterssonsblogg.se              |  4.835680751173709   |  817        |  213
10  |  http://gruvmor.wordpress.com            |  3.8                 |  28         |  10
31  |  http://thoralfalfsson.webblogg.se       |  3.6484375           |  339        |  128
33  |  http://tobbesmedieblogg.blogspot.se     |  2.583333333333333   |  19         |  12
9   |  http://galnegunnarsblogg.wordpress.com  |  2.388888888888889   |  250        |  180
27  |  http://samnytt.se                       |  2.193548387096774   |  74         |  62
13  |  http://imittsverige.blogspot.se         |  1.98                |  49         |  50
7   |  http://everykindapeople.blogspot.se     |  1.9                 |  9          |  10
30  |  http://thoralf.bloggplatsen.se          |  1.7986577181208054  |  119        |  149
32  |  http://tobbesmedieblogg.blogspot.com    |  1.75                |  9          |  12
38  |  http://www.abcnyheter.se                |  1.7457627118644068  |  44         |  59
37  |  http://varjager.wordpress.com           |  1.7267441860465116  |  125        |  172
15  |  http://integrationsbloggen.blogspot.se  |  1.694736842105263   |  66         |  95
2   |  http://aktualia.wordpress.com           |  1.6551724137931034  |  19         |  29
42  |  http://www.dagenssamhalle.se            |  1.5                 |  5          |  10
18  |  http://jihadimalmo.blogspot.se          |  1.3711340206185567  |  36         |  97
36  |  http://twitter.com                      |  1.3414634146341464  |  14         |  41
0   |  http://affes.wordpress.com              |  1.3333333333333333  |  33         |  99
22  |  http://morklaggning.wordpress.com       |  1.2421052631578948  |  23         |  95
8   |  http://friatider.se                     |  1.1009174311926606  |  11         |  109
47  |  http://www.magnussandelin.se            |  1.0714285714285714  |  3          |  42
35  |  http://tullberg.org                     |  1.0535714285714286  |  3          |  56
11  |  http://gudmundson.blogspot.se           |  1.0454545454545454  |  3          |  66
```