class Fundamental:
    def __init__(self, date, sales, earnings, book_value):
        self.date = date
        self.sales = sales
        self.earnings = earnings
        self.book_value = book_value
        print(date + " " + str(sales) + " " + str(earnings) + " " + str(book_value))
