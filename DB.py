import os, pymysql, asyncio, json
from typing import Optional, Tuple
with open("riot.json") as json_file:
    champtbl = (json.load(json_file))[1]["champ"]

class connectDB:
    conn = pymysql.connect(host=os.environ["DBHOST"], user=os.environ["DBUSEID"], password=os.environ["DBKEY"], db="championdb", charset="utf8", autocommit=True)
    cur = conn.cursor()

    async def insert(self, tbl: int, itemID: int) -> None:
        self.cur.execute(query=f"INSERT items{tbl}(item) VALUES({itemID})")

    async def search(self, champName: str, itemID: Optional[int] = -1) -> Tuple[Tuple[int, int]]:
        if itemID == -1:
            self.cur.execute(f"SELECT item, {champName} FROM items{champtbl[champName]} ORDER BY {champName} DESC;")
            return self.cur.fetchall()
        else:
            self.cur.execute(query=f"SELECT {champName} FROM items{champtbl[champName]} WHERE item = {itemID};")
            return self.cur.fetchall()[0][0]
    
    async def update(self, champName: str, itemID: int, num: Optional[int] = 1) -> None:
        value = await self.search(champName, itemID)
        self.cur.execute(query=f"UPDATE items{champtbl[champName]} SET {champName} = {value + num} WHERE item = {itemID};")