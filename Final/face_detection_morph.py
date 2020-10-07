import cv2
import dlib
import json
import numpy as np
from PIL import Image
import scipy.spatial

# Take in user input
def match(fileName):
    img_name = fileName
    try:
        img = Image.open(img_name)
    except IOError:
        print("==========================================")
        print("ERROR: Image cannot be open. Example input: test.jpg")
        print("Loading provided image...")
        img_name = 'test1.jpg'
        pass

    # Image
    user_img = cv2.imread(img_name)
    img_copy = cv2.imread(img_name)

    # Find grayscale of image
    gray = cv2.cvtColor(user_img, cv2.COLOR_BGR2GRAY)

    # Extracting dlib's face detector and grab facial landmark
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("face_landmarks.dat")

    faces = detector(gray)

    # Capture the points on face
    # 1-17 on Jaw (left to right)
    # 18-22 on Left Eyebrow (left to right)
    # 23-27 on Right Eyebrow (left to right)
    # 28-31 on Nose Bridge (top to bottom)
    # 32-36 on Nose (left to right)
    # 37-42 on Left Eye (very left point to clockwise)
    # 43-48 on Right Eye (very left point to clockwise)
    # 49-60 on Outer Lip (very left point to clockwise)
    # 61-68 on Inner Lip (very left point to clockwise)

    jaw = []
    brow_l = []
    brow_r = []
    bridge = []
    nose = []
    eye_l = []
    eye_r = []
    lip_out = []
    lip_in = []
    all_coord = []

    for face in faces:
        landmark = predictor(gray, face)

        # Color and store face data
        count = 1
        for n in range(0,68):

            x = landmark.part(n).x
            y = landmark.part(n).y
            all_coord.append((x,y))

            if count <= 17: # Purple (Jaw)
                jaw.append((x,y))
                color = 255
                color1 = 0
                color2 = 100
            elif count <= 22: # Green (Left Eyebrow)
                brow_l.append((x,y))
                color = 100
                color1 = 255
                color2 = 170
            elif count <= 27: # Blue (Right Eyebrow)
                brow_r.append((x,y))
                color = 50
                color1 = 104
                color2 = 255
            elif count <= 31: # Light Blue (Nose Bridge)
                bridge.append((x,y))
                color = 235
                color1 = 169
                color2 = 169
            elif count <= 36: # Light Green (Nose)
                nose.append((x,y))
                color = 169
                color1 = 235
                color2 = 185
            elif count <= 42: # Light Blue (Left Eye)
                eye_l.append((x,y))
                color = 169
                color1 = 215
                color2 = 235
            elif count <= 48: # Pale Yellow (Right Eye)
                eye_r.append((x,y))
                color = 235
                color1 = 230
                color2 = 169
            elif count <= 60: # Light Blue (Outer Lip)
                lip_out.append((x,y))
                color = 255
                color1 = 204
                color2 = 153
            elif count <= 68: # Light Purple (Inner Lip)
                lip_in.append((x,y))
                color = 160
                color1 = 142
                color2 = 209
            count += 1

            cv2.circle(user_img, (x,y), 2, (color, color1, color2), -1)
        # Breaks after detecting the first face
        break

    # If Image size is too big
    #char_size = user_img.shape
    #if char_size[0] > 900 and char_size[1] > 900:
    #    char_img = cv2.resize(user_img, (0,0), None, .3, .3)

    # Store User Data into one list
    user_data = [jaw, brow_l, brow_r, bridge, nose, eye_l, eye_r, lip_out, lip_in]

    # ===========================
    # Debug Print Statements.
    # print("Jaw Coordinates:", jaw)
    # print("Left Brow Coordinates:", brow_l)
    # print("Right Brow Coordinates:", brow_r)
    # print("Bridge Coordinates:", bridge)
    # print("Nose Coordinates:", nose)
    # print("Left Eye Coordinates:", eye_l)
    # print("Right Eye Coordinates:", eye_r)
    # print("Outer Lip Coordinates:", lip_out)
    # print("Inner Lip Coordinates:", lip_in)
    # print("Number of Coordinates:",len(all_coord))
    # ========

    # Opening JSON file
    f = open('facedata.json')

    # Return JSON object as a dictionary
    data = json.load(f)

    # Array of Characters
    characters = []
    features = ["Jaw Coordinates", "Left Brow Coordinates","Right Brow Coordinates",\
                "Bridge Coordinates", "Nose Coordinates", "Left Eye Coordinates", \
                "Right Eye Coordinates", "Outer Lip Coordinates", "Inner Lip Coordinates"]
            # [jaw,     l_brow, r_brow, bridge, nose,   l_eye,  r_eye,  o_lip,  i_lip]
    weights = [0.25,    .1,     .1,     .04,    0.2,    0.45,    0.45,    0.3,   0.3]

    # Closest Comparision
    closest_character = ""
    closest_score = 99999

    # Iterating through the JSON to get Character's Name
    for character in data:
        characters.append(character)


    for name in characters:
        count = 0
        current_score = 0
        for feat in features:
            # print(name, feat) # debug
            compare = scipy.spatial.procrustes(user_data[count], data[name][feat])[-1]
            current_score += compare*weights[count]
            count += 1

        # Change closest character if better results
        if current_score < closest_score:
            closest_score = current_score
            closest_character = name
            #print(name,"is the closest with score of", closest_score)

    # Image of Chosen Character
    dic = 'disney-characters\ '
    dic = dic.rstrip()
    chosen_one = dic+closest_character+".jpg"
    #print(chosen_one)
    char_img = cv2.imread(chosen_one)

    # Output Character
    cv2.imwrite('output/char.jpg', char_img)

    all_coord2 = []
    # Draw points on Character
    for feat in features:
        for coord in data[closest_character][feat]:
            all_coord2.append(coord)
            cv2.circle(char_img, (coord[0],coord[1]), 4, (208,104,193), -1)

    # If Image size is too big
    new_char_img = cv2.imread(chosen_one)
    char_size = char_img.shape
    user_size = user_img.shape
    while char_size[0] > user_size[0] or char_size[1] > user_size[1]:
        char_img = cv2.resize(char_img, (0,0), None, .9, .9)
        new_char_img = cv2.resize(new_char_img, (0,0), None, .9, .9)
        for coord in all_coord2:
            coord[0] = int(coord[0]*(9/10))
            coord[1] = int(coord[1]*(9/10))
        char_size = char_img.shape



    # Closing file
    f.close()

    # Display Window
    # cv2.imshow("Char_img", char_img)
    # cv2.imshow("User_img", user_img)

    # Output Results
    cv2.imwrite('output/user_output.jpg', user_img)
    cv2.imwrite('output/char_output.jpg', char_img)


    def rect_contains(rect, point) :
        if point[0] < rect[0] :
            return False
        elif point[1] < rect[1] :
            return False
        elif point[0] > rect[2] :
            return False
        elif point[1] > rect[3] :
            return False
        return True

    # Draw a point
    def draw_point(img, p, color ) :
        cv2.circle( img, p, 2, color, -1)

    # Draw delaunay triangles
    def draw_delaunay(img, subdiv, delaunay_color, dictionary ) :
        triangleList = subdiv.getTriangleList();
        triangle_list = []
        size = img.shape
        r = (0, 0, size[1], size[0])

        for t in triangleList :

            pt1 = (int(t[0]), int(t[1]))
            pt2 = (int(t[2]), int(t[3]))
            pt3 = (int(t[4]), int(t[5]))

            if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
                cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
                triangle_list.append((dictionary[pt1],dictionary[pt2],dictionary[pt3]))

        dictionary = {}
        return triangle_list


    def delaunay_window(img, all_coord, subdiv, dictionary) :
        win_delaunay = "Delaunay Triangulation"
        # Turn on animation while drawing triangles
        animate = True

        # Define colors for drawing.
        delaunay_color = (255,255,255)
        points_color = (0, 0, 255)

        img_orig = cv2.imread(img_name)

        # Rectangle to be used with Subdiv2D
        size = img.shape
        rect = (0, 0, size[1], size[0])


        # Create an instance of Subdiv2D
        subdiv = cv2.Subdiv2D(rect)

        # Read in the points
        size=(img.shape[1],img.shape[0])
        all_coord.append((1,1)) # top left corner ?
        all_coord.append((size[0]-1,1)) # top right corner
        all_coord.append(((size[0]-1)//2,1)) #
        all_coord.append((1,size[1]-1))
        all_coord.append((1,(size[1]-1)//2))
        all_coord.append(((size[0]-1)//2,size[1]-1))
        all_coord.append((size[0]-1,size[1]-1)) # bottom right corner
        all_coord.append(((size[0]-1),(size[1]-1)//2)) # middle

        # Make a points list and a searchable dictionary.
        points=[(int(x[0]),int(x[1])) for x in all_coord]
        dictionary={x[0]:x[1] for x in list(zip(points,range(76)))}

        new_all_coord = []
        for points in all_coord:
            new_point = (points[0], points[1])
            new_all_coord.append(new_point)
        all_coord = new_all_coord

        # Insert points into subdiv
        for p in new_all_coord:
            subdiv.insert(p)
            # Show animation
            if animate :
                img_copy = cv2.imread(img_name)
                    # Draw delaunay triangles
                draw_delaunay( img_copy, subdiv, (255, 255, 255), dictionary )
                # cv2.imshow(win_delaunay, img_copy)

        # Draw delaunay triangles
        triangle_list = draw_delaunay( img_copy, subdiv, (255, 255, 255), dictionary )
        # cv2.imshow(win_delaunay, img_copy)

        return triangle_list

    subdiv = []
    subdiv2 = []
    dictionary = {}
    dictionary2 = {}

    #coordinates of the given image
    triangle_list = delaunay_window(user_img, all_coord, subdiv, dictionary)
    #coordinates of the matching one
    triangle_list2 = delaunay_window(char_img, all_coord2, subdiv2, dictionary2)


    def applyAffineTransform(src, srcTri, dstTri, size) :

        # Given a pair of triangles, find the affine transform.
        warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )

        # Apply the Affine Transform just found to the src image
        dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

        return dst


    # Warps and alpha blends triangular regions from img1 and img2 to img
    def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

        # Find bounding rectangle for each triangle
        r1 = cv2.boundingRect(np.float32([t1]))
        r2 = cv2.boundingRect(np.float32([t2]))
        r = cv2.boundingRect(np.float32([t]))


        # Offset points by left top corner of the respective rectangles
        t1Rect = []
        t2Rect = []
        tRect = []


        for i in range(0, 3):
            tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
            t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
            t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


        # Get mask by filling triangle
        mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
        cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

        # Apply warpImage to small rectangular patches
        img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

        size = (r[2], r[3])
        warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
        warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

        # Alpha blend rectangular patches
        imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

        # Copy triangular region of the rectangular patch to the output image
        img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

    alpha = 0.5

        # Convert Mat to float data type
    img1 = np.float32(img_copy)
    img2 = np.float32(new_char_img)

        # Read array of corresponding points
    points1 = all_coord
    points2 = all_coord2
    points = []

        # Compute weighted average point coordinates
    for i in range(0, len(points1)):
        x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
        y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
        points.append((x,y))

        # Allocate space for final output
    imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

    # index of the triangles
    # get a list of the triangles in an image
    # for each triangle - go through it
    for i in range(len(triangle_list)):
        x = triangle_list[i][0]
        y = triangle_list[i][1]
        z = triangle_list[i][2]

        x = int(x)
        y = int(y)
        z = int(z)

        t1 = [points1[x], points1[y], points1[z]]
        t2 = [points2[x], points2[y], points2[z]]
        t = [ points[x], points[y], points[z] ]

                # Morph one triangle at a time.
        morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)

        # Display Result
    #cv2.imshow("Morphed Face", np.uint8(imgMorph))
    cv2.imwrite('output/morph.jpg', imgMorph)




    cv2.waitKey()
