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
    
    async def upsertChannel(self, id: str, name: str, category_id: str):
        order = GraphQLRequest(
            query = """
            mutation UpsertChannel ($id: String, $name: String, $category_id: String) {
                insert_channels_one(
                    object: {
                        id: $id, 
                        name: $name,
                        category_id: $category_id
                    }, 
                    on_conflict: {
                        constraint: channels_pkey, 
                        update_columns: [name, category_id]
                    }
                ) 
                { 
                    id
                }
            }
        """,
            variables = {
                "id": id,
                "name": name,
                "category_id": category_id
            }
        )
        response = await self.make_query(order)
        return response
    
    async def upsertCategory(self, id: str, name: str):
        order = GraphQLRequest(
            query = """
            mutation UpsertCategory ($id: String, $name: String) {
                insert_category_one(
                    object: {
                        id: $id, 
                        name: $name
                    }, 
                    on_conflict: {
                        constraint: category_pkey, 
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

    async def allUsers(self):
        order = GraphQLRequest(
            query = """
            query AllUsers {
                lads {
                    id
                    name
                    wallet
                }
            }
        """
        )
        response = await self.make_query(order)
        return response

    async def makePayment(self, user, amount):
        order = GraphQLRequest(
            query = """
            mutation Payment ($user: String, $amount: float8) {
                update_lads(
                    _set: {
                        wallet: $amount
                    }, 
                    where: {
                        id: {
                            _eq: $user
                        }
                    }
                ) 
                {
                    affected_rows
                }
            }
        """,
            variables = {
                "user": user,
                "amount": amount
            }
        )
        response = await self.make_query(order)
        return response

moe = Tavern()

#result = moe.execute(query)
#print(result)