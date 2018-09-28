#!/usr/bin/python3
from codecs import open
from datetime import date
import os.path
import requests
import shutil
import errno

#Local import
import cd

def main(user, target, lichess_api_key, args):
    print("Downloading %s's games to %s:" % (user, target))
    #Make my target directory
    try:
        os.makedirs(target)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with cd.cd(target):
        if (args.chess):
            archives = 'https://api.chess.com/pub/player/%s/games/archives' % user
            for archive in requests.get(archives).json()['archives']:
                download_archive(archive, target)

        if (args.lichess):
            getLichessGames(url, target)

#Download the lichess archive
def getLichessGames(url, target):
    Print("about to make lichess request")
    if lichess_api_key is not None:
        print(lichess_api_key)
        r = requests.get('https://lichess.org/api/games/user/%s' % user, headers={'Authorization': 'Bearer ' + lichess_api_key[0]}, stream=True)
    elif lichess_api_key is None:
        print(lichess_api_key)
        r = requests.get('https://lichess.org/api/games/user/%s' % user, stream=True)
    print(r.text)
    with open(target, 'a', encoding = 'utf-8') as output:
        print(r.text, target=output)
        print('', target=output)

#Download the chess.com archive
def download_archive(url, target):
    games = get(url)['games']
    print('Starting work on %s...' % url)

    for game in games:
        gameId = 0
        basePgn = game['white']['username'] + "-" + game['black']['username'] + ".pgn"
        pgn = basePgn
        #Add numbers until unique.
        while os.path.isfile(pgn):
            gameId = gameId + 1
            pgn = basePgn + str(gameId)
            
        with open(pgn, 'a', encoding='utf-8') as output:
            print(game['pgn'], file=output)
            print('', file=output)

def get(url, headers=None):
    return requests.get(url, headers = headers).json()

#Main
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER', help='The user whose games we want')
    parser.add_argument('target', metavar='PATH', help='which target directory to create the PGN files', default="./target", nargs='?')
    parser.add_argument('-c', '--chess', action='store_true', help='Get Chess.com games')
    parser.add_argument('-l', '--lichess', action='store_true', help='Get lichess games')
    parser.add_argument('--lichess_api_key', metavar='API_KEY', help =  'the api key for lichess', default=None, nargs = 1)
    args = parser.parse_args()
    main(args.user, args.target, args.lichess_api_key, args)
