from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from keys import GQL_ENDPOINT, HASURA_SECRET

# Try GQL Way of Importing
transport = AIOHTTPTransport(
    url=GQL_ENDPOINT,
    headers={'x-hasura-admin-secret': HASURA_SECRET}
)

manager = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
    query AllChannels {
        channels {
            name
        }
    }
"""  
)

result = manager.execute(query)
print(result)