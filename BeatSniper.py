import requests
import json
import math

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'if-none-match': 'W/"5bb-1w7PpBYUYHeYpyYe6WV2MPmiJj0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }

def check_error(resp):
    resp = str(resp)
    code = resp[11:14]
    if code != "200":
        print('Code: ' + code + ', exiting...')
        exit()



RANK = 822  # User Input
snipe_maps = {}

players_page_num = math.floor(RANK / 50) + 1
player_resp = requests.get(f'https://scoresaber.com/api/players?page={players_page_num}', headers=headers)
check_error(player_resp)

player_list = json.loads(player_resp.text)["players"]

for player in player_list:
    player_id = player[id]
    player_scores_resp = requests.get('https://scoresaber.com/api/player/' + player_id + '/scores?limit=8&sort=top', headers=headers)
    check_error(player_scores_resp)
    player_scores = json.loads(player_scores_resp.text)["playerScores"]
    for score in player_scores:
        song_hash = score["leaderboard"]["songHash"]
        if song_hash in snipe_maps.keys():
            snipe_maps.update( {song_hash: snipe_maps[song_hash] + 1} )
        else:
            snipe_maps[song_hash] = 1




# player_id = 76561198048064878
# player_scores_resp = requests.get(f'https://scoresaber.com/api/player/{player_id}/scores?limit=8&sort=top', headers=headers)
# check_error(player_scores_resp)
# player_scores = json.loads(player_scores_resp.text)["playerScores"]
# for score in player_scores:
#     song_hash = score["leaderboard"]["songHash"]
#     if song_hash in snipe_maps.keys():
#         snipe_maps.update( {song_hash: snipe_maps[song_hash] + 1} )
#     else:
#         snipe_maps[song_hash] = 1

















