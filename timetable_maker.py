'''
Function: Adjacency List that stores the neighbouring nodes, in a directed grapgh

Time Complexity: O(N) time to make the list, N being the number of nodes

'''
class AdjacencyList:
    def __init__(self, size):
        self.size = size
        self.adj_list = [[] for x in range(size)]

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def get_neighbors(self, u):
        return self.adj_list[u]



'''
Function: This creates takes in the given inputs , and creates an adjacency matrix and list, Using that List and Matrix it runs Ford Fulkerson using DFS to find the maximum flow, then returns it


Flow Network Approach: Firstly The flow network structure chosen is, two nodes repersenting the min and max connect to officers with a capacity of mim number of shifts and max minus min shift
respectively, Officers connect to nodes in the officer/day category, so for each officer there is a corresponding node of that officer number and a day (Officer 1 Day 1, Officer 1 Day 2 ... etc)
the edges between Offficer and Officer day have a capacity of 1 as they can only work once a day.
Officer Day connect to Shift Day, same principle, for each day there will be a every single shift from each company, the edge capacity is also one and this is where the prefences are set
Shift days connect back to companies, which are merged down to repersent every day, similar to officers, the edge capacity being the number of shifts needed a day multiplied by days.
Then the companies connect to a sink node.

Code Approach:
Initalise the Matrix with it's capacities, and also initalise the adjacency list with the neighbours.
Run Ford Fulkerson once on the matrix with the adjaceny list, setting the source of the min node(index 0),
Ford Fulkerson uses DFS and also repersents the flow by changing the inverse edge to hold the flow, if u -> v with capacity 10 and ford wants a flow of 5 then v -> u with edge weight 5
so the Matrix stores the capacities and flow, and it should saturated the min to officer edges if it is a valid allocation.
Run Ford a second time setting the max as source, and this should return the matrix with a completely saturated edges from the companies to the sink, 

Time Complexity: 
N is the number of Officers and M is the number of companies 
Making the Matrix is O(N^2 + M^2), the size of the array is M + N hence to make the matrix it is (M+N)^2 therefore O(M^2 + N^2)  
Making the Adjacency list is O(M + N). 
Running Ford Folkerson Using DFS takes O(N*N*M), As the time to run Ford Fulkerson is O(E * maxFlow), edges * max flow.
The maximum flow can be found using the number of officers multipled by the maximum number of shifts, hence it equates to N.
And the number of edges within the adjacency_list is equal to N*M, as each officer connects to each companies shifts.
Thus the Ford Fulkerson time complexity is O(N*(N*M)) = O(N * N * M )
The time to form the allocation sheet is O(N*M) as the rest are constants.

OVERALL TIME COMPLEXITY: O(N * N * M) is the dominating term and is the time it takes to run Ford Fulkerson,
ford is run twice but the dominating term is still O(N* N *M)


Space Complexity: is O(M^2 + N*2) the matrix dominates space complexity compared to the adjacency list.


'''

class FlowNetwork:


    def __init__(self,preferences, officeres_per_org, min_capcity: int, max_capcity: int ):
        self.number_of_days = 30

        self.min_capcity = min_capcity
        self.max_capcity = max_capcity
        

        self.comp_number = len(officeres_per_org)
        self.officer_number = len(preferences)
        self.array_size = 3 + self.comp_number + (self.comp_number*3*self.number_of_days) + self.officer_number + (self.officer_number*self.number_of_days)
        self.officer_start = 2
        self.officer_day_start = self.officer_number + self.officer_start
        self.shift_day_start = self.officer_day_start + self.officer_number*self.number_of_days 

        self.company_start = self.shift_day_start + self.comp_number*3*self.number_of_days
        
        self.total_shifts_per_day = 0

        for orgs in officeres_per_org:
            for shift in orgs:
                self.total_shifts_per_day += shift

        self.total_shifts_months = self.total_shifts_per_day*self.number_of_days

        self.min_number_of_shifts = self.min_capcity * self.officer_number

        self.adjacencyList = AdjacencyList(self.array_size)

        self.matrix = [[0 for x in range(self.array_size)] for x in range(self.array_size)]


        self.connect_officerD_shiftD(self.adjacencyList,self.matrix,preferences)
        self.connect_Officer_OfficerD(self.adjacencyList,self.matrix)
        self.connect_shifts_companies(self.adjacencyList,self.matrix,officeres_per_org)
        self.connect_companies_sink(self.adjacencyList,self.matrix,officeres_per_org)
        self.connecnt_source_officers(self.adjacencyList,self.matrix,self.min_capcity)
        self.max_connect_source(self.adjacencyList,self.matrix,self.min_capcity,self.max_capcity)

        
    def result(self):
        return self.collect_data(self.adjacencyList,self.matrix)

    def dfs(self, source, sink, parent, adjacency_list:AdjacencyList, matrix, visited):
        stack = [source]
        visited[source] = True

        while stack:
            u = stack.pop()

            for v in adjacency_list.get_neighbors(u):
                if not visited[v] and matrix[u][v] > 0:
                    stack.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True

        return False

    def ford_fulkerson(self, adjacency_list:AdjacencyList, source, sink, matrix):
        parent = [-1] * adjacency_list.size
        max_flow = 0

        while True:
            visited = [False] * adjacency_list.size
            if not self.dfs(source, sink, parent, adjacency_list, matrix, visited):
                break

            path_flow = float('Inf')
            s = sink

            while s != source:
                path_flow = min(path_flow, matrix[parent[s]][s])
                s = parent[s]

            v = sink
            while v != source:
                u = parent[v]
                matrix[u][v] -= path_flow
                matrix[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow



    def connecnt_source_officers(self,adjacency_list: AdjacencyList,matrix,capcity):
        for officer in range(self.officer_number):
            matrix[0][self.officer_start + officer] = capcity 
            adjacency_list.add_edge(0,self.officer_start + officer)
            
    

    def max_connect_source(self,adjacency_list:AdjacencyList,matrix,min_shift,max_shift):
        for officer in range(self.officer_number):
            matrix[1][self.officer_start + officer] = max_shift - min_shift
            adjacency_list.add_edge(1,self.officer_start + officer)



    def connect_officerD_shiftD(self,adjacency_list:AdjacencyList,matrix,prefences):
        for day in range(self.number_of_days):

            offcier_number = 0
            for officer in prefences:
                for company in range(self.comp_number):
                    shift_number = 0
                    for shift in officer:
                        if shift == 1:
                            matrix[self.officer_day_start + (day*self.officer_number) + offcier_number ][self.shift_day_start + (day*self.comp_number*3) + (3*company) + shift_number] = 1
                            adjacency_list.add_edge(self.officer_day_start + (day*self.officer_number) + offcier_number ,self.shift_day_start + (day*self.comp_number*3) + (3*company) + shift_number)

                        shift_number += 1
                offcier_number += 1

                        
    def connect_Officer_OfficerD(self,adjacency_list:AdjacencyList,matrix):
        for officer in range(self.officer_number):

            for day in range(self.number_of_days):
                
                matrix[self.officer_start + officer][self.officer_day_start + (day*self.officer_number) + officer] = 1
                adjacency_list.add_edge(self.officer_start + officer,self.officer_day_start + (day*self.officer_number) + officer)
    


    def connect_shifts_companies(self,adjacency_list : AdjacencyList,matrix,officeres_per_org):
        company_number = 0
        for company in officeres_per_org:
            
            for day in range(self.number_of_days):
                shift_number = 0
                for shift in company:

                    matrix[self.shift_day_start + (day*self.comp_number*3) + (company_number*3) + shift_number][self.company_start + company_number] = shift

                    adjacency_list.add_edge(self.shift_day_start + (day*self.comp_number*3) + (company_number*3) + shift_number,self.company_start + company_number)

                    shift_number += 1

            company_number += 1
    

    def connect_companies_sink(self,adjacency_list: AdjacencyList,matrix,officeres_per_org):

        company_number = 0
        for company in officeres_per_org:
            total_shifts = 0
            for shift in company:
                total_shifts += shift
            
            total_shifts = total_shifts*self.number_of_days
            matrix[self.company_start + company_number][self.array_size-1] = total_shifts
            adjacency_list.add_edge(self.company_start + company_number,self.array_size-1)

            company_number += 1
    
    

    def collect_data(self,adjacency_list:AdjacencyList,matrix):
        
        result = self.ford_fulkerson(adjacency_list,0,self.array_size-1,matrix)

      
        for value in self.adjacencyList.get_neighbors(0):
            if matrix[value][0] < self.min_capcity:
                return None

        max_result = self.ford_fulkerson(self.adjacencyList,1,self.array_size-1,matrix)



        if result + max_result < self.total_shifts_months:
            return None

        ret_data = [[[[0 for x in range(3)] for x in range(self.number_of_days)] for x in range(self.comp_number)] for x in range(self.officer_number)]


        for officer in range(self.officer_number):

            for day in range(self.number_of_days):
                    
                for company in range(self.comp_number):
                    
                    for shift in range(3):
                        if matrix[self.officer_day_start + (day*self.officer_number) + officer][self.shift_day_start + (day*self.comp_number*3) + (3*company) + shift] == 1:
                            ret_data[officer][company][day][shift] = 1

        return ret_data



def allocate(pref,req,min,max):
    flow = FlowNetwork(pref,req,min,max)
    
    return flow.result()