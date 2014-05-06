import random

class Sperner:

  # calculates spener for a given n agents/resources, k (meaning k+2) price intervals between 0 and totalBalance for each resource
  def sperner(self, n, k, preferences, totalBalance):
    # determine the payments for k (k+2 values) subdivisions of totalBalance
    payments = list(xrange(0, totalBalance + 1, totalBalance / (k + 1)))
    paymentsLength = len(payments)

    self.agentPreferences = preferences

    # determine allocations by creating the graph for our given values
    allocations = self.createGraph(n, k+2, n, [], payments)

    # determine the sinks or the inner triangle with satisfying assignment vertices as a perimeter
    # by walking the graph contained in allocations
    solutionSinks = self.solve(n, k + 2, allocations)

    # if we have found no solution we return (this should only happen if an invariant is naively broken)
    if solutionSinks == None:
      return
    # average the satisfying assignments that are the solutionSinks to find the final solution
    finalSolution = self.averageFair(n, solutionSinks, payments)
    return finalSolution



# create a n^k size representation of the sperner simplexes graph
  def createGraph(self, n, k, iterator, indices, payments):
    allocations = [[[0 for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(k)]

    # assign corners, each of the unique resources to an agent
    allocations[k - 1][0][0] = self.assignAgentToRoom([2], [k-1, 0, 0], n)
    allocations[0][k - 1][0] = self.assignAgentToRoom([3], [0, k-1, 0], n)
    allocations[0][0][k - 1] = self.assignAgentToRoom([1], [0, 0, k-1], n)

    # assign each outer vertex from resource to an agent, such that these resources match the corners containing them
    for i in xrange(k):
      for j in xrange(k):
        allocations[i][j][0] = self.assignAgentToRoom([3], [i, j, 0], n)

    for j in xrange(k):
      for l in xrange(k):
        allocations[0][j][l] = self.assignAgentToRoom([1], [0, j, l], n)

    for i in xrange(k):
      for l in xrange(k):
        allocations[i][0][l] = self.assignAgentToRoom([2], [i, 0, l], n)

    # randomly "color" rest of graph, assigning any given room to an agent by top preference
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          # ignore nodes which are illogical in our "squareification" of the graph
          if payments[i] + payments[j] + payments[l] != payments[len(payments) - 1]:
            allocations[i][j][l] = None
          # if this node is not a corner or outer edge, we then assign a random "color" to it
          elif allocations[i][j][l] == 0: 
            allocations[i][j][l] = self.assignAgentToRoom([1,2,3], [i, j, l], n)

    return allocations


  # given a set of possible resources and costs for each resource, find an agent who prefers a room
  def assignAgentToRoom(self, room, costs, n):
    agentPreferences = [self.agentPreferences[x][costs[0]][costs[1]][costs[2]] for x in xrange(n)]
    for preference in agentPreferences:
      if preference in room:
        return agentPreferences.index(preference) + 1

    # due to the invariance of the algorithm, we need an error value for a naive preference set which breaks the outer-coloring invariants
    return 40

  # arbitrarily (randomly) generates test preference values, returning a strict preference ordering for each agent at each cost assignment of resources
  def generatePreferences(self, n, k):
    preferences = [[[[0 for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(k)] for _ in xrange(n)]
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          for x in xrange(n):
            preferences[x][i][j][l] = random.randrange(1, n + 1)

    return preferences

  # given a created Sperner's graph and allocation assignment, search the graph to find satisfying one-to-one assignments
  # and find the inner triangle which is surrounded by these one-to-one assignments
  # take the average of these values to get the approximation ideal solution for a given k
  def solve(self, n, k, allocations):
    remaining, sinks, allocation = [], [], []
    for i in xrange(k):
      for j in xrange(k):
        for l in xrange(k):
          if allocations[i][j][l] == None:
            continue
          if allocations[i][j][l] == 40:
            return None
          remaining = list(xrange(1, n + 1))
          sinks = []
          
          remaining.remove(allocations[i][j][l])
          sinks.append([i,j,l])
          neighbors = self.getNeighbors(i, j, l, k, allocations)
          
          for neighbor in neighbors:
            if neighbor[0] in remaining:
              remaining.remove(neighbor[0])
              sinks.append(neighbor[1])

    if len(remaining) == 0:
      return sinks
    else:
      print "no solution found for 3-person Sperner's"
      return None



  # given a set of satisfying one-to-one assignment vertices, average their values to get the 
  # approximate ideal solution for a given k
  def averageFair(self, n, sinks, payments):
    returnArray = []
    for bidder in xrange(n):
      values = sinks[:][bidder]
      returnValue = sum([payments[x] for x in values]) / len(values)
      print returnValue
      returnArray.append(returnValue)
    return returnArray


  # simple constant-space, linear-time function to determine if there are any duplicate assignments
  # if there are not, we have a non-conflicting one-to-one assignment
  def check_satisfying(self, choices):
    for choice in choices:
      choiceIndex = choice - 1
      if choices[choiceIndex] < 0:
        return False
      else:
        choices[choiceIndex] = -1 * choice
    return True


  # find all neighbors of a vertex, such that we can determine which are also in the perimeter 
  # of the satisfying inner triangle.
  # We naively consider all possibilities and filter out those which are illogical
  def getNeighbors(self, i, j, l, k, allocations):
    neighbors = [[i+ 1, j-1, l], [i-1, j+1, l], [i, j-1, l+1], [i, j+1, l-1],  [i-1, j, l+1], [i+1, j, l-1]] 
    for neighbor in neighbors:
      for index in neighbor:
        if index < 0 or index > k:
          neighbors.remove(neighbor)
          continue
    return [[allocations[x][y][z], [x,y,z]] for [x,y,z] in neighbors]

#### sample functionality ####
newSperner = Sperner()
preferences = newSperner.generatePreferences(3, 3)

print newSperner.sperner(3, 1, preferences, 1000)






  
