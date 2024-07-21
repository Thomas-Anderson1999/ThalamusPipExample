
import numpy as np
import cv2 as cv
import cv2

def get_SIFT_mathching(img1, img2, dist_opt=0.7): #input, grayscale
    # Initiate SIFT detector
    sift = cv.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    match_list = []
    for i, (m, n) in enumerate(matches):
        if m.distance < dist_opt * n.distance:
            match_list.append([kp1[i].pt, kp2[m.trainIdx].pt])

    return match_list


def show_matching(img1, img2, match_list):
    szh = max([img1.shape[0], img2.shape[0]])
    szx1 = img1.shape[1]
    szx2 = img2.shape[1]

    resimg = np.zeros((szh, szx1+szx2), np.uint8)
    resimg[0:szh, 0:szx1] = img1
    resimg[0:szh, szx1:szx1+szx2] = img2

    resimg = cv2.cvtColor(resimg, cv2.COLOR_GRAY2BGR)
    for idx, match in enumerate(match_list):
        x1 = int(match[0][0])
        y1 = int(match[0][1])

        x2 = int(match[1][0])
        y2 = int(match[1][1])
        x2 += szx1

        if idx % 3 == 0:
            cv2.line(resimg, (x1, y1), (x2, y2), (0, 0, 255), 1)
        if idx % 3 == 1:
            cv2.line(resimg, (x1, y1), (x2, y2), (0, 255, 0), 1)
        if idx % 3 == 2:
            cv2.line(resimg, (x1, y1), (x2, y2), (255, 0, 0), 1)

    return resimg


if __name__ == '__main__':
    img1 = cv.imread('act_scene.png', cv.IMREAD_GRAYSCALE)  # queryImage
    img2 = cv.imread('gen_scene.png', cv.IMREAD_GRAYSCALE)  # trainImage

    match_list = get_SIFT_mathching(img1, img2)
    resimg = show_matching(img1, img2, match_list)

    cv2.imshow("resimg", resimg)

    cv2.waitKey(0)
