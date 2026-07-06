import csv
def create_review(review):
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
def read_review(market_id):
    file_path = f"files/{"REVIEWS"}.csv"
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i in reader:
            print('s')
def calculate_score(market_id):
    pass