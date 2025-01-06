import cv2
import numpy as np

'''
相似度检测
'''

FLANN_INDEX_KDTREE = 1 # SIFT 用这个
FLANN_INDEX_LSH = 6 # ORB 用这个

MIN_MATCH_COUNT = 10 # 控制匹配点的数量


def detect_similarity_images_with_sift(images, query_image):
    for image in images:
        if (detect_similarity_with_sift(query_image, image)):
            break
        # if (detect_similarity_with_orb(query_image, image)):
        #     break


def detect_similarity_with_sift(image1, image2):
    """ 使用 SIFT 描述符检测图像相似度 并使用 FLANN 匹配器 """
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    # 用SIFT找到关键点和描述符
    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # ＃根据Lowe的比率测试存储所有符合条件的匹配项
    good = []
    for tup in matches:
        if tup[0].distance < 0.7 * tup[1].distance:
            good.append(tup[0])

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        h, w = image1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, m)
        image2 = cv2.polylines(image2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matches_mask = None

    draw_params = dict(matchColor=(0, 255, 0),  # 用绿色绘制匹配
                       singlePointColor=None,
                       matchesMask=matches_mask,  # 只绘制内部点
                       flags=2)

    img3 = cv2.drawMatches(image1, kp1, image2, kp2, good, None, **draw_params)
    cv2.imshow("Image", img3)
    k = cv2.waitKey()
    cv2.destroyAllWindows()
    return k == 27

def detect_similarity_with_orb(image1, image2):
    """ 使用 ORB 描述符检测图像相似度 并使用 BF 匹配器"""
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)

    # """ 使用汉明距离作为相似度度量 """
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # matches = bf.match(des1, des2)
    # matches = sorted(matches, key=lambda x: x.distance)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 根据Lowe的比率测试存储所有符合条件的匹配项
    good = []
    for tup in matches:
        if tup[0].distance < 0.7 * tup[1].distance:
            good.append(tup[0])

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        h, w = image1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, m)
        image2 = cv2.polylines(image2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matches_mask = None

    draw_params = dict(matchColor=(0, 255, 0),  # 用绿色绘制匹配
                       singlePointColor=None,
                       matchesMask=matches_mask,  # 只绘制内部点
                       flags=2)

    img3 = cv2.drawMatches(image1, kp1, image2, kp2, good, None, **draw_params)
    cv2.imshow("Image", img3)
    k = cv2.waitKey()
    cv2.destroyAllWindows()
    return k == 27
