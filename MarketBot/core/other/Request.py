from datetime import datetime, timedelta, date, time


class Request:
    def __init__(self, connectionDb):
        self.connectionDb = connectionDb

    async def dbGetCategories(self):
        query = f"SELECT DISTINCT category FROM market"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        lst = [result[0] for result in results]
        return lst

    async def dbGetSubCategories(self, category):
        query = f"SELECT DISTINCT subcategory FROM market WHERE category= '{category}'"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        lst = [result[0] for result in results]
        return lst

    async def dbGetProducts(self, category, subcategory):
        query = f"SELECT product,price FROM market WHERE category= '{category}' AND subcategory= '{subcategory}'"
        rows = await self.connectionDb.execute(query)
        lst = await rows.fetchall()
        return lst

    async def dbGetProductDescription(self, product, category, subcategory):
        query = (f"SELECT product,price,description FROM market WHERE category= '{category}' AND subcategory= '{subcategory}'"
                 f" AND product='{product[0]}'")
        rows = await self.connectionDb.execute(query)
        lst = await rows.fetchone()
        return lst
