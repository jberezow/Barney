from gql import gql, Client
from gql.transport.aiohttp import AsyncTransport
from barney import GQL_ENDPOINT, HASURA_SECRET
from aiographql.client import GraphQLClient, GraphQLRequest

class Tavern():
    moe = GraphQLClient(
        endpoint=GQL_ENDPOINT,
        headers={'x-hasura-admin-secret': HASURA_SECRET}
    )

    async def upsertUser(self, id: str, name: str):
        order_variables = {
            "id": id,
            "name": name
        }
        order = GraphQLRequest(
            """
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
        """
        )
        return await self.moe.query(order, order_variables)

moe = Tavern()

#result = moe.execute(query)
#print(result)