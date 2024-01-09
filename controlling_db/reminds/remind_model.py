import json

class Remind:
    def __init__(self, creator: int, task: str, remind_type: str, nearest_trigger: int):
        self.id = None
        self.creator = creator
        self.task = task
        self.remind_type = remind_type
        self.nearest_trigger = nearest_trigger

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return {
            'id': self.id,
            'creator': self.creator,
            'task': self.task,
            'remind_type': self.remind_type,
            'nearest_trigger': self.nearest_trigger
        }


# Пример использования
# reminder = Remind('123456', 'Встреча в 15:00', 'ежедневные', 1672531200)
# print(reminder.to_json())