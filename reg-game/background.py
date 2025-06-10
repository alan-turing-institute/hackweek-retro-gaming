from pygame import Surface, image


class BackgroundView:
    def __init__(self, img_path: str):
        self.image = image.load(img_path)

    def render(self, surface: Surface):
        surface.blit(self.image, (0, 0))
