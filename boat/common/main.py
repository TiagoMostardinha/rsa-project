import utils
import dijkstra


def main(map_file):
    map, freeSpace = utils.csvToMap(map_file)
    graph = dijkstra.mapToGraph(map)
    src = (0, 0)
    target = (12,16)
    shortest = dijkstra.shortestPath(n=freeSpace, edges=graph, src=src,target=target)
    print(shortest)


if __name__ == "__main__":
    map_file = "map.csv"
    main(map_file)
