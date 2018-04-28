import datetime

# I want a group of classes that will represent the frames in memory for each strategy

class BaseFrame:
    def __init__(self, number, name):
        self.number = number
        self.name = name


class ClockItem(BaseFrame):
    def __init__(self, number, name):
        super().__init__(number, name)
        self.just_used = True

class OptimalReplacementRR():
    def __init__(self, frame_index_in_memory, distance_to_next_access):
        # self.process_stream_index = process_stream_index
        self.frame_index_in_memory = frame_index_in_memory
        self.distance_to_next_access = distance_to_next_access

# class LRUItem(BaseFrame):
#     last_update = None
#     def __init__(self, number, name):
#         super().__init__(number, name)
#         self.last_update = datetime.now()
#
#     def update(self):
#         self.last_update = datetime.now()
