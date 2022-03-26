import asyncio
from typing import List, Dict,Optional
import aiohttp, json

with open("riot.json") as json_file:
    riot_headers = (json.load(json_file))[0]

class LolHttpsClient:
    URL_1 = "https://kr.api.riotgames.com"
    URL_2 = "https://asia.api.riotgames.com"
    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.session = session

    async def __enter__(self) -> "LolHttpsClient":
        return self

    async def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
    
    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def request_1( self, endpoint: str) -> Dict[str, str]:
        if not self.session:
            self.session = aiohttp.ClientSession(headers=riot_headers)
        async with self.session.get( self.URL_1+endpoint ) as response:
            return await response.json()
    
    async def request_2( self, endpoint: str) -> Dict[str, str]:
        if not self.session:
            self.session = aiohttp.ClientSession(headers=riot_headers)
        async with self.session.get( self.URL_2+endpoint ) as response:
            return await response.json()

    async def summoner_v4_by_name(self, summonerName: str) -> Dict[str, str]:
        return await self.request_1(f"/lol/summoner/v4/summoners/by-name/{summonerName}")

    async def league_v4_by_summoner(self, encryptedSummonerId: str) -> Dict[str, str]:
        return await self.request_1(f"/lol/league/v4/entries/by-summoner/{encryptedSummonerId}")

    async def match_v5_by_puuid(self, puuid: str, start: int, count: int) -> List[str]:
        return await self.request_2(f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}")

    async def match_v5_matchs(self, match_id: str) -> Dict[str, str]:
        return await self.request_2(f"/lol/match/v5/matches/{match_id}")

    async def champion_v4_free_champion(self) -> Dict[str, str]:
        return await self.request_1("/lol/platform/v3/champion-rotations")

    async def champion_mastery_v4(self, summonerID: str) -> Dict[str, str]:
        return await self.request_1(f"/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}")

    async def summoner_match_info(self, info: Dict[str, str]) -> Dict[str, str]:
        _list = [self.gamemode(info)]
        for player in info["participants"]:
            _list.append(self.summoner_match_info_Parsing(player))
        return await asyncio.gather(*_list)

    async def summoner_match_info_Parsing(self, info: str) -> Dict[str, str]:
        return { "kills" : info["kills"], "assists" : info["assists"],
            "deaths" : info["deaths"], "championName" : info["championName"], "champLevel" : info["champLevel"]
            , "teamPosition" : info["teamPosition"], "summonerName" : info["summonerName"], "summonerLevel" : info["summonerLevel"]
            , "win" : info["win"], "goldEarned" : info["goldEarned"], "goldSpent" : info["goldSpent"]
            , "items" : [info["item0"], info["item1"], info["item2"], info["item3"], info["item4"], info["item5"], info["item6"]]
            , "teamId" : info["teamId"]}

    async def gamemode(self, info):
        return {"gamemode" : info["gameMode"], "gameStartTimeStamp" : info["gameStartTimestamp"]
                , "gameDuration" : info["gameDuration"], "queueId" : info["queueId"]}