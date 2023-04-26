import numpy as np
import cv2
import random
import math
import music21

def extract_notes_from_image(image_path):
    # Load the image
    print("Loading image: " + image_path)
    img = cv2.imread(image_path)

    #resize image 4 times smaller
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("Blurring image...")
    # Apply a Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)


    minRadius = 15
    maxRadius = 30
    print("Detecting circles...")
    # Apply the HoughCircles transform to detect circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1=25, param2=15, minRadius=minRadius, maxRadius=maxRadius)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 100
    max_area = 2000
    # Create an empty list to store the coordinates of squares
    squares = []

    # Iterate through each contour
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        # Check if the polygon has four vertices
        if len(approx) == 4:
            # Calculate the area of the polygon
            area = cv2.contourArea(approx)
            # Check if the area of the polygon is greater than the threshold
            if area > min_area and area < max_area:
                squares.append(approx)

    # Draw squares around the squares
    cv2.drawContours(img, squares, -1, (0, 255, 0), 3)

    # withdraw all square wich center coordinates are in a circle
    if circles is not None:
        tmpCircles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in tmpCircles:
            for i, square in enumerate(squares):
                if cv2.pointPolygonTest(square, np.float32((x, y)), False) >= 0:
                    # remove the square from the squares array
                    print("removing square")
                    squares = np.delete(squares, i, axis=0)
                    break

    # Draw squares around the squares
    cv2.drawContours(img, squares, -1, (0, 255, 0), 3)

    # Extract the coordinates of each circle found
    coords = []
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            print("x: " + str(x) + " y: " + str(y) + " r: " + str(r))
            coords.append((x, y, r))
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)


    cv2.imshow("Notes with centers", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coords, img

def sortMegaGroup(megaGroup):
    tmpGroups = []
    #split megaGroup into smaller groups of 32
    for i in range(len(megaGroup) // 32):
        tmpGroups.append(megaGroup[i * 32: (i + 1) * 32])
        print("tmpGroup length : " + str(len(tmpGroups[i])))

    #sort each group by horizontal position
    for group in tmpGroups:
        group.sort(key=lambda tup: tup[0])

    #res matrix is a list of 128 elements
    resGroup = [(0,0,0)] * 128

    print("total groups: " + str(len(tmpGroups)))
    for x in range(len(tmpGroups)):
        for y in range(len(tmpGroups[x])):
            element = tmpGroups[x][y]
            if (element is (0,0,0)):
                print("x: " + str(x) + " y: " + str(y) + " is None")
            resGroup[x + y * 4] = element

    return resGroup

def get_circle_groups(imgPath):
    circlesCoords, img = extract_notes_from_image(imgPath)
    #remove all (0,0,0) elements
    circlesCoords = [x for x in circlesCoords if x != (0,0,0)]

    tmp = circlesCoords.copy()
    tmp.sort(key=lambda tup: tup[0])
    print("tmp: " + str(tmp))
    legend = tmp[:7]
    legend.sort(key=lambda tup: tup[1])
    print("Legend: " + str(legend))
    for circle in legend:
        circlesCoords.remove(circle)

    #sort circles by vertical position
    circlesCoords.sort(key=lambda tup: tup[1])
    megaGroups = []
    currentGroup = []
    for i in range(len(circlesCoords)):
        if i != 0 and  i % 128 == 0:
            megaGroups.append(currentGroup)
            currentGroup = [circlesCoords[i]]
        else:
            currentGroup.append(circlesCoords[i])

    megaGroups.append(currentGroup)

    groups = []
    for megaGroup in megaGroups:
        sortedMegaGroup = sortMegaGroup(megaGroup)
        group1 = sortedMegaGroup[:64]
        group2 = sortedMegaGroup[64:]
        groups.append(group1)
        groups.append(group2)

    print("Groups: " + str(groups))
    res = []

    # Draw circles with random colors around the circles in each group and a number in the center
    number = 0
    for group in groups:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for (x, y, r) in group:
            #cv2.circle(img, (x, y), r, color, 2)
            #cv2.putText(img, str(number), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            number += 1
            res.append((x, y, r))

    cv2.imshow("Notes with centers", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the image
    #cv2.imwrite("cercles_notes_colors.jpeg", img)

    return res, legend, img
def get_circle_groups_without_legend(imgPath):
    circlesCoords, img = extract_notes_from_image(imgPath)

    # sort circles by vertical position
    circlesCoords.sort(key=lambda tup: tup[1])
    megaGroups = []
    currentGroup = []
    for i in range(len(circlesCoords)):
        if i != 0 and i % 128 == 0:
            megaGroups.append(currentGroup)
            currentGroup = [circlesCoords[i]]
        else:
            currentGroup.append(circlesCoords[i])

    megaGroups.append(currentGroup)

    groups = []
    for megaGroup in megaGroups:
        sortedMegaGroup = sortMegaGroup(megaGroup)
        group1 = sortedMegaGroup[:64]
        group2 = sortedMegaGroup[64:]
        groups.append(group1)
        groups.append(group2)

    print("Groups: " + str(groups))
    res = []

    # Draw circles with random colors around the circles in each group and a number in the center
    number = 0
    for group in groups:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for (x, y, r) in group:
            # cv2.circle(img, (x, y), r, color, 2)
            # cv2.putText(img, str(number), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            number += 1
            res.append((x, y, r))

    cv2.imshow("Notes with centers", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the image
    # cv2.imwrite("cercles_notes_colors.jpeg", img)

    return res, img

def get_circle_mean_color(circle, img):
    # Get the mean color of a circle
    x, y, r = circle
    circle_img = img[y - r:y + r, x - r:x + r]
    mean_color = np.mean(circle_img, axis=(0, 1))

    # Draw a circle with the mean color on the img
    #img = cv2.circle(img, (x, y), r, mean_color, -1)

    return mean_color,img

def get_colors_from_group(groups : dict, img):
    # Get the colors of the circles in each group
    colors = []
    separate = 0
    for i in range(len(groups)):
        circle = groups[i]
        color, img = get_circle_mean_color(circle, img)
        colors.append(color)

    cv2.imshow("Mean colors", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #save img
    cv2.imwrite("cercles_mean_colors.jpeg", img)

    return colors


def color_distance(color1, color2):
    # Compute the distance between two colors
    return np.linalg.norm(color1 - color2)

def find_nearest_color(color, colorList=None):
    # eg. rgb_tuple = (2,44,300)

    # add as many colors as appropriate here, but for
    # the stated use case you just want to see if your
    # pixel is 'more red' or 'more green'
    colors = {"red": (255, 0, 0),
              "green": (0, 255, 0),
              }

    distances = []
    for (r,g,b,color_name) in colorList:
        distances.append(color_distance(color, (r,g,b)))

    color = colorList[distances.index(min(distances))][3]
    return color


def simplify_colors(groupsColors, colorNoteList):
    # Simplify the colors of the circles in each group
    res = []
    for color in groupsColors:
        nearestColor = find_nearest_color(color, colorNoteList)
        res.append((nearestColor,False))

    return res

def merge_none_notes(noteTrack):
    newNoteTrack = []
    totalDuration = 0
    for i in range(len(noteTrack)):
        if noteTrack[i][0] != 'None':
            if totalDuration > 0:
                newNoteTrack.append(('None', totalDuration))
                newNoteTrack.append(noteTrack[i])
                totalDuration = 0
            else:
                newNoteTrack.append(noteTrack[i])
        else:
            totalDuration += noteTrack[i][1]

    if totalDuration > 0:
        newNoteTrack.append(('None', totalDuration))

    return newNoteTrack



def convert_note_track_to_note_and_duration(noteTrack):
# Convert the note track to a list of nodes and durations
    res = []
    duration = 0
    lastNote = noteTrack[0][0]
    for i in range(0, len(noteTrack)):
        if noteTrack[i][1]:
            if (duration == 7):
                duration += 1
            res.append((lastNote, duration))
            lastNote = noteTrack[i][0]
            duration = 1
        else:
            if noteTrack[i][0] == lastNote:
                duration += 1
            else:
                if (duration == 7):
                    duration += 1
                res.append((lastNote, duration))
                duration = 0
                lastNote = noteTrack[i][0]

    res.append((lastNote, duration))

    res = merge_none_notes(res)

    return res


def get_separators(simplifiedColors, biais, circles, img, colorsList):
    le = len(simplifiedColors)
    for i, color in enumerate(simplifiedColors[biais::4]):
        i_circles = biais + i * 4
        if (i_circles - 4 > 0 and i_circles < le):
            circle = circles[i_circles]
            lastCircle = circles[i_circles - 4]
            # get mean color of the horizontal segment between the two circles
            x, y, r = circle
            x2, y2, r2 = lastCircle
            # get the mean color of the horizontal segment between the two circles, knowing that y is the vertical alignment
            middleX = int((x + x2) / 2)

            mean_color = img[y, middleX]

            if (biais == 1):
                print("mean_color: ", mean_color)
            nearestColor = find_nearest_color(mean_color, colorsList)
            if (nearestColor == "None"):
                circleColor, _ = get_circle_mean_color(circle, img)
                print("lastCircleColor: ", circleColor)
                nearestColor = find_nearest_color(circleColor, colorsList)
                simplifiedColors[i_circles] = (nearestColor, True)


def create_musicxml(tracks, file_name):
    # create a Score object to hold the music
    score = music21.stream.Score()

    # create a Part object for each track
    parts = []
    for i in range(len(tracks)):
        part = music21.stream.Part(id='part{}'.format(i + 1))
        parts.append(part)
        score.insert(i, part)

    # iterate through each track and add its notes to the corresponding Part object
    for i in range(len(tracks)):
        for noteName, duration in tracks[i]:
            if noteName == 'None':
                # add a rest to the Part
                parts[i].append(music21.note.Rest(quarterLength=duration/4))
            else:
                # add a Note to the Part
                n = music21.note.Note(noteName, quarterLength=duration/4)
                parts[i].append(n)

    # write the music to a musicXML file
    score.write('musicxml', fp=file_name)


def process_image(file_name, save_path):
    circles1, legend, img1 = get_circle_groups(file_name)
    #circles2, img2 = get_circle_groups_without_legend("test_2.png")

    print("legend: " + str(legend))
    print("=================================")
    colorsList = []
    red, _ = get_circle_mean_color(legend[0], img1)
    print("red: ", red)
    brown, _ = get_circle_mean_color(legend[1], img1)
    print("brown: ", brown)
    yellow, _ = get_circle_mean_color(legend[2], img1)
    print("yellow: ", yellow)
    green, _ = get_circle_mean_color(legend[3], img1)
    print("green: ", green)
    ligh_blue, _ = get_circle_mean_color(legend[4], img1)
    print("light blue: ", ligh_blue)
    pink, _ = get_circle_mean_color(legend[5], img1)
    print("pink: ", pink)
    purple, _ = get_circle_mean_color(legend[6], img1)
    print("purple: ", purple)

    colorsList.append((255, 255, 255, "None"))
    colorsList.append((*red, "C"))
    colorsList.append((*brown, "D"))
    colorsList.append((*yellow, "E"))
    colorsList.append((*green, "F"))
    colorsList.append((*ligh_blue, "G"))
    colorsList.append((*pink, "A"))
    colorsList.append((*purple, "B"))

    colorGroups1 = get_colors_from_group(circles1, img1)
    #colorGroups2 = get_colors_from_group(circles2, img2)

    simplifiedColors1 = simplify_colors(colorGroups1, colorsList)
    #simplifiedColors2 = simplify_colors(colorGroups2, colorsList)

    get_separators(simplifiedColors1, 0, circles1, img1, colorsList)
    get_separators(simplifiedColors1, 1, circles1, img1, colorsList)
    get_separators(simplifiedColors1, 2, circles1, img1, colorsList)
    get_separators(simplifiedColors1, 3, circles1, img1, colorsList)
    #get_separators(simplifiedColors2, 0, circles2, img2)
    #get_separators(simplifiedColors2, 1, circles2, img2)
    #get_separators(simplifiedColors2, 2, circles2, img2)
    #get_separators(simplifiedColors2, 3, circles2, img2)

    print(colorsList)
    # print("simplifiedColors1.1: ", simplifiedColors1[::4])
    # print("simplifiedColors1.2: ", simplifiedColors2[::4])

    track1 = simplifiedColors1[::4]
    track1 = convert_note_track_to_note_and_duration(track1)

    track2 = simplifiedColors1[1::4] # + simplifiedColors2[1::4] + simplifiedColors3[1::4]
    track2 = convert_note_track_to_note_and_duration(track2)

    track3 = simplifiedColors1[2::4] # + simplifiedColors2[2::4] + simplifiedColors3[2::4]
    track3 = convert_note_track_to_note_and_duration(track3)

    track4 = simplifiedColors1[3::4] # + simplifiedColors2[3::4] + simplifiedColors3[3::4]
    track4 = convert_note_track_to_note_and_duration(track4)

    print("track1: ", track1)
    print("track2: ", track2)
    print("track3: ", track3)
    print("track4: ", track4)

    create_musicxml(tracks=[track1, track2, track3, track4], file_name=save_path)




'''
i = 0
le = len(simplifiedColors)
while i < le:
    print(simplifiedColors[i:i+4])
    print("========================================================================")
    i += 4
'''

#print(simplifiedColors)
#extract_rectangles_from_image("rectangles_rythmes.jpeg")
