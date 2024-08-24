from hackman_notifier import api as notification_api
from django.core.management.base import BaseCommand
from django_redis import get_redis_connection

from hackman_rfid import api as rfid_api
from hackman import api as hackman_api

import json


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        r = get_redis_connection('default')

        for card_hash, rawdata in rfid_api.cards_read():

            card = rfid_api.card_validate(card_hash)
            if not card:
                continue

            if rawdata is None:
                # if we have no raw data, just use the card data
                rawdata = card_hash
            if isinstance(rawdata, bytes):
                # make it readable
                rawdata = rawdata.hex()

            if not card.user_id:
                r.set('rfid_last_unpaired', card.id)
                notification_api.notify_subject(b'door_event', json.dumps({
                    'event': 'CARD_UNPAIRED',
                    'card_id': card.id,
                    'rawdata': rawdata,
                }))
                # Hacky magic number to turn blink LEDs in error pattern
                rfid_api._card_command("7")
                continue

            # TODO:
            # - lookup user_name and send it to the door open

            opened = hackman_api.door_open_if_paid(
                card.user_id,
                source="CARD",
                rawdata=rawdata,
            )

            if opened:
                # Hacky magic numbers to turn on green LED only
                rfid_api._card_command("0")
                rfid_api._card_command("1")
                # TODO:
                # - should have the green light turn off at the same time as
                #   the lock shuts.
                #   Adding the door lock timeout to the config would at least
                #   allow the correct number to be known to this microservice,
                #   but this microservice would need to have a timer added
            else:
                # Hacky magic number to turn blink LEDs in error pattern
                rfid_api._card_command("7")
