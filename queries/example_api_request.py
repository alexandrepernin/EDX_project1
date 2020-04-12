import requests
import pprint
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0BnTXldL5qD8QiRIybiNg", "isbns": "0399153942"}).json()
pprint.pprint(res)
print(res["books"][0]["average_rating"])
