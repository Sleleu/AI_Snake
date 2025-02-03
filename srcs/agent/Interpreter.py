from settings import R_COLLISION, R_GREEN_FRUIT, R_RED_FRUIT, GRID_SIZE


class Interpreter:
    @staticmethod
    def get_state(snake: list[list],
                  green_fruits: list[list],
                  red_fruits: list[list]
                  ) -> list:
        """Returns current game state as input for neural network.

        Args:
            `snake`: Snake coordinates [[y,x], ...]
            `green_fruits`: Green fruit coordinates [[y,x], ...]
            `red_fruits`: Red fruit coordinates [[y,x], ...]

        Returns:
            `List` of 20 values [0-1]:
            - [0-3]: Wall dist in directions [up,down,left,right]
            - [4-7]: Green fruit dist in directions [up,down,left,right]
            - [8-11]: Red fruit dist in directions [up,down,left,right]
            - [12-15]: Body dist in directions [up,down,left,right]
            - [16-19]: Collision flags [up,down,left,right] (0 or 1)
        """
        snake_head = snake[0]

        def get_collision_dist(direction: list):
            """Returns normalized distance [0-1] to wall in given direction."""
            y, x = snake_head
            dy, dx = direction
            distance = 0

            while 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                y += dy
                x += dx
                distance += 1
            return distance / GRID_SIZE

        def get_item_dist(direction, items_lst):
            """Returns normalized Manhattan distance [0-1] to nearest item.
            Returns 1 if no item in that direction."""
            y, x = snake_head
            dy, dx = direction
            distance = 1

            while 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
                if [y, x] in items_lst:
                    dist_y = abs(y - snake_head[0])
                    dist_x = abs(x - snake_head[1])
                    distance = (dist_y + dist_x) / GRID_SIZE
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
    def get_reward(snake_head: list[int],
                   snake_body: list[list],
                   green_fruits: list[list],
                   red_fruits: list[list]
                   ) -> tuple[int, bool]:
        """Returns reward and game over state based on snake's position.

        Args:
            `snake_head`: Head coordinates [y,x]
            `snake_body`: Snake coordinates [[y,x], ...]
            `green_fruits`: Green fruit coordinates [[y,x], ...]
            `red_fruits`: Red fruit coordinates [[y,x], ...]

        Returns:
            `tuple`: (reward, game_over)
        """
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
