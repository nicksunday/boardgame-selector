from boardgamegeek import BGGClient
from random import randint

def get_random_game(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    bgg = BGGClient()

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'username' in request_json:
        username = request_json['username']
    elif request_args and 'username' in request_args:
        username = request_args['username']
    else:
        return "Please enter a BoardGameGeek username"

    if request_json and 'players' in request_json:
        players = int(request_json['players'])
    elif request_args and 'players' in request_args:
        players = int(request_args['players'])
    else:
        players = None

    collection = bgg.collection(user_name=username, own=True, exclude_subtype="boardgameexpansion")
    #print(collection[0].max_players)
    sub_collection = []
    if players:
        for game in collection:
            if game.min_players <= players <= game.max_players:
                sub_collection.append(game)
        random_game = randint(0, len(sub_collection) - 1)
        # return sub_collection[random_game].name #, 
        return sub_collection[random_game].image
    else:
        random_game = randint(0, len(collection) - 1)
        # return collection[random_game].name #, 
        return collection[random_game].image