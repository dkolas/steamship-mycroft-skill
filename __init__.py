# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

from mycroft.skills.core import FallbackSkill
from mycroft.util.log import LOG


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

        # Any other initialize code goes here

    def handle_fallback(self, message):
        utterance = message.data.get("utterance")

        self.speak('Echoing a test: '+utterance)

        return True  # Indicate that the utterance was handled

def create_skill():
    return SteamshipAgentSkill()
