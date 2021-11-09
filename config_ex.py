# Other
log_level = 'INFO'
twitchDLBin = "~/twitch-dl/twitch-dl.1.16.0.pyz"            # Location of twitch-dl.pyz file
targetDLDir = "/mnt/D/Media/Twitch"                         # Where to archive Vods to
dlThreadCount = 2                                           # Number of download threads to use. 1 for no concurrent downloads, more if your network can handle it

# Server
server_address = 'https://mydomain.com'                     # Public facing address corresponding to your SSL certs
bind_address = '192.168.0.20'                              # Address your host can bind to. For me this is the local ip of my server

# Twitch API auth
clientId = "t0TkCHwV8w0Axyauzq8XNZe7QC8lDo"                 # Id from Twitch dev dashboard. Not used yet
clientSecret = "W8jVCD0rRdcm6367ccqnbm266lw5iq"             # Secret from Twitch dev dashboard. Not used yet

# Subscriptions
subscriptionSecret = "9c119a2b-a003-4a6a-bc9e-674f5484702a" # Secret given to Twitch when creating your eventSub. I used a random GUID but it can be whatever string you want

## Note: All keys above are randomly generated in the form of real secrets. They aren't real ids or secrets.
