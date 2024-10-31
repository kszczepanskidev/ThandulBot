import logging
from tinydb import TinyDB, where

class DatesNotifyDatabase:
    """
    Helper class responsible for interacting with database storing data for dates message notifications.
    """

    class DatesNotifyLog:
        """
        Model class representing data with flags for dates message notifications.
        """

        message_id = None
        had_one_to_go = False
        had_all_players = False
        had_cant_players = False

        def __init__(self, message_id, had_one_to_go=False, had_all_players=False, had_cant_players=False):
            self.message_id = message_id
            self.had_one_to_go = had_one_to_go
            self.had_all_players = had_all_players
            self.had_cant_players = had_cant_players

        @classmethod
        def from_json(cls, json):
            return cls(json['message_id'], json['had_one_to_go'], json['had_all_players'], json['had_cant_players'])

        def to_json(self):
            return {'message_id': self.message_id, 'had_one_to_go': self.had_one_to_go, 'had_all_players': self.had_all_players, 'had_cant_players': self.had_cant_players}

        def __str__(self):
            return str(self.to_json())

    __dates_notify_log = TinyDB('storage/dates_notify_log.json')

    def add_log(self, dates_notify_log: DatesNotifyLog):
        if self.get_log(dates_notify_log.message_id) is not None:
            self.update_log(dates_notify_log)
            return

        self.__dates_notify_log.insert(dates_notify_log.to_json())

    def get_log(self, message_id):
        try:
            notify_log = self.__dates_notify_log.search(where('message_id') == message_id)[0]
            return self.DatesNotifyLog.from_json(notify_log)
        except:
            return None

    def update_log(self, dates_notify_log: DatesNotifyLog):
        self.__dates_notify_log.update(dates_notify_log.to_json(), where('message_id') == dates_notify_log.message_id)

dates_notify_database = DatesNotifyDatabase()
