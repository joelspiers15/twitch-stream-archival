import http.server
import os
import json
import hmac
import hashlib
import logging
from config import *
from TwitchDLBridge import downloadLatestVod

LOG = logging.getLogger("RequestHandler")

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ended':
            LOG.debug("POST recieved")
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            ## Used for adding new event subscriptions. Twitch validates endpoint by requesting you respond with a random challenge
            ## Uncomment when adding new webhook
            # challenge = json.loads(body).get('challenge')
            # if challenge is not None and challenge:
            #     self.handleChallenge(challenge)
            #     return

            ## Validate request came from Twitch
            if not self.validate(body):
                return

            LOG.debug('======== Headers ========')
            LOG.debug(self.headers)
            LOG.debug('======== Request body ========')
            LOG.debug(json.loads(body))
            LOG.debug('')

            try:
                self.handleIt(body)
            except Exception:
                LOG.error("Error handling request")
                return
        else:
            # Post to unknown endpoint
            self.send_response(404)
            self.end_headers()

    def validate(self, body):
        LOG.debug("======== Validating ========")

        hmac_message = self.headers['Twitch-Eventsub-Message-Id'] + self.headers['Twitch-Eventsub-Message-Timestamp'] + str(body)[2:-1]
        signature = hmac.new(
            bytes(subscriptionSecret, 'utf-8'),
            msg=bytes(hmac_message, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        expected_signature_header = 'sha256=' + str(signature)

        LOG.debug("Expected:\t" + expected_signature_header)
        LOG.debug("Actual:  \t" + self.headers['Twitch-Eventsub-Message-Signature'])

        if self.headers['Twitch-Eventsub-Message-Signature'] != expected_signature_header:
            LOG.error("Validation failed")
            print("")
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Validation failed')
            return False
        else:
            LOG.debug("Success")
            LOG.debug("")
            self.send_response(200)
            self.end_headers()
            return True

    def handleChallenge(self, challenge):
        LOG.info("Responding to challenge: " + challenge)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(challenge, 'ascii'))


    def handleIt(self, body):
        LOG.debug("======== Handling request ========")

        # Twitch requires that we return 200 to their webhook requests or risk deactivation of the subscription
        # Just return 200 before trying to download
        self.send_response(200)
        self.end_headers()

        channelName = json.loads(body).get('event').get('broadcaster_user_name')
        downloadLatestVod(channelName)
