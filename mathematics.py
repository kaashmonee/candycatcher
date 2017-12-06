
# returns a list whose points are scaled by some factor
def scale(listToScale, factor):
    scaledList = []
    for num in listToScale:
        scaledList.append(num * factor)

    return scaledList