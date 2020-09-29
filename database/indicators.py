"""
Circulation
Source: ===
Params: 
    data: pandas DataFrame
    period: smoothing period
    close_col: the name of the CLOSE values column

Returns:
    copy of 'data' DataFrame with 'ema[period]' column added
"""


def circulation(data, close_col='<CLOSE>', vol_col='<VOL>'):
    data['Circulation'] = data[close_col] * data[vol_col]
    return data


"""
Simple moving average
Source: ===
Params: 
    data: pandas DataFrame
    period: smoothing period
    close_col: the name of the CLOSE values column

Returns:
    copy of 'data' DataFrame with 'ema[period]' column added
"""


def sma(data, period=0, close_col='<CLOSE>'):
    data['sma' + str(period)] = data[close_col].rolling(window=period).mean()
    return data


"""
Exponential moving average
Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
Params: 
    data: pandas DataFrame
    period: smoothing period
    column: the name of the column with values for calculating EMA in the 'data' DataFrame
    
Returns:
    copy of 'data' DataFrame with 'ema[period]' column added
"""


def ema(data, period=0, close_col='<CLOSE>'):
    data['ema' + str(period)] = data[close_col].ewm(ignore_na=False, min_periods=period, com=period, adjust=True).mean()
    return data


"""
Moving Average Convergence/Divergence Oscillator (MACD)
Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_average_convergence_divergence_macd
Params: 
    data: pandas DataFrame
    period_long: the longer period EMA (26 days recommended)
    period_short: the shorter period EMA (12 days recommended)
    period_signal: signal line EMA (9 days recommended)
    column: the name of the column with values for calculating MACD in the 'data' DataFrame
    
Returns:
    copy of 'data' DataFrame with 'macd_val' and 'macd_signal_line' columns added
"""


def macd(data, period_long=26, period_short=12, period_signal=9, close_col='<CLOSE>'):
    remove_cols = []
    if not 'ema' + str(period_long) in data.columns:
        data = ema(data, period=period_long, close_col=close_col)
        remove_cols.append('ema' + str(period_long))

    if not 'ema' + str(period_short) in data.columns:
        data = ema(data, period=period_short, close_col=close_col)
        remove_cols.append('ema' + str(period_short))

    data['macd_val'] = data['ema' + str(period_short)] - data['ema' + str(period_long)]
    data['macd_signal_line'] = data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_signal,
                                                    adjust=True).mean()

    data = data.drop(remove_cols, axis=1)

    return data


"""
Typical Price
Source: https://en.wikipedia.org/wiki/Typical_price
Params: 
    data: pandas DataFrame
    high_col: the name of the HIGH values column
    low_col: the name of the LOW values column
    close_col: the name of the CLOSE values column

Returns:
    copy of 'data' DataFrame with 'typical_price' column added
"""


def typical_price(data, high_col='<HIGH>', low_col='<LOW>', close_col='<CLOSE>'):
    data['typical_price'] = (data[high_col] + data[low_col] + data[close_col]) / 3

    return data


"""
Ease of Movement
Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ease_of_movement_emv
Params: 
    data: pandas DataFrame
    period: period for calculating EMV
    high_col: the name of the HIGH values column
    low_col: the name of the LOW values column
    vol_col: the name of the VOL values column

Returns:
    copy of 'data' DataFrame with 'emv' and 'emv_ema_[period]' columns added
"""


def ease_of_movement(data, period=14, high_col='<HIGH>', low_col='<LOW>', vol_col='<VOL>'):
    for index, row in data.iterrows():
        if index > 0:
            midpoint_move = (row[high_col] + row[low_col]) / 2 - (
                    data.at[index - 1, high_col] + data.at[index - 1, low_col]) / 2
        else:
            midpoint_move = 0

        diff = row[high_col] - row[low_col]

        if diff == 0:
            # this is to avoid division by zero below
            diff = 0.000000001

        vol = row[vol_col]
        if vol == 0:
            vol = 1
        box_ratio = (vol / 100000000) / diff
        emv = midpoint_move / box_ratio

        data.set_value(index, 'emv', emv)

    data['emv_ema_' + str(period)] = data['emv'].ewm(ignore_na=False, min_periods=0, com=period, adjust=True).mean()

    return data


"""
Money Flow Index (MFI)
Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi
Params: 
    data: pandas DataFrame
    periods: period for calculating MFI (14 days recommended)
    vol_col: the name of the VOL values column

Returns:
    copy of 'data' DataFrame with 'money_flow_index' column added
"""


def money_flow_index(data, periods=14, high_col='<HIGH>', low_col='<LOW>', close_col='<CLOSE>', vol_col='<VOL>'):
    remove_tp_col = False
    if not 'typical_price' in data.columns:
        data = typical_price(data, high_col=high_col, low_col=low_col, close_col=close_col)
        remove_tp_col = True

    data['money_flow'] = data['typical_price'] * data[vol_col]
    data['money_ratio'] = 0.
    data['money_flow_index'] = 0.
    data['money_flow_positive'] = 0.
    data['money_flow_negative'] = 0.

    for index, row in data.iterrows():
        if index > 0:
            if row['typical_price'] < data.at[index - 1, 'typical_price']:
                data.set_value(index, 'money_flow_positive', row['money_flow'])
            else:
                data.set_value(index, 'money_flow_negative', row['money_flow'])

        if index >= periods:
            period_slice = data['money_flow'][index - periods:index]
            positive_sum = data['money_flow_positive'][index - periods:index].sum()
            negative_sum = data['money_flow_negative'][index - periods:index].sum()

            if negative_sum == 0.:
                # this is to avoid division by zero below
                negative_sum = 0.00001
            m_r = positive_sum / negative_sum

            mfi = 1 - (1 / (1 + m_r))

            data.set_value(index, 'money_ratio', m_r)
            data.set_value(index, 'money_flow_index', mfi)

    data = data.drop(['money_flow', 'money_ratio', 'money_flow_positive', 'money_flow_negative'], axis=1)

    if remove_tp_col:
        data = data.drop(['typical_price'], axis=1)

    return data


"""
Rate of change
Source: https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
Params: 
    data: pandas DataFrame
    periods: period for calculating ROC
    close_col: the name of the CLOSE values column

Returns:
    copy of 'data' DataFrame with 'roc' column added
"""


def roc(data, periods=14, close_col='<CLOSE>'):
    data['roc'] = 0.

    for index, row in data.iterrows():
        if index >= periods:
            prev_close = data.at[index - periods, close_col]
            val_perc = (row[close_col] - prev_close) / prev_close

            data.set_value(index, 'roc', val_perc)

    return data


"""
Relative Strength Index
Source: https://en.wikipedia.org/wiki/Relative_strength_index
Params: 
    data: pandas DataFrame
    periods: period for calculating momentum
    close_col: the name of the CLOSE values column
    
Returns:
    copy of 'data' DataFrame with 'rsi' column added
"""


def rsi(data, periods=14, close_col='<CLOSE>'):
    data['rsi_u'] = 0.
    data['rsi_d'] = 0.
    data['rsi'] = 0.

    for index, row in data.iterrows():
        if index >= periods:

            prev_close = data.at[index - periods, close_col]
            if prev_close < row[close_col]:
                data.set_value(index, 'rsi_u', row[close_col] - prev_close)
            elif prev_close > row[close_col]:
                data.set_value(index, 'rsi_d', prev_close - row[close_col])

    data['rsi'] = data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() / (
            data['rsi_u'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean() +
            data['rsi_d'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean())

    data = data.drop(['rsi_u', 'rsi_d'], axis=1)

    return data


"""
William's % R
Source: https://www.metastock.com/customer/resources/taaz/?p=126
Params: 
    data: pandas DataFrame
    periods: the period over which to calculate the indicator value
    high_col: the name of the HIGH values column
    low_col: the name of the LOW values column
    close_col: the name of the CLOSE values column

Returns:
    copy of 'data' DataFrame with 'williams_r' column added
"""


def williams_r(data, periods=14, high_col='<HIGH>', low_col='<LOW>', close_col='<CLOSE>'):
    data['williams_r'] = 0.

    for index, row in data.iterrows():
        if index > periods:
            price_range = max(data[high_col][index - periods:index]) - min(data[low_col][index - periods:index])
            if price_range == 0:
                continue
            data.set_value(index, 'williams_r', ((max(data[high_col][index - periods:index]) - row[close_col]) /
                                                 price_range) * (-100))

    return data


"""
TRIX
Source: https://www.metastock.com/customer/resources/taaz/?p=114
Params: 
    data: pandas DataFrame
    periods: the period over which to calculate the indicator value
    signal_periods: the period for signal moving average
    close_col: the name of the CLOSE values column
    
Returns:
    copy of 'data' DataFrame with 'trix' and 'trix_signal' columns added
"""


def trix(data, periods=14, signal_periods=9, close_col='<CLOSE>'):
    data['trix'] = data[close_col].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=1, adjust=True).mean()
    data['trix_signal'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=signal_periods, adjust=True).mean()

    return data
