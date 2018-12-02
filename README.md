# WSEOptimizer v0.5.2
Project created as base for engineering thesis _"Optimization of stock exchange investment strategy with a genetic algorithm"_ written @ AGH UST 2018.

As a whole it computes winning strategy on WSE stocks basing on fundamental & technical analysis indicators optimized by genetic algorithm.

Result strategy is a set of clauses like `if( today RSI > 40 ) then +4 else 0`\
Sum of clause values can be used to compare each stock to pick best ones to theoretically beat the market.

## Installation

WSEO is heavily dependent on **Pandas** and **TkInter** frameworks.\
Simplest installation requires [Anaconda](https://www.anaconda.com/) Platform.\
Run `conda install -c anaconda pandas tk` to install everything at once.

Another approach is to open project in IDE such as PyCharm and let it manage dependencies for you.

## Components

Current version includes 3 separate modules:
* Database - fetches fundamental analysis data from BiznesRadar.pl & computes technical analysis over prepared data from Stooq.pl\
Returned data is used then by Genetic.\
Hit `python database/database_operator.py` to run.
* Genetic - implements main algorithm to optimize investing strategy.\
More info below.\
Hit `python genetic/GA_main.py` to run.
* GUI - currently stub :c

## License

This project is released under the MIT Licence. See the bundled LICENSE file for details.

(c) S.Domarecki 2018