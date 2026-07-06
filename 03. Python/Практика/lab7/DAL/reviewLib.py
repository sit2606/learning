"""
reviewLib — библиотека для работы с отзывами о фермерских рынках.

Основные функции:
- create_review(review): добавление отзыва в CSV-файл
- read_review(market_id): чтение отзывов по ID рынка
- calculate_score(market_id): расчёт средней оценки рынка

Структура CSV REVIEWS.csv:
- Id: UUID отзыва
- review_date: дата и время создания
- user_id: ID пользователя
- market_id: ID рынка
- review_text: текст отзыва
- score: оценка от 1 до 5

Использование:
    from DAL.reviewLib import create_review, read_review, calculate_score
"""
import csv
from statistics import mean

from BusinessLogic.marketList import get_market_by_id, update_market_info


def create_review(review):
    """
    Добавляет отзыв в файл REVIEWS.csv.

    Args:
        review (dict): Словарь с полями:
            - Id: UUID отзыва
            - review_date: дата и время
            - user_id: ID пользователя
            - market_id: ID рынка
            - review_text: текст отзыва
            - score: оценка (int, 1-5)
    """
    field_names = ['Id',
                  'review_date',
                  'user_id',
                  'market_id',
                  'review_text',
                  'score']
    file_path = f"files/{"REVIEWS"}.csv"
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writerow(review)
    except Exception as e:
        print(e)
        print("Error in create_review")
def get_review_by_market_id(market_id):
    """
    Читает отзывы для указанного рынка из файла REVIEWS.csv.

    Args:
        market_id: ID рынка для фильтрации отзывов.

    Returns:
        Список отзывов (в разработке — пока только выводит в консоль).
    """
    file_path = f"files/{"REVIEWS"}.csv"
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        review_list = []
        for review in reader:
            if review['market_id'] == market_id:
                review_list.append(review)
        return review_list
def calculate_score(market_id):
    """
    Рассчитывает среднюю оценку рынка на основе отзывов.

    Args:
        market_id: ID рынка.

    Returns:
        Средняя оценка (float) или None (в разработке).
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