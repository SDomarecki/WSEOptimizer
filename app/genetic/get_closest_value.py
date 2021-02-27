import datetime


def get_closest_value(df, day, column) -> float:
    delta = datetime.timedelta(days=1)

    while True:
        try:
            return df.at[day, column]
        except KeyError:
            day -= delta
            continue
