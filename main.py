from typing import List, Dict, Optional
from fastapi import FastAPI
from LoLHttpsClient import LolHttpsClient
from pydantic import BaseModel
from DB import connectDB
import uvicorn, asyncio
app = FastAPI()
lol = LolHttpsClient()
db = connectDB()

class matchList(BaseModel):
    matchlist: List[str]

@app.get("/")
async def read_root():
    return {'hello':'world'}

@app.post("/")
async def read_root():
    return {'hello':'world'}

@app.get("/search/{summonerName}")
async def summonerinfo(summonerName: str) -> Dict[str, str]:
    return await lol.summoner_v4_by_name(summonerName)

@app.post("/match")
async def summoner_match(matchlist: matchList) -> List[Dict[str, str]]:
    match_list = []
    for match_id in dict(matchlist)["matchlist"]:
        match_list.append(lol.match_v5_matchs(match_id))
    info = asyncio.gather(*match_list)

@app.get("/match/{summonerpuuid}")
async def summoner_match(summonerpuuid: str, start: Optional[int] = 0, count: Optional[int] = 20) -> List[str]:
    return await lol.match_v5_by_puuid(summonerpuuid, start, count)

@app.get("/champitem/{champName}")
async def champion_items(champName: str, itemID: Optional[int] = -1):
    return await db.search(champName=champName, itemID=itemID)

@app.get("/summoner/{summonerid}")
async def summoner_profile(summonerid: str) -> List[Dict[str, str]]:
    return await lol.league_v4_by_summoner(summonerid)

@app.get("/freeChampion")
async def free_champion() -> Dict[str, str]:
    return await lol.champion_v4_free_champion()

@app.get("/championmastery/{summonerid}")
async def get_championmastery(summonerid: str, count: Optional[int] = 7) -> List[Dict[str, str]]:
    return (await lol.champion_mastery_v4(summonerid))[:count]

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8099, reload=True, workers=4)