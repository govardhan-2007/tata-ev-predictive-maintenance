from collections import deque


class SequenceBuffer:

    def __init__(self, sequence_length=50):
        self.buffer = deque(maxlen=sequence_length)

    def add(self, sample):
        self.buffer.append(sample)

    def ready(self):
        return len(self.buffer) == self.buffer.maxlen

    def get_sequence(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()