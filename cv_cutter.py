import cv2
import numpy as np


def find_centers(pic, background=False):
    if type(pic) == str:
        img = cv2.imread(pic)
    else:
        img = pic

    cv2.imshow('Pic', img)

    h, w = img.shape[:2]
    # Get grayscale image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Get binary image
    img_binarized = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # copy one
    img_binarized[img_gray >= 100] = 0
    img_binarized[img_gray < 100] = 1

    positions = [[0], [0], [0], [0]]

    area = [0]  # Area of single pic
    cir_center = []
    color = (255, 0, 0)

    num, img_labeled = cv2.connectedComponents(img_binarized, connectivity=8)
    num -= 1

    if num > 0:
        print('#'*62)
        print('#')
        for i in range(1, num+1):
            position = GetPosition(img_labeled, i)
            positions[0].append(position[0])  # top
            positions[1].append(position[1])  # bottom
            positions[2].append(position[2])  # right
            positions[3].append(position[3])  # left
            area.append(GetArea(img_labeled, i))
        num = simplefilter(img_labeled, area, positions, num)
        centers = []
        for i in range(1, num+1):
            center_x = int((positions[2][i]+positions[3][i])/2)
            center_y = int((positions[0][i]+positions[1][i])/2)
            centers.append([center_x,center_y])
            print('#\tCenter', i, ':(', center_x, ',', center_y, ')')
            cir_center.append([center_x, center_y])
            cv2.rectangle(img,(int((center_x-(positions[2][i]-positions[3][i])/2)*1)-5,int((center_y-(positions[0][i]-positions[1][i])/2)*1)-5),
                          (int((center_x+(positions[2][i]-positions[3][i])/2)*1)+5,int((center_y+(positions[0][i]-positions[1][i])/2)*1)+5), (255,0,0), 2)
            cv2.circle(img, (center_x, center_y), 6, color, 2)

        print('#')
        print('#'*62)
        cv2.imshow('Output', img)
        return centers
    else:
        return None


# ***********************************************
# Function Name      GetPosition
# Function           Find the aim's position, to top bottom right left
# Input              find the pixel named num
# ***********************************************
def GetPosition(m_pData, num):
    position = [0] * 4   # top, bottom, right, left

    index_label = np.argwhere(m_pData == num)
    position[1] = np.min(index_label[..., 0])
    position[0] = np.max(index_label[..., 0])
    position[3] = np.min(index_label[..., 1])
    position[2] = np.max(index_label[..., 1])

    return position


#***********************************************
# Function Name      GetArea
#***********************************************
def GetArea(m_pData, num):
    return np.sum(m_pData == num)


# ***********************************************
# * Function Name      SimpleFilter
# ***********************************************
def simplefilter(m_pData, area, positions, num, scaling=1):
    R = []
    R_num = 0
    newtop = [0]
    newbottom = [0]
    newright = [0]
    newleft = [0]
    for i in range(1, num+1):
        if True:
            if area[i] < 102400 and area[i] > 10:
                R.append(i)
                newtop.append(positions[0][i])
                newbottom.append(positions[1][i])
                newright.append(positions[2][i])
                newleft.append(positions[3][i])
                R_num += 1
        # Remove no use tag
        if i not in R:
            m_pData[m_pData == i] = 0

    # Revalue all of the pixel
    for k in range(R_num):
        m_pData[m_pData == R[k]] = k+1

    # new_top1 new_top2 new_top3  top4 top5 top6
    for i in range(1, R_num+1):
        positions[0][i] = newtop[i]
        positions[1][i] = newbottom[i]
        positions[2][i] = newright[i]
        positions[3][i] = newleft[i]
    # newtop1 newtop2 newtop3
    for i in range(num - R_num):
        positions[0].pop()
        positions[1].pop()
        positions[2].pop()
        positions[3].pop()
    return R_num


if __name__ == '__main__':
    pic_file = r"test.bmp"
    import time
    t0 = time.time()
    find_centers(pic_file)
    t = time.time() - t0
    print("Time:", t)
    cv2.waitKey()
