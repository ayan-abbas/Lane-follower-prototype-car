import cv2
import numpy as np
import math
import time

def lane_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    height, width = image.shape[:2]
    mask = np.zeros_like(edges)
    vertices = np.array([[(0, height), (width / 2, height * 2/3), (width, height)]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, 255)
    roi = cv2.bitwise_and(edges, mask)
    cv2.polylines(image, [vertices], isClosed=True, color=(0, 255, 255), thickness=2)  # Yellow triangle
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 20, minLineLength=50, maxLineGap=100)

    if lines is not None:
        line_image = np.zeros_like(image)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        left_lines = []
        right_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 == x1:  # check if the line is vertical
                continue  # skip to the next line in the loop
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            if slope < 0:
                left_lines.append((slope, intercept))
            else:
                right_lines.append((slope, intercept))

        if left_lines:
            left_lane = np.average(left_lines, axis=0)
            draw_lane_line(image, left_lane)

        if right_lines:
            right_lane = np.average(right_lines, axis=0)
            draw_lane_line(image, right_lane)

        if left_lane is not None and right_lane is not None:
            left_x_bottom = int((height - left_lane[1]) / left_lane[0])
            right_x_bottom = int((height - right_lane[1]) / right_lane[0])
            mid_x_bottom = int((left_x_bottom + right_x_bottom) / 2)
            cv2.circle(image, (mid_x_bottom, height), 10, (0, 0, 255), -1)
            left_x_middle = int(((height / 2) - left_lane[1]) / left_lane[0])
            right_x_middle = int(((height / 2) - right_lane[1]) / right_lane[0])
            mid_x_middle = int((left_x_middle + right_x_middle) / 2)
            cv2.circle(image, (mid_x_middle, int(height / 2)), 10, (0, 0, 255), -1)
            cv2.line(image, (mid_x_bottom, height), (mid_x_middle, int(height / 2)), (255, 255, 0), 5)
            steering_angle = (math.atan2(height - int(height / 2), mid_x_middle - mid_x_bottom) * 180 / math.pi)-90
            print(steering_angle)


    return image


def draw_lane_line(image, lane):
    slope, intercept = lane
    y1 = image.shape[0]
    y2 = int(y1 * 0.6)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 10)


video = cv2.VideoCapture("road12.webm")
#video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Cannot open camera")
    exit()

timer = time.time()


while True:
    if time.time() - timer >= 0.024:
        try:
            ret, frame = video.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            output = lane_detection(frame)

            cv2.imshow('output', output)
            if cv2.waitKey(1) == ord('q'):
                break

        except:
            pass
        timer = time.time()
video.release()
cv2.destroyAllWindows()
