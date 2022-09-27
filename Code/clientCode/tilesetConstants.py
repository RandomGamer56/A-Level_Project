# connections = [top,left,right,bottom]

def pick_tile(main,sub,connections):
    if main == "forest":
        if sub == "grass":
            if connections == [0,0,0,1]:
                return [6,2]
            elif connections == [0,0,1,0]:
                return [7,1]
            elif connections == [0,0,1,1]:
                return [7,2]
            elif connections == [0,1,0,0]:
                return [5,1]
            elif connections == [0,1,0,1]:
                return [5,2]
            elif connections == [0,1,1,0]:
                return [4,1]
            elif connections == [0,1,1,1]:
                return [4,2]
            elif connections == [1,0,0,0]:
                return [6,0]
            elif connections == [1,0,0,1]:
                return [2,0]
            elif connections == [1,0,1,0]:
                return [7,0]
            elif connections == [1,0,1,1]:
                return [3,0]
            elif connections == [1,1,0,0]:
                return [5,0]
            elif connections == [1,1,0,1]:
                return [1,0]
            elif connections == [1,1,1,0]:
                return [4,0]
            elif connections == [1,1,1,1]:
                return [6,1]






FOREST_GRASS_TOP_LEFT_RIGHT_BOTTOM = [0, 0]
FOREST_GRASS_TOP_LEFT_BOTTOM = [1, 0]
FOREST_GRASS_TOP_BOTTOM = [2, 0]
FOREST_GRASS_TOP_RIGHT_BOTTOM = [3, 0]
FOREST_GRASS_TOP_LEFT_RIGHT = [4, 0]
FOREST_GRASS_TOP_LEFT = [5, 0]
FOREST_GRASS_TOP = [6, 0]
FOREST_GRASS_TOP_RIGHT = [7, 0]
FOREST_GRASS_TOP_LEFT_RIGHT_BOTTOM = [0,1]
