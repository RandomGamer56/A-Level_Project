import random

class CellularAutomataMap(object):
    def __init__(self, width, height, spawn_chance):
        self.width = width
        self.height = height
        self.spawn_chance = spawn_chance
        self.map = []

    def create_map(self):

        # Create Empty Map

        for row in range(0, self.height):
            self.map.append([])
            for col in range(0, self.width):
                self.map[row].append(0)

        # Randomise Map
        for row in range(5, self.height - 5):
            for col in range(5, self.width - 5):
                if (random.randint(0, 100)) / 100 <= self.spawn_chance:
                    self.map[row][col] = 60
                else:
                    self.map[row][col] = 10

        #self.print_map()

    def generation(self,iteration):
        for i in range(0,iteration):

            new_map = []
            for row in range(0, self.height):
                new_map.append([])
                for col in range(0, self.width):
                    new_map[row].append(0)


            for row in range(1, self.height - 1):
                for col in range(1, self.width - 1):


                    count = 0
                    for row_offset in range(-1, 2):
                        for col_offset in range(-1, 2):
                            row_dif = row + row_offset
                            col_dif = col + col_offset
                            count += self.map[row_dif][col_dif]

                    count -= self.map[row][col]
                    mean = count // 8

                    if mean < 40 and mean-self.map[row][col] < 0:
                        new_map[row][col] = self.map[row][col] - random.randint(0,self.map[row][col] - mean)
                    elif mean < 40 and mean-self.map[row][col] > 0:
                        new_map[row][col] = self.map[row][col] + random.randint(0, mean - self.map[row][col])
                    elif self.map[row][col] > mean:
                        new_map[row][col] = self.map[row][col] + random.randint(-10,10)
                    else:
                        new_map[row][col] = self.map[row][col] + random.randint(0,mean//5)

            self.map = new_map
            #self.print_map()
