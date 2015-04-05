__author__ = 'ariky'
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.',
          'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# noinspection PyPep8Naming
def toFullMonthName(month):
    if month == 'Aug.':
        return 'August'
    if month == 'Sept.':
        return 'September'
    if month == 'Oct.':
        return 'October'
    if month == 'Nov.':
        return 'November'
    if month == 'Dec.':
        return 'December'
    return month


def toMonthNumber(month):
    index = months.index(month)
    if index > 11:
        return index - 11
    else:
        return index + 1