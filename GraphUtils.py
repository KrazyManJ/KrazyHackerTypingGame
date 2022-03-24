from pygame import gfxdraw, Rect, freetype


def draw_rect(surface, x, y, width, height, color: tuple[int, int, int], thickness, invert: bool = False) -> Rect:
    if invert:
        rect = Rect(x + thickness, y + thickness, width - thickness * 2, height - thickness * 2)
        gfxdraw.box(surface, rect, color)
        return rect
    else:
        rect = Rect(x, y, width, height)
        for i in range(round(thickness)):
            gfxdraw.rectangle(surface, rect, color)
            rect.x += 1
            rect.y += 1
            rect.width -= 2
            rect.height -= 2
        return rect


def draw_text_f(surface, font, text, size, rect, color):
    ft = freetype.SysFont(font, size)
    r = ft.get_rect(text, size=size)
    r.center = rect.center
    ft.render_to(surface, r, text, color)