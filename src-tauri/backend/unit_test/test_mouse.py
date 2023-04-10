from utils.mouse_utils import MouseUtils
from time import sleep

for i in range (0, 1):
    MouseUtils.move_and_click_point(
        750, 600, "home_back", mouse_clicks=100
    )
    sleep(1)

