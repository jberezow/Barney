# Barney
A simple Discord Bot. Mostly for learning the Discord API and making small tools for our server.

**PROJECT UPDATE 02/2022**

I am working to connect the bot to a simple GQL API on top of a small Postgres DB for collecting server statistics. This is to work towards having data for running NLP experiments in the hopes of making a basic chatbot.

<hr />

**Details**

BARNEY: Discord bot client

MOE: Data manager (GQL api)

ACTIONS: Server-side and client-side functions

KEYS: Private folder for connection keys

Barney is hosted on an EC2 Amazon Linux instance on AWS. One mid-term action item is to create a deployment pipeline so Barney can be upgraded seamlessly with minimal downtime.

The long term goal is to implement data tagging of conversations for the development of a weak chatbot tuned to our Discord server.
