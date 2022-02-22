# Get GQL Endpoint
with open("gql_endpoint.txt",'r') as f:
    GQL_ENDPOINT = f.read()

# Get Admin Secret
with open("hasura_secret.txt",'r') as f:
    HASURA_SECRET = f.read()

# Get Discord Token
with open('token.txt', 'r') as file:
    TOKEN = file.read()