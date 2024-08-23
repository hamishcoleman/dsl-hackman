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
                continue

            # TODO:
            # - lookup user_name and send it to the door open

            hackman_api.door_open_if_paid(
                card.user_id,
                source="CARD",
                rawdata=rawdata,
            )
