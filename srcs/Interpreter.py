from ..settings import R_COLLISION, R_GREEN_FRUIT, R_RED_FRUIT, R_WIN

class Interpreter:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def get_state(self, snake_head, snake_body, green_fruits, red_fruits) -> list:
        def get_collision_dist(direction):
            y, x = snake_head
            dy, dx = direction
            distance = 0

            while 0 <= y < self.grid_size and 0 <= x < self.grid_size:
                y += dy
                x += dx
                distance += 1
            return distance / self.grid_size

        def get_item_dist(direction, items_lst):
            y, x = snake_head
            dy, dx = direction
            distance = 1

            while 0 <= y < self.grid_size and 0 <= x < self.grid_size:
                if [y, x] in items_lst:
                    distance = (abs(y - snake_head[0]) + abs(x - snake_head[1])) / self.grid_size
                    break
                y += dy
                x += dx
            return distance

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        state = []
        
        for direction in directions:
            state.append(get_collision_dist(direction))
        for direction in directions:
            state.append(get_item_dist(direction, green_fruits))
        for direction in directions:
            state.append(get_item_dist(direction, red_fruits))
        for direction in directions:
            state.append(get_item_dist(direction, snake_body[1:]))
        return state

    def get_reward(self, snake_head, snake_body, green_fruits, red_fruits) -> tuple[float, bool]:
        gameover = True
        Ok = False
        
        if snake_head in snake_body[1:]:
            return R_COLLISION, gameover
        elif self.grid_size in snake_head or -1 in snake_head:
            return R_COLLISION, gameover
        elif snake_head in green_fruits:
            return R_GREEN_FRUIT, Ok
        elif snake_head in red_fruits:
            if len(snake_body) <= 1:
                gameover = True
                return R_COLLISION, gameover
            return R_RED_FRUIT, Ok
        else:
            return 0, Ok