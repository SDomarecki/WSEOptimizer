# WSEOptimizer

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![Updates](https://pyup.io/repos/github/SDomarecki/WSEOptimizer/shield.svg)](https://pyup.io/repos/github/SDomarecki/WSEOptimizer/)
[![Actions Status](https://github.com/SDomarecki/WSEOptimizer/workflows/Python%20application/badge.svg)](https://github.com/SDomarecki/WSEOptimizer/actions)
[![codecov](https://codecov.io/gh/SDomarecki/WSEOptimizer/branch/master/graph/badge.svg?token=8CB84LZK43)](https://codecov.io/gh/SDomarecki/WSEOptimizer)

WSEO is trading strategy optimization library based on genetic algorithm and fundamental & technical analysis indicators.

Code was tested on data of Warsaw Stock Exchange stocks -
- stooq.pl for stock price history,
- BiznesRadar.pl for fundamental indicators.

Result strategy is a set of clauses like `if( today RSI > 40 ) then +4 else 0`\
Sum of clause values can be used to compare each stock to pick best ones to theoretically beat the market.

## Usage

#### 1. Stooq downloader
To wget all of WSE stocks history a few days or VPN will be needed due to stooq.pl limit of daily downloads.
Run:
```bash
$ python database_scripts\\stooq_downloader.py
```
to download 200 stock histories into database/stooq directory.
Currently (2020-10-05) WSE main market lists 436 companies.

#### 2. Fundamental database scrapping

If all stock histories are ready, fundamental data can be scrapped from BiznesRadar.pl and mixed into preprocessed .csv database.
To scrap:
```bash
$ python database_scripts\\database_preprocessor.py
```
It can be kinda slow due to all of the technical indicators computations.

#### 3. Genetic algorithm
Last part of application is genetic algorithm itself.
All you have to do is ~~squish that cat~~ run:
```bash
$ python genetic\\genetic_algorithm_worker.py
```
in root directory.
Application as a result will generate at each epoch plot of best model performance comparing to benchmark.
Moreover at the end of execution WSEOptimizer will print plot of end performance of best model in each epoch.

#### Config.json
List of all of the options:
```bash
{
  "database": {
    "min_circulation": 500000, #-1 == omitted, prevents from trading with penny stocks-like companies
    "max_circulation": -1, #-1 == omitted
    "sectors": [],
    "companies": [], #if empty whole database will load
    "chunks": 8 #divide database into equal chunks, reduces overfitting
  },
  "simulation": {
    "timedelta": 7, #rating calculations will be performed each x days
    "iterations": 50, #aka epochs
    "initial_population": 100,
    "learning": { #RRRR-MM-DD
      "start_date": "2010-01-01",
      "end_date": "2015-12-31"
    },
    "testing": [ #RRRR-MM-DD, multiple data ranges are handled
      {"start_date": "2016-01-01", "end_date": "2017-12-31"}
    ]
  },
  "selection": {
    "method": "roulette", #available "rating", "tournament", "roulette"
    "agents_to_save": 0.75 #rest of them will be erased
  },
  "crossover": {
    "constant_length": true, #genome length
    "initial_genes": 5, #in epoch 0 all of agents have genome of this length
    "max_genes": 10,
    "mutation_rate": 0.1
  },
  "wallet": {
    "start_cash": 100000,
    "return_method": "total_value", #Optimization method, available "total_value" & "sharpe"
    "benchmark": "wig", #Index used in comparison of performance
    "risk_free_return": 0.025, #Used in sharpe opt. method
    "fees": { # fee= cost_of_position*rate + added,
              # if smaller than min then min,
              # if larger than max then max
      "min": 0,
      "rate": 0.098,
      "added": 1,
      "max": 125
    },
    "stocks_to_buy": 3, #minimum amount of different companies in wallet
    "stocks_to_hold": 6  #maximum amount of different companies in wallet
  },
  "genes": {
    "fin_statement_lag": 135, #statement of quarter is published at the end of quarter plus x days
                              #prevents from "looking into the future"
    "fundamental_to_all": 0.7 #how many fundamental genes are in genome, from 0.0 to 1.0
  }
}
```
## Install

```bash
# Clone this repository
$ git clone https://github.com/SDomarecki/WSEOptimizer

# Go into the repository
$ cd WSEOptimizer

# (optional) Install virtualenv for venv handling
$ pip install virtualenv

# (optional) Create virtual environment for this project
$ virtualenv venv

# (optional) Activate new venv
$ venv/Scripts/activate

# Install dependencies
$ pip install -r requirements.txt

# Run script
$ python genetic\\genetic_algorithm_worker.py
```

Alternative way is to use bundled `PyCharm` configurations.

## See Also

- [eiten](https://github.com/tradytics/eiten) - Implements statistical and algorithmical trading engine, genetic algorithm included.
- [Lean](https://github.com/QuantConnect/Lean) - Algorithmic strategy research, backtesting and live trading engine.

## License

Project created as base for engineering thesis "Optimization of stock exchange investment strategy with a genetic algorithm" written @ AGH UST 2019.

This project is released under the MIT Licence. See the bundled LICENSE file for details.

(c) S.Domarecki 2018
