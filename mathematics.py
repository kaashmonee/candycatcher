
# returns a list whose points are scaled by some factor
def scale(listToScale, factor):
    scaledList = []
    for num in listToScale:
        scaledList.append(num * factor)

    return scaledList


def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5