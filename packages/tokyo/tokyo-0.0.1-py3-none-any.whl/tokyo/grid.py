import sdl2
import sdl2.ext

# Classic DOS 16 colors (RGB)
DOS_COLORS = [
    (0, 0, 0),  # 0: Black (unused)
    (0, 0, 170),  # 1: Blue
    (0, 170, 0),  # 2: Green
    (0, 170, 170),  # 3: Cyan
    (170, 0, 0),  # 4: Red
    (170, 0, 170),  # 5: Magenta
    (170, 85, 0),  # 6: Brown
    (170, 170, 170),  # 7: Light Gray
    (85, 85, 85),  # 8: Dark Gray
    (85, 85, 255),  # 9: Bright Blue
    (85, 255, 85),  # 10: Bright Green
    (85, 255, 255),  # 11: Bright Cyan
    (255, 85, 85),  # 12: Bright Red
    (255, 85, 255),  # 13: Bright Magenta
    (255, 255, 85),  # 14: Yellow
    (255, 255, 255),  # 15: White
    (0, 0, 0),  # 16: Another Black or user-defined
]


class TokyoGrid:
    def __init__(self, width=800, height=600, cell_size=8, title="Tokyo Grid"):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size

        sdl2.ext.init()
        self.window = sdl2.ext.Window(title, size=(self.width, self.height))
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.clear()

    def clear(self):
        self.renderer.color = 0, 0, 0
        self.renderer.clear()

    def put_pixel(self, x, y, color_index: int):
        if not (1 <= color_index <= 16):
            raise ValueError("Color index must be between 1 and 16")
        if not (0 <= x < self.grid_width) or not (0 <= y < self.grid_height):
            return

        r, g, b = DOS_COLORS[color_index]
        self.renderer.color = r, g, b

        px = x * self.cell_size
        py = y * self.cell_size
        self.renderer.fill((px, py, self.cell_size, self.cell_size))

    def render(self):
        self.renderer.present()

    def run_until_closed(self):
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
        sdl2.ext.quit()
