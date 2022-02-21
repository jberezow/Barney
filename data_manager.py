from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Get GQL Endpoint
with open("gql_endpoint.txt",'r') as f:
    gql_endpoint = f.read()

# Get admin secret
with open("hasura_secret.txt",'r') as f:
    hasura_secret = f.read()

# Try GQL Way of Importing
transport = AIOHTTPTransport(
    url=gql_endpoint,
    headers={'x-hasura-admin-secret': hasura_secret}
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