from datetime import date, datetime, timedelta


def get_closest_value(df, day: date, column) -> float:
    lookup = convert_date_to_datetime(day)
    delta = timedelta(days=1)

    while True:
        try:
            return df.at[lookup, column]
        except KeyError:
            lookup -= delta
            continue


def convert_date_to_datetime(day: date) -> datetime:
    min_time = datetime.min.time()
    return datetime.combine(day, min_time)
