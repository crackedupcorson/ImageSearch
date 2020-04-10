import numpy as np
import cv2
import glob
import shutil
import gc


class FeatureMatching:

    def compare_photos(self):
        MIN_MATCH_COUNT = 20  # Min amount of keypoints matched, for image considered to be alike.

        original_image = cv2.imread('original/origin.jpg', 0)
        for image in glob.iglob("compare/*.jpg"):

            comparison_image = cv2.imread(image)

            # Initiate SIFT detector
            orb = cv2.ORB_create()

            # find the keypoints and descriptors with SIFT
            kp1, des1 = orb.detectAndCompute(original_image, None)
            kp2, des2 = orb.detectAndCompute(comparison_image, None)

            # FLANN parameters
            #FLANN_INDEX_KDTREE = 1
            #index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            #search_params = dict(checks=50)  # or pass empty dictionary
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)


            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
            # If the amount of matches is greater than the minimal match count(accepted amount of matches)
            if len(good_matches) >= MIN_MATCH_COUNT:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, 0, 5.0)  # Find homography
                matchesMask = mask.ravel().tolist()

                h, w = original_image.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)

                comparison_image = cv2.polylines(comparison_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            else:
                print("Not enough matches ({}) found. Minimum is {}".format(len(good_matches), MIN_MATCH_COUNT))
                matchesMask = None

            draw_params = dict(matchColor=(255, 0, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)
            # Draw the matches.
            cv2.drawMatches(original_image, kp1, comparison_image, kp2, good_matches, None, **draw_params)
            amount = len(good_matches)
            if amount >= MIN_MATCH_COUNT:
                gc.collect()
                destination = 'compare2/'
                shutil.copy(image, destination)
