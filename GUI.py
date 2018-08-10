import snake
import cv2

clicks = list()


def activate_GUI():
    background = cv2.imread("background.png", 1)
    cv2.namedWindow('image')
    cv2.setMouseCallback("image", mouse_callback)
    cv2.imshow("image",background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    snake.run(6)

def mouse_callback(event,x,y,flags,params):
    if event == 2 or event == 1:
        global clicks
        clicks.append([x,y])

if __name__ == '__main__':
    activate_GUI()