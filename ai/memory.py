class Memory:
    def __init__(self):
        self.history = []

    def save_interaction(self, data):
        self.history.append(data)

    def get_history(self):
        return self.history