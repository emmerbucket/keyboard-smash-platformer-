import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "epic platformer"

class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()