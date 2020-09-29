# WSEOptimizer

WSEO is trading strategy optimization library based on genetic algorithm and fundamental & technical analysis indicators.

Code was tested on data of Warsaw Stock Exchange stocks -
- stooq.pl for stock price history,
- BiznesRadar.pl for fundamental indicators.

Result strategy is a set of clauses like `if( today RSI > 40 ) then +4 else 0`\
Sum of clause values can be used to compare each stock to pick best ones to theoretically beat the market.

## Usage

#### Regular run


#### Fundamental database scrapping


#### Config

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
$ python genetic\\GA_main.py
```

Alternative way is to use bundled `PyCharm` configurations.

## See Also

- [eiten](https://github.com/tradytics/eiten) - Implements statistical and algorithmical trading engine, genetic algorithm included.
- [Lean](https://github.com/QuantConnect/Lean) - Algorithmic strategy research, backtesting and live trading engine.

## License

Project created as base for engineering thesis "Optimization of stock exchange investment strategy with a genetic algorithm" written @ AGH UST 2019.

This project is released under the MIT Licence. See the bundled LICENSE file for details.

(c) S.Domarecki 2018