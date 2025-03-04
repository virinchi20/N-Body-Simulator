class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, body):
        body_x = body.position[0]
        body_y = body.position[1]
        return (
            body_x > self.x - self.w and
            body_x < self.x + self.w and
            body_y > self.y - self.h and
            body_y < self.y + self.h
        )
