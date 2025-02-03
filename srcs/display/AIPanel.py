from .Colors import Colors as Col
from settings import *
import pygame as pg


class AIPanel:
    # State panel const
    STATE_PANEL_WIDTH = 310
    STATE_PANEL_HEIGHT = 200
    STATE_ROW_HEIGHT = 30
    STATE_DIR_WIDTH = 60
    
    # Neural network const
    NN_WIDTH = 475
    NN_HEIGHT = min(HEIGHT - 250, 400) 
    NN_LAYER_SPACING = 100
    NN_INPUT_SPACING = 15
    NN_OUTPUT_SPACING = None
    
    # Other
    CATEGORIES = ["Wall", "Green fruit", "Red fruit", "Body", "Collisions"]
    DIRECTIONS = ["TOP", "BOTTOM", "LEFT", "RIGHT"]
    BASE_COLORS = [
        Col.PG_YELLOW,    # Wall
        Col.PG_GREEN,     # Green fruit
        Col.PG_RED,       # Red fruit
        Col.PG_MAGENTA,   # Body
        Col.PG_CYAN       # Collisions
    ]

    @classmethod
    def get_gradient_color(cls, value, category=None):
        value = max(0, min(1, value))
        
        # For output neuron
        if category is None:
            threshold = 0.5
            if value <= threshold:
                normalized = value / threshold
                return (255, int(255 * normalized), 0)
            else:
                normalized = (value - threshold) / (1 - threshold)
                return (int(255 * (1 - normalized)), 255, 0)

        base_color = cls.BASE_COLORS[category]
        inactive = tuple(min(255, int(c * 1.3)) for c in Col.BG_COLOR)
        if category < 4: # inverse color for distance neurons
            value = 1 - value
        value = max(0.15, min(1, value)) # brighter to see inactive neurons

        return tuple(int(c1 * value + c2 * (1 - value))
                     for c1, c2 in zip(base_color, inactive))

    @classmethod
    def draw_panel_background(cls, surface, x, y, width, height, title):
        # Border
        panel_rect = pg.Rect(x, y, width, height)
        pg.draw.rect(surface, Col.PG_WHITE, panel_rect, 1)

        # Title
        font = pg.font.Font(None, 24)
        title_surf = font.render(title, True, Col.PG_CYAN)
        title_rect = title_surf.get_rect(
            top=y + 5,
            centerx=x + width // 2
        )
        surface.blit(title_surf, title_rect)

    @classmethod
    def draw_state_direction(cls, surface, x, y):
        small_font = pg.font.Font(None, 16)
        for i, direction in enumerate(cls.DIRECTIONS):
            text = small_font.render(direction, True, Col.PG_CYAN)
            rect = text.get_rect(
                left=x + 80 + i * cls.STATE_DIR_WIDTH,
                top=y
            )
            surface.blit(text, rect)

    @classmethod
    def draw_state_category(cls, surface, x, y, row, category, values, is_ai):
        small_font = pg.font.Font(None, 16)
        
        # Category name
        cat_text = small_font.render(category, True, cls.BASE_COLORS[row])
        cat_rect = cat_text.get_rect(left=x + 10, top=y)
        surface.blit(cat_text, cat_rect)

        # Draw circle + value for each direction
        for col in range(len(cls.DIRECTIONS)):
            value = values[row * 4 + col]
            pos_x = x + 80 + col * cls.STATE_DIR_WIDTH
            
            color = (cls.get_gradient_color(value, row) 
                    if is_ai else Col.PG_RED)
            pg.draw.circle(surface, color, (pos_x + 10, y + 8), 8)

            # Print ':.2f' if distance or 1/0 for collision
            format_str = "{}" if row == 4 else "{:.2f}"

            text = small_font.render(format_str.format(value), True, Col.PG_WHITE)
            surface.blit(text, text.get_rect(left=pos_x + 20, top=y))

    @classmethod
    def draw_neural_state(cls, surface, state, is_ai_control):
        panel_x = WIDTH - MARGIN * 5
        panel_y = 0
        
        # Only 0 values if player (AI brain off)
        if not is_ai_control:
            state = [0] * len(state)

        cls.draw_panel_background(
            surface, panel_x, panel_y,
            cls.STATE_PANEL_WIDTH, cls.STATE_PANEL_HEIGHT,
            "Snake State"
        )

        header_y = panel_y + 35
        cls.draw_state_direction(surface, panel_x, header_y)

        start_y = header_y + 20
        for row, category in enumerate(cls.CATEGORIES):
            cls.draw_state_category(
                surface, panel_x,
                start_y + row * cls.STATE_ROW_HEIGHT,
                row, category, state, is_ai_control
            )

    @classmethod
    def draw_input_layer(cls, surface, x, y, state, is_ai):
        neurons = []
        for i, value in enumerate(state):
            pos_y = y + (i * cls.NN_INPUT_SPACING)
            category_index = i // 4
            color = (cls.get_gradient_color(value, category_index)
                    if is_ai else Col.PG_RED)
            pg.draw.circle(surface, color, (x, pos_y), 6)
            neurons.append((x + 2, pos_y))
        return neurons

    @classmethod
    def draw_hidden_layers(cls, surface, x, y, height):
        font = pg.font.Font(None, 24)
        
        # First hidden layer
        text = font.render("Hidden (128)", True, Col.PG_WHITE)
        text_rotate = pg.transform.rotate(text, -90)
        surface.blit(text_rotate, text_rotate.get_rect(center=(x, y + height//2)))
        
        # Second hidden layer
        x2 = x + cls.NN_LAYER_SPACING
        text = font.render("Hidden (64)", True, Col.PG_WHITE)
        text_rotate = pg.transform.rotate(text, -90)
        surface.blit(text_rotate, text_rotate.get_rect(center=(x2, y + height//2)))
        
        # Border of hidden layers
        for layer_x in (x, x2):
            rect = pg.Rect(layer_x - 20, y + 60, 40, height - 120)
            pg.draw.rect(surface, Col.PG_CYAN, rect, 1)
            
        return x2

    @classmethod
    def draw_output_layer(cls, surface, x, y, height, values, is_ai):
        small_font = pg.font.Font(None, 20)
        output_start_y = y + height//2 - (height // 6)
        neurons = []
        
        max_val = max(values) if values else 0
        
        for i, (action, value) in enumerate(zip(cls.DIRECTIONS, values)):
            pos_y = output_start_y + (i * (height // 6))
            
            # To protect from division by 0
            norm_val = value / max_val if max_val > 0 else 0

            color = (cls.get_gradient_color(norm_val, None)
                    if is_ai else Col.PG_RED)
            pg.draw.circle(surface, color, (x, pos_y), 8)
            neurons.append((x, pos_y))

            text_color = Col.PG_WHITE
            if value == max(values):
                text_color = Col.PG_CYAN
            text = small_font.render(f"{action}: {value:.2f}", True, text_color)
            surface.blit(text, text.get_rect(left=x + 15, centery=pos_y))
            
        return neurons

    @classmethod
    def draw_neural_network(cls, surface, state, action_values, is_ai_control):
        nn_x = WIDTH - MARGIN * 5
        nn_y = 220
        
        if not is_ai_control:
            action_values = [0] * len(action_values)

        # Background and title
        cls.draw_panel_background(
            surface, nn_x, nn_y,
            cls.NN_WIDTH, cls.NN_HEIGHT,
            "Neural Network"
        )

        input_x = nn_x + 50
        hidden1_x = input_x + cls.NN_LAYER_SPACING
        input_neurons = cls.draw_input_layer(
            surface, input_x, nn_y + 60,
            state, is_ai_control
        )
        hidden2_x = cls.draw_hidden_layers(
            surface, hidden1_x, nn_y,
            cls.NN_HEIGHT
        )
        output_x = hidden2_x + cls.NN_LAYER_SPACING
        output_neurons = cls.draw_output_layer(
            surface, output_x, nn_y,
            cls.NN_HEIGHT, action_values,
            is_ai_control
        )

        # Lines
        mid_y = nn_y + cls.NN_HEIGHT//2
        for in_pos in input_neurons:
            pg.draw.line(surface, Col.PG_CYAN, in_pos,
                        (hidden1_x - 20, mid_y), 1)
        
        pg.draw.line(surface, Col.PG_CYAN,
                    (hidden1_x + 20, mid_y),
                    (hidden2_x - 20, mid_y), 1)
        
        for out_pos in output_neurons:
            pg.draw.line(surface, Col.PG_CYAN,
                        (hidden2_x + 20, mid_y),
                        (out_pos[0] - 8, out_pos[1]), 2)
