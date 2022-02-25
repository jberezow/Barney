from gql import gql, Client
from gql.transport.aiohttp import AsyncTransport
from barney import GQL_ENDPOINT, HASURA_SECRET
from aiographql.client import GraphQLClient, GraphQLRequest
from aiohttp import ClientSession, TCPConnector

class Tavern():
    db_client = GraphQLClient(
        endpoint=GQL_ENDPOINT,
        headers={'x-hasura-admin-secret': HASURA_SECRET}
    )

    async def upsertUser(self, id: str, name: str):
        connector = TCPConnector(
            force_close=True, limit=1, enable_cleanup_closed=True
        )
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
        session = ClientSession(connector=connector)
        response = await self.db_client.query(request=order,session=session)
        await session.close()
        return response
    
    async def upsertChannel(self, id: str, name: str):
        connector = TCPConnector(
            force_close=True, limit=1, enable_cleanup_closed=True
        )
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
        session = ClientSession(connector=connector)
        response = await self.db_client.query(request=order,session=session)
        await session.close()
        return response

moe = Tavern()

#result = moe.execute(query)
#print(result)