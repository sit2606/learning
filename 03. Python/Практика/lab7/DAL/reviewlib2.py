import csv
import sqlite3
from statistics import mean

from BusinessLogic.marketList import get_market_by_id, update_market_info
from config import DATABASE_PATH


def create_review(review):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO REVIEWS (review_date, user_id, market_id, review_text, score) VALUES (?,?,?,?,?)",
        (review['review_date'], review['user_id'], review['market_id'],
         review['review_text'], review['score'])
    )
    conn.commit()
    conn.close()
def get_review_by_market_id(market_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM REVIEWS WHERE market_id = ?",
            (market_id,)
        )
        entries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return entries
    except Exception as e:
        print(e)
        print("Error in get_review_by_market_id")
        return []
def calculate_score(market_id):
    """
    Рассчитывает среднюю оценку рынка на основе отзывов и обновляет MARKET_INFO.csv.

    Args:
        market_id: ID рынка.

    Returns:
        dict: обновлённые данные рынка (market_info) с полем score.
    """
    reviews = get_review_by_market_id(market_id)
    score = []
    for review in reviews:
        score.append(float(review['score']))
    score = mean(score)
    market_info = get_market_by_id(market_id)
    market_info['basic_info'].update({'score': score})
    update_market_info(market_info)
    return market_info