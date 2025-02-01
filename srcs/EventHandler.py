import pygame as pg

class EventHandler:
    
    @staticmethod
    def handle(visual, snakeAgent, change_direction):
        if visual != "on":
            return False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True # if game need to stop

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    snakeAgent.save_model("manual_save.pt")
                    print("Model saved as 'manual_save.pt'")
                else:
                    change_direction(event.key)

        return False