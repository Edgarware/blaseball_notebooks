import requests_cache
import requests
import json
import os
import os.path

API_URL = "https://api2.blaseball.com"

_SESSIONS_BY_EXPIRY = {}


def session(expiry=0):
    """Get a caching HTTP session"""
    if expiry not in _SESSIONS_BY_EXPIRY:
        _SESSIONS_BY_EXPIRY[expiry] = requests_cache.CachedSession(backend="memory", expire_after=expiry)
    return _SESSIONS_BY_EXPIRY[expiry]


def _authorize():

    if os.path.exists('.blase_token'):
        with open('.blase_token', 'r') as f:
            x = json.load(f)
        return requests.utils.cookiejar_from_dict(x)

    x = session(0).post(f"{API_URL}/auth/sign-in",
                      data=json.dumps({"email": os.environ.get("BB_EMAIL"), "password": os.environ.get("BB_PASSWORD")}),
                      headers={"content-type": "application/json"})
    with open('.blase_token', 'w') as f:
        json.dump(requests.utils.dict_from_cookiejar(x.cookies), f)
    return requests.utils.dict_from_cookiejar(x.cookies)


def _api_get(url, expiry=60, req_auth=True):
    cookies = None
    if req_auth:
        cookies = _authorize()

    x = session(expiry).get(url, cookies=cookies)
    x.raise_for_status()
    return x.json()


def get_sim():
    return _api_get(f"{API_URL}/sim", expiry=360, req_auth=False)


def get_team(team_id, season_id=None, day=None):
    if season_id is None:
        season_id = get_sim()["simData"]["currentSeasonId"]
    if day is None:
        day = get_sim()["simData"]["currentDay"]

    return _api_get(f"{API_URL}/seasons/{season_id}/days/{day}/teams/{team_id}")


def get_all_teams(season_id=None, day=None):
    if season_id is None:
        season_id = get_sim()["simData"]["currentSeasonId"]
    if day is None:
        day = get_sim()["simData"]["currentDay"]

    return _api_get(f"{API_URL}/seasons/{season_id}/days/{day}/teams")


def get_player(player_id, season_id=None, day=None):
    if season_id is None:
        season_id = get_sim()["simData"]["currentSeasonId"]
    if day is None:
        day = get_sim()["simData"]["currentDay"]

    return _api_get(f"{API_URL}/seasons/{season_id}/days/{day}/players/{player_id}")


def get_elections(season_id=None):
    if season_id is None:
        season_id = get_sim()["simData"]["currentSeasonId"]

    return _api_get(f"{API_URL}/seasons/{season_id}/elections")
