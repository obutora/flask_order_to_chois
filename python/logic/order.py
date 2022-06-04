class Order:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def toJson(self):
        return {
            "name":self.name,
            "value":self.value
        }