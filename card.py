class Card:
    def __init__(self, colour, shape, number, shading, uid):
        self.colour = colour
        self.shape = shape
        self.number = number
        self.shading = shading
        self.uid = uid

    def __str__(self):
        return f"{self.colour}, {self.shape}, {self.number}, {self.shading}"