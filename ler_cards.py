# import requests
# import json

# URL_CARDS = 'https://api.clashroyale.com/v1/cards'

# headers = {
#     'Content-type': 'application/json',
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjhmYjMwZTRiLTQ4MTMtNGMyZC1iMWE2LWUzODliM2JmODk5MyIsImlhdCI6MTcyNjM2MTM1NSwic3ViIjoiZGV2ZWxvcGVyL2I2NGU1YmMzLWZiMmEtODRjNi1mOGE4LTBhOWVmMjBmNTNiYSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjQuMTYzLjIxMS4xMjMiXSwidHlwZSI6ImNsaWVudCJ9XX0.uMAt4Ed0WrECGJfLMOn6OaIKPlD3_YXo4mXxMOVxENlHPM2ndnWVGIO-Jw8AKFMaom_q6-WhrQ3sQyTqlVK5dw'
# }

# def get_cards_info():
#     response = requests.get(url=URL_CARDS, headers=headers)
#     print('teste')

# get_cards_info()


import pandas as pd

arquivo_csv = 'cardlist.csv'

df = pd.read_csv(arquivo_csv)

print(df.head(100))  

print(df.describe())

print(df.columns)
