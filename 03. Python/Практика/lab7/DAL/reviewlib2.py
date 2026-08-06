"""
Модуль для работы с отзывами в SQLite (версия 2).

Содержит функции для CRUD-операций с таблицей REVIEWS.

Функции:
    create_review — добавляет отзыв
    get_review_by_market_id — читает отзывы для рынка
    calculate_score — рассчитывает среднюю оценку рынка
"""

import sqlite3
from statistics import mean

from BusinessLogic.marketList import get_market_by_id, update_market_info
from config import DATABASE_PATH



def create_review(review):
    """Добавляет отзыв в таблицу REVIEWS.

    Args:
        review (dict): Словарь с полями:
            - review_date: дата отзыва
            - user_id: ID пользователя
            - market_id: ID рынка
            - review_text: текст отзыва
            - score: оценка (1-5)

    Returns:
        None
    """
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
    from models.entities.review import Review
    """Читает все отзывы для указанного рынка.

    Args:
        market_id: ID рынка для фильтрации

    Returns:
        list[dict]: Список словарей с отзывами
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM REVIEWS WHERE market_id = ?",
            (market_id,)
        )
        entries = [Review.from_dict(dict(row)) for row in cursor.fetchall()]
        conn.close()
        return entries
    except Exception as e:
        print(e)
        print("Error in get_review_by_market_id")
        return []

def delete_reviews_by_market_id(market_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM REVIEWS WHERE market_id = ?",
        (market_id,)
    )
    conn.commit()
    conn.close()