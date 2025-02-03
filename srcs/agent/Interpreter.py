from settings import R_COLLISION, R_GREEN_FRUIT, R_RED_FRUIT, GRID_SIZE

class Interpreter:
    @staticmethod
    def get_state(snake, green_fruits, red_fruits) -> list:
        snake_head = snake[0]
        def get_collision_dist(direction):
            y, x = snake_head
            dy, dx = direction
            distance = 0

            while 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                y += dy
                x += dx
                distance += 1
            return distance / GRID_SIZE

        def get_item_dist(direction, items_lst):
            y, x = snake_head
            dy, dx = direction
            distance = 1

            while 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                if [y, x] in items_lst:
                    distance = (abs(y - snake_head[0]) + abs(x - snake_head[1])) / GRID_SIZE
                    break
                y += dy
                x += dx
            return distance

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        state = []
        y, x = snake_head
        direct_collisions = [
            1 if (y-1 < 0 or [y-1, x] in snake[1:]) else 0,
            1 if (y+1 >= GRID_SIZE or [y+1, x] in snake[1:]) else 0,
            1 if (x-1 < 0 or [y, x-1] in snake[1:]) else 0,
            1 if (x+1 >= GRID_SIZE or [y, x+1] in snake[1:]) else 0
        ]
        
        for direction in directions:
            state.append(get_collision_dist(direction))
        for direction in directions:
            state.append(get_item_dist(direction, green_fruits))
        for direction in directions:
            state.append(get_item_dist(direction, red_fruits))
        for direction in directions:
            state.append(get_item_dist(direction, snake[1:]))
        state.extend(direct_collisions)
        return state

    @staticmethod
    def get_reward(snake_head, snake_body, green_fruits, red_fruits) -> tuple[float, bool]:
        gameover = True
        Ok = False

        if snake_head in snake_body[1:]:
            return R_COLLISION, gameover
        elif GRID_SIZE in snake_head or -1 in snake_head:
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
