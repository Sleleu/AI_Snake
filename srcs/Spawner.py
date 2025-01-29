import random

class Spawner:
    
    @staticmethod
    def snake_spawn(snake_size: int, grid_size: int, directions: dict[str, tuple]):
        assert snake_size <= grid_size, "Snake size can't be greater than grid size"
        rand = lambda: random.randint(0, grid_size - 1)

        while True:
            head_x, head_y = rand(), rand()
            snake = [[head_y, head_x]]
            
            valid_directions = []
            for dir_name, (dy, dx) in directions.items():
                new_y = head_y + dy * (snake_size - 1)
                new_x = head_x + dx * (snake_size - 1)
                if 0 <= new_y < grid_size and 0 <= new_x < grid_size:
                    valid_directions.append((dir_name, dy, dx))

            if not valid_directions:
                continue

            body_spawn_dir, dy, dx = random.choice(valid_directions)
            
            # Build snake
            for _ in range(1, snake_size):
                head_y += dy
                head_x += dx
                snake.append([head_y, head_x])

            # Inverse of body spawn direction, to have a natural first direction
            snake_direction = {"TOP": "BOTTOM", "BOTTOM": "TOP", "LEFT": "RIGHT", "RIGHT": "LEFT"}[body_spawn_dir]

            return snake, snake_direction

    @staticmethod
    def fruit_spawn(snake, green_lst, red_lst, grid_size):
        all_occupied = {tuple(pos) for pos in (snake + green_lst + red_lst)}
        all_positions = {(y, x) for y in range(grid_size) for x in range(grid_size)}
        available_positions = list(all_positions - all_occupied)
        
        if available_positions:
            y, x = random.choice(available_positions)
            return [y, x]
        return None
