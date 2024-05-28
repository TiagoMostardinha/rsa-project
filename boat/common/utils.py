import csv

def csvToMap(file):
    map = []
    freeSpace = 0
    with open(file, "r") as mapReader:
        csv_reader = csv.reader(mapReader, delimiter=",")

        for row in csv_reader:
            line = []
            for square in row:
                if square == "o" or square == "x":
                    if square == "o":
                        freeSpace += 1
                    line.append(square)
                else:
                    raise Exception("Invalid map format!")
            map.append(line)
    
    return map,freeSpace
