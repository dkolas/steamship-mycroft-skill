# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.
import requests
from mycroft.skills.core import FallbackSkill
from mycroft.skills.audioservice import AudioService
from mycroft.util.log import LOG
import time


class SteamshipAgentSkill(FallbackSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SteamshipAgentSkill, self).__init__(name="SteamshipAgentSkill")

    def initialize(self):
        """Registers the fallback skill."""
        # Warning:
        # This sets the fallback priority to 1, making it happen before
        # all other fallbacks, even padatious intents.
        # This is good for this example but BAD in general,
        # a fallback prio between 11 and 89 is good for most skills.

        self.register_fallback(self.handle_fallback, 1)
        self.audio_service = AudioService(self.bus)

        # Any other initialize code goes here

    def handle_fallback(self, message):
        utterance = message.data.get("utterance")

        api_key = self.settings.get('steamship_api_key')
        invocation_url = self.settings.get('package_instance_invocation_url') + '/mycroft_respond'
        user_id = self.settings.get('user_id')

        result = requests.post(invocation_url, headers={"Authorization":f"Bearer {api_key}"}, json={"user_id":user_id, "message":utterance})
        voice_url = result.text
        self.log.info(f"Got result URL: {voice_url}")
        response = requests.get(voice_url, headers={"Authorization":f"Bearer {api_key}"})
        filename = time.strftime("%Y%m%d-%H%M%S") + ".mp3"
        file_path = self.file_system.path.absolute() / filename

        self.log.info(f"Saved data at: {file_path}")
        with self.file_system.open(filename, "wb") as f:
            f.write(response.content)

        self.audioservice.play(tracks=(f"file://{file_path}", "audio/mpeg"))

        return True  # Indicate that the utterance was handled

def create_skill():
    return SteamshipAgentSkill()
