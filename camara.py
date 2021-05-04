import cv2
cap = cv2.VideoCapture(0)
print("camara is opening")
#while True:
ret, frame = cap.read()

const = 50
edge = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
edge = cv2.Laplacian(frame, cv2.CV_16S, ksize=3)
cv2.imshow("camera", frame)
key = cv2.waitKey(0)
if key == ord('q'):
    cv2.destroyAllWindows()
       # break