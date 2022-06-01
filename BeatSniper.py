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



RANK = int(input("Enter rank: "))
snipe_maps = {}     # {'Hash': Freq}

# Gets a list of 50 players on the same page as input rank
players_page_num = math.floor(RANK / 50) + 1
player_resp = requests.get(f'https://scoresaber.com/api/players?page={players_page_num}', headers=headers)
check_error(player_resp)
player_list = json.loads(player_resp.text)["players"]

# Fill and sort snipe_maps
for player in player_list:
    player_id = player["id"]
    player_scores_resp = requests.get('https://scoresaber.com/api/player/' + player_id + '/scores?limit=8&sort=top', headers=headers)
    check_error(player_scores_resp)
    player_scores = json.loads(player_scores_resp.text)["playerScores"]
    for score in player_scores:
        song_hash = score["leaderboard"]["songHash"]
        if song_hash in snipe_maps.keys():
            snipe_maps.update( {song_hash: snipe_maps[song_hash] - 1} )
        else:
            snipe_maps[song_hash] = -1

sorted_snipe_maps = {k: v for k, v in sorted(snipe_maps.items(), key=lambda item: item[1])}

# Output top 20 most common maps
count = 0
for hash in sorted_snipe_maps:
    if count < 20:
        map_resp = requests.get('https://api.beatsaver.com/maps/hash/' + hash)
        check_error(map_resp)
        map = json.loads(map_resp.text)
        print(str(sorted_snipe_maps[hash] * -1) + ' ' + map["id"] + ' ' + map["metadata"]["songAuthorName"] + ' - ' + map['metadata']['songName'])
        count += 1
    else:
        break
