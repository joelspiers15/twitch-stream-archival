import requests

authUrl = "https://id.twitch.tv/oauth2/token"
eventSubUrl = "https://api.twitch.tv/helix/eventsub/subscriptions"

class TwitchApi:
    clientId = ""
    clientSecret = ""
    accessToken = ""

    headers = {}

    def __init__(self, clientId, clientSecret):
        print("Setting up api client")
        self.clientId = clientId
        self.accessToken = self.getAccessToken(clientSecret)
        self.headers =  {
                            "Client-ID":self.clientId,
                            "Authorization":"Bearer " + self.accessToken
                        }
        print("Successfully connected to twitch")
        print("\tAccessToken: " + self.accessToken)

    def getAccessToken(self, clientSecret):
        res = requests.post(authUrl + "?client_id=" + self.clientId + "&client_secret=" + clientSecret + "&grant_type=client_credentials")

        if (not res.ok):
            print("ERROR: Failed to get accessToken")
            print(res)
            print(res.json())
            raise LookupError()

        return res.json().get("access_token")

    def getEventSubs(self):
        res = requests.get(eventSubUrl, headers=self.headers)
        return res.json().get("data")

    def addEventSub(self):
        res = requests.get(eventSubUrl, headers=self.headers)