
import requests

# postedFrom = '01/10/2021'
# postedTo = '01/29/2021'


from datetime import datetime, timedelta
for x in range(10,30):
    todayDate = datetime(2020, 1, x)
    date = todayDate + timedelta(days=1)
    print(f'Yesterday : {date} & Today : {todayDate}')

# limit = '1000'
# offset = '1'
# response = requests.get(
#     f'https://api.sam.gov/prod/opportunities/v1/api/search?api_key=966J4JxaYz7zuKoYpAQBMOxW41uQ9w12aGdQuY6K&limit={limit}&postedFrom={postedFrom}&postedTo={postedTo}&offset={offset}')
# if response.status_code == 200:
#     data = response.json()
#     if data['description']:
#         for opportunity in data['opportunitiesData']:
#             print(opportunity['description'])
#     else:
#         print('No Data, API ')
# else:
#     print(f'Status : {response.status_code}')
#     message = response.json()
#     print(f'Error : {message["error"]}')
