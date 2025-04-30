from pymongo import MongoClient

class SentimentSDK:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    async def get_sentiment_score(self, symbol: str) -> float:
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "tokens",
                        "let": { "tokenIdStr": "$tokenid" },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": [{ "$toString": "$_id" }, "$$tokenIdStr"]
                                    }
                                }
                            }
                        ],
                        "as": "token_info"
                    }
                },
                { "$unwind": "$token_info" },
                { "$match": { "token_info.symbol": symbol } },
                {
                    "$group": {
                        "_id": "$token_info.symbol",
                        "score": { "$first": "$score" }
                    }
                }
            ]

            result = list(self.db.token_mentions.aggregate(pipeline))
            if result:
                return float(result[0]['score'])
            return 0.0
        except Exception as e:
            print(f"[SentimentSDK] Error getting sentiment score: {e}")
            return 0.0
