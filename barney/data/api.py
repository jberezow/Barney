from urllib import response
from gql import gql, Client
from gql.transport.aiohttp import AsyncTransport
from barney import GQL_ENDPOINT, HASURA_SECRET
from aiographql.client import GraphQLClient, GraphQLRequest
from aiohttp import ClientSession, TCPConnector

class Tavern():
    
    async def make_query(self, query):
        async with ClientSession() as session:
            db_client = GraphQLClient(
                endpoint=GQL_ENDPOINT,
                headers={'x-hasura-admin-secret': HASURA_SECRET},
                session=session
            )
            response = await db_client.query(request=query)
        return response

    async def upsertUser(self, id: str, name: str):
        order = GraphQLRequest(
            query = """
            mutation UpsertUser ($id: String, $name: String) {
                insert_lads_one(
                    object: {
                        id: $id, 
                        name: $name
                    }, 
                    on_conflict: {
                        constraint: lads_pkey, 
                        update_columns: name
                    }
                ) 
                { 
                    id
                }
            }
        """,
            variables = {
                "id": id,
                "name": name
            }
        )
        response = await self.make_query(order)
        return response
    
    async def upsertChannel(self, id: str, name: str):
        order = GraphQLRequest(
            query = """
            mutation UpsertChannel ($id: String, $name: String) {
                insert_channels_one(
                    object: {
                        id: $id, 
                        name: $name
                    }, 
                    on_conflict: {
                        constraint: channels_pkey, 
                        update_columns: name
                    }
                ) 
                { 
                    id
                }
            }
        """,
            variables = {
                "id": id,
                "name": name
            }
        )
        response = await self.make_query(order)
        return response

moe = Tavern()

#result = moe.execute(query)
#print(result)