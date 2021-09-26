from fastapi import FastAPI, Request, Response
from src.env import ENV
from pymongo import MongoClient


app = FastAPI()

cluster = MongoClient(ENV['MONGO_CONNECTION_STRING'])
collection = cluster[ENV['DB_NAME']][ENV['DB_NAME']]

tournaments = {}

@app.get('/')
async def home(res: Response, req: Request):
    print(f'Home Received Request')
    return "Welcome to the Tournam8 API!!!"

@app.get('/get_all_tournaments')
async def get_all_tournaments(res: Response, req: Request) -> None:
    database = collection.find({}, {'_id': False})
    tournaments.clear()
 
    for data in database:
        tournaments.update(data)

    print('get_all_tournaments -> ', tournaments)
    return tournaments

@app.post('/create_tournament')
async def create_tournament(res: Response, req: Request) -> None:
    tournament = await req.json()
    collection.insert_one({ '_id': tournament['id'], tournament['id']: tournament })
    print('API -> ', tournaments)
    return None

@app.post('/delete_tournament')
async def create_tournament(res: Response, req: Request) -> None:
    tournament = await req.json()
    collection.delete_many({ '_id': tournament['id'] })
    print('delete_tournament', tournaments)
    return None

@app.post('/player_signed_up')
async def player_signed_up(res: Response, req: Request) -> None:
    tournament = await req.json()
    id = tournament['id']
    player = tournament['player']

    # TODO: Checking if a player exists can be optimized by using mongo exist function
    tournament = collection.find_one({ '_id': id }, { '_id': False })

    if player in tournament[id]['players_signed_up']:
        return None

    collection.update_one({ 
        '_id': id
        }, 
            {
            '$push': {
                f"{id}.players_signed_up": player
            }
        }
    )
    print('API -> ', tournaments)

@app.post('/player_removed_from_signups')
async def player_removed_from_signups(res: Response, req: Request) -> None:
    player_data = await req.json()
    id = player_data['id']
    collection.update_one({ 
        '_id': id
        }, 
        {
            '$pull': {
                f"{id}.players_signed_up": player_data['player']
            }
        }
    )
    print('API -> ', tournaments)

@app.post('/start_tournament')
async def start_tournament(res: Response, req: Request) -> None:
    tournament_data = await req.json()
    id = tournament_data['id']

    # TODO Move these 2 update_one's to update_many()
    collection.update_many({
         '_id': id
        }, 
        {
            '$set': {
                f"{id}.status": True ,
                f"{id}.players_attended": tournament_data['tournament']['players_signed_up']
            }
        }
    )

# TODO: Could maybe be optimized to just add to player's stats
@app.post('/record_player_stats')
async def record_player_stats(res: Response, req: Request) -> None:
    player_data = await req.json()
    id = player_data['id']
    stats = player_data['stats']
    player = player_data['player']

    data = collection.find_one({ '_id': id, }, { '_id': False })
    player_stats = data[id]['player_stats']
    print(player_stats)

    if not player_stats.get(player):
        player_stats[player] = { '1': stats }
    else:
        player_stats[player][str(len(player_stats[player]) + 1)] = stats

    collection.update_one({
         '_id': id
        }, 
        {
            '$set': {
                f"{id}.player_stats.{player}": player_stats[player]
            }
        }
    )
    print('start_tournament -> ', tournaments)


