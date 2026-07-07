from BusinessLogic.marketList import get_all_markets_ordered_by_column


def process(column, filter):
    market_base = get_all_markets_ordered_by_column(column)
