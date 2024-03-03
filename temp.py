import requests

movie = '603'

url = f"https://api.themoviedb.org/3/movie/{movie}"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Zjk4MWQ3YThhZjFmYjZlMWI4YjYxMzgzMzE4Yjk3MSIsInN1YiI6IjY1NTUzM2NmOTY1M2Y2MTNmNThhNWYxYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VQuWqWjwGjcV8Ij4UK9sYeTgjW2ShSdpxH__rLUXbSU"
}
response = requests.get(url, headers=headers)
data = response.json()

print(data)

# import requests
#
# url = "https://api.themoviedb.org/3/discover/movie?certification=matrix&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
# # url = "https://api.themoviedb.org/3/discover/movie?certification=
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Zjk4MWQ3YThhZjFmYjZlMWI4YjYxMzgzMzE4Yjk3MSIsInN1YiI6IjY1NTUzM2NmOTY1M2Y2MTNmNThhNWYxYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VQuWqWjwGjcV8Ij4UK9sYeTgjW2ShSdpxH__rLUXbSU"
# }
#
# response = requests.get(url, headers=headers)
#
# resp_dict = response.json()
#
# print(resp_dict['results'][1])