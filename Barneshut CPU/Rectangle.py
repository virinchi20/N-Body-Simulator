class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, body):
        body_x = body.x
        body_y = body.y
        return (
            body_x >= self.x - self.w and
            body_x < self.x + self.w and
            body_y >= self.y - self.h and
            body_y < self.y + self.h
        )
