import database.indicators as ind
from shared.company import Company


def boost_company_info(company: Company) -> Company:
    company = englishify_columns(company)
    company = calculate_all_technicals(company)
    company = set_date_as_index(company)
    return company


def englishify_columns(company: Company) -> Company:
    company.technicals = company.technicals.rename(columns={'Data': 'Date',
                                                            'Otwarcie': 'Open',
                                                            'Najwyzszy': 'High',
                                                            'Najnizszy': 'Low',
                                                            'Zamkniecie': 'Close',
                                                            'Wolumen': 'Volume'})
    return company


def calculate_all_technicals(company: Company) -> Company:
    t = company.technicals

    t = ind.circulation(t, close_col='Close', vol_col='Volume')
    t = ind.sma(t, period=15, close_col='Close')
    t = ind.sma(t, period=40, close_col='Close')
    t = ind.ema(t, period=200, close_col='Close')
    t = ind.rsi(t, periods=14, close_col='Close')
    t = ind.macd(t,
                 period_long=26,
                 period_short=12,
                 period_signal=9,
                 close_col='Close')
    t = ind.trix(t, periods=14, signal_periods=9, close_col='Close')
    t = ind.williams_r(t,
                       periods=10,
                       high_col='High',
                       low_col='Low',
                       close_col='Close')
    t = ind.money_flow_index(t,
                             periods=14,
                             high_col='High',
                             low_col='Low',
                             close_col='Close',
                             vol_col='Volume')
    t = ind.roc(t, periods=14, close_col='Close')
    t = ind.ease_of_movement(t,
                             period=14,
                             high_col='High',
                             low_col='Low',
                             vol_col='Volume')

    company.technicals = t
    return company


def set_date_as_index(company: Company) -> Company:
    company.technicals.set_index('Date', inplace=True)
    return company
