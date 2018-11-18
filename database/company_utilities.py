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
    company.technicals = ind.circulation(company.technicals, close_col='Close', vol_col='Volume')
    company.technicals = ind.sma(company.technicals, period=15, close_col='Close')
    company.technicals = ind.sma(company.technicals, period=40, close_col='Close')
    company.technicals = ind.ema(company.technicals, period=200, close_col='Close')
    company.technicals = ind.rsi(company.technicals, periods=14, close_col='Close')
    company.technicals = ind.macd(company.technicals,
                                  period_long=26,
                                  period_short=12,
                                  period_signal=9,
                                  close_col='Close')
    company.technicals = ind.trix(company.technicals, periods=14, signal_periods=9, close_col='Close')
    company.technicals = ind.williams_r(company.technicals,
                                        periods=10,
                                        high_col='High',
                                        low_col='Low',
                                        close_col='Close')
    company.technicals = ind.money_flow_index(company.technicals,
                                              periods=14,
                                              high_col='High',
                                              low_col='Low',
                                              close_col='Close',
                                              vol_col='Volume')
    company.technicals = ind.momentum(company.technicals, periods=14, close_col='Close')
    company.technicals = ind.ease_of_movement(company.technicals,
                                              period=14,
                                              high_col='High',
                                              low_col='Low',
                                              vol_col='Volume')
    return company


def set_date_as_index(company: Company) -> Company:
    company.technicals.set_index('Date', inplace=True)
    return company
