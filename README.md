# Access pre-release beta

Go to https://speakoia.sekoia.lol/beta/thohzaen7oG3uathiegh6Ahd8saikeghaey0ohvie1aigh8aequaitoowahjee6c

![](2023-04-01-14-33-26.png)

# How to run

````bash
docker build -t xy .
docker run -p 8000:8000 --name xy --rm xy
````

Then go to `http://localhost:8000`

# Dev mode

````bash
./dev.sh
````

or `make dev`


# API

* Add a vote to a card (created if doesn't exist)
````python
client.post("/api/vote", json={"title": "my situation"}).json()
````

* Add a description to a card (created if doesn't exist)
````python
client.put("/api/vote", json={"title": "my situation", "description": "my description"}).json()
````

* Set a card's tag (created if doesn't exist) : use a list of strings or a comma-separated string. Tags are overwritten. If provided with an empty string or empty array, all tags are removed from the card
````python
client.put("/api/vote", json={"title": "my situation", "tags": ["tag1","tag2"]}).json()
````

* Get votes (cards content)
````python
client.get("/api/votes")
````

* Bet for the current month
````python
client.post("/api/bet", body=42)
````

* Get bets for the month (ADMIN ONLY). If no month is given in queryparams, take the current month
````python
client.get("/api/bets", params={"month":2})
````

* Get aggregate bet stats for the month (ADMIN ONLY). If no month is given in queryparams, take the current month
````python
client.get("/api/bets/stats", params={"month":2})
````
