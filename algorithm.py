from sympy import Point, Triangle, N, Edge

def bowyer_watson(points: list[tuple[int, int]]) -> list[Triangle]:
    # create big triangle
    # add points and perform algo
    # check point against circumcircles
    # If inside, for each edge or triangle create new triangle with added point
    # delete old triangles
    # repeat
    # remove big triangle
    # return and rejoice
    # TODO

def msp(triangles: list[Triangle]) -> list[Edge]:
    # triangles to weighted edges by distance
    # figure out algo to use for this
    # TODO

def astar(edge: Edge) -> list[Point]:
    # find and return path for a single edge per call
    # TODO