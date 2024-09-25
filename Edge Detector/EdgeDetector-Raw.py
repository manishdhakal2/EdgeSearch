import cv2
import numpy as np

img=r"" #Your Image Path Goes Here
img_=cv2.imread(img,cv2.IMREAD_GRAYSCALE)

save_path_h = r"" #Your result Path Goes Here (Horizontal Edge)
save_path_v = r"" #Your result Path Goes Here (Vertical Edge)

vertical_kernel=np.array([[0.25,0,-0.25],
                 [1,0,-1],
                 [1.75,0,-1.75]])
horizontal_kernel=np.array([[1,1,1],
                            [0,0,0],
                            [-1,-1,-1]])

img_1=cv2.filter2D(img_,-1,vertical_kernel)
cv2.imwrite(save_path_v,img_1)
img_2=cv2.filter2D(img_,-1,horizontal_kernel)
cv2.imwrite(save_path_h,img_2)
