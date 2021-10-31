# Twitch stream archival

The goal of this project is to automate Twitch vod downloads using [twitch-dl](https://github.com/ihabunek/twitch-dl).

This is done by setting up a simple python server to register with Twitch as a webhook for `stream.offline` notifications. When the webhook is called, it downloads the most recent stream. 

Currently subscription management is entirely manual. I used Postman to subscribe to channels I wished to archive. See [Twitch EventSub dev docs for more details](https://dev.twitch.tv/docs/eventsub).

#### Config
Configuration is handled with `config.py` I've gitignored my actual config since it contains secrets but I've included a redacted `config_ex.py` which uses fake credentials. Rename that file to `config.py` and fill in your own secrets and target directories.