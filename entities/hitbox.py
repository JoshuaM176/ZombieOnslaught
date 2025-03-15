class HitBox:
    
    def __init__(self,X, Y, x, y, w, l):
        self.x = [X, x]
        self.y = [Y, y]
        self.size = (w, l)

    def get(self):
        return (sum(self.x), sum(self.y), sum(self.x, self.size[0]), sum(self.y, self.size[1]))
    
    def update(self, X, Y):
        self.x[0] = X
        self.y[0] = Y 
        