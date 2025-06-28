import ast
import pickle
import pt_engine.globals as globals

class Edge:
  def __init__(self, source, target, data):
    # src and tgt are strings, label is AST node ref
    self.src = source
    self.tgt = target
    self.label = data

class Graph:
  def __init__(self):
    # rep invariants: 
    #    nodes has no duplicates
    #    edges.keys() is_subset nodes
    
    # nodes is a list of String function names
    self.nodes = []
    # adjacency list reprsentation from names to [Edge]
    # for each edge in edges[name] edge.src = name  
    self.edges = {}
    # reverse edges. for each edge in edges with edge.src and edge.tgt 
    # there is a rev_edge in rev_edges with rev_edge.src = edge.tgt and rev_edge.tgt = edge.src
    self.rev_edges = {}

  def hasNode(self,node):
    return node in self.nodes

  def addNode(self,node):
    if not self.hasNode(node):
     self.nodes.append(node)

  def hasEdge(self,source,target,data):
    if not (source in self.edges):
      return False
    edges_from_source = self.edges[source]
    for edge in edges_from_source:
      if edge.src == source and edge.tgt == target and edge.label == data:
        return True
    return False
  
  def hasRevEdge(self,source,target,data):
    if not (source in self.rev_edges):
      return False
    rev_edges_from_source = self.rev_edges[source]
    for rev_edge in rev_edges_from_source:
      if rev_edge.src == source and rev_edge.tgt == target and rev_edge.label == data:
        return True
    return False  

  def addEdge(self,source,target,data):
    result = False
    self.addNode(source)
    self.addNode(target)
    if not self.hasEdge(source,target,data):
      edge = Edge(source,target,data)
      rev_edge = Edge(target,source,data)
      if edge.src not in self.edges:
        self.edges[edge.src] = [edge]
      else:
        self.edges[edge.src].append(edge)
      if rev_edge.src not in self.rev_edges:
        self.rev_edges[rev_edge.src] = [rev_edge]
      else:
        self.rev_edges[rev_edge.src].append(rev_edge)    
      result = True
    return result

  def getEdgesFromSource(self,source):
    if not (source in self.edges):
      return []
    else: 
      return self.edges[source]

  def getRevEdgesFromSrouce(self,source):
    if not (source in self.rev_edges):
      return []
    else:
      return self.rev_edges[source]

  def getEdgesToTarget(self,target):
    result = []
    for source in self.edges.keys():
      for edge in self.edges[source]:
         if (edge.tgt == target):
           result.append(edge)
    return result

  def printGraph(self, extra_info = None):
    print("\n Printing the graph: ")    
    #print(extra_info)
    for key in self.edges.keys():
      for edge in self.edges[key]:
        # assert isinstance(edge.src, ast.FunctionDef) and isinstance(edge.tgt, ast.FunctionDef)
        assert isinstance(edge.src, ast.FunctionDef) or isinstance(edge.src, ast.AsyncFunctionDef)
        assert isinstance(edge.tgt, ast.FunctionDef) or isinstance(edge.tgt, ast.AsyncFunctionDef)
        #print("Call from ",edge.src," to ",edge.tgt)
        extra_src = " (in "+extra_info[edge.src].name+")" if extra_info != None and edge.src in extra_info else ""
        extra_tgt = " (in "+extra_info[edge.tgt].name+")" if extra_info != None and edge.tgt in extra_info else ""
        print("Call from ",edge.src.name+extra_src," to ",edge.tgt.name+extra_tgt) 
    print("")

  def cg_to_pkl(self, extra_info = None):
    print("\n Printing the graph: ")    
    #print(extra_info)
    ep = globals.encl_path
    def rpl(x):
      if False:
        pp = ["/.../pt_analysis/orig_pro_dynamic/cerberus/",
              "/.../pt_analysis/orig_pro_dynamic/pygal/",
              "/.../pt_analysis/orig_pro_dynamic/mtgjson/",
              "/.../pt_analysis/orig_pro_dynamic/sc2/",
              "/.../pt_analysis/orig_pro_dynamic/zfsp/",
              "/.../pt_analysis/orig_pro_dynamic/invoke/"]
        for p in pp:
          x = x.replace(p,"")
      x = x.replace(globals.curr_package_dir, "")
      return x
    dd = {}
    if 0:
      if extra_info is not None:
        for a in extra_info:
          b = extra_info[a]
          print("Class =", b.name)
          print("Func =", a.name)
          if a in ep:
            print("   ", rpl(ep[a]))
    for key in self.edges.keys():
      for edge in self.edges[key]:
        # assert isinstance(edge.src, ast.FunctionDef) and isinstance(edge.tgt, ast.FunctionDef)
        assert isinstance(edge.src, ast.FunctionDef) or isinstance(edge.src, ast.AsyncFunctionDef)
        assert isinstance(edge.tgt, ast.FunctionDef) or isinstance(edge.tgt, ast.AsyncFunctionDef)
        #print("Call from ",edge.src," to ",edge.tgt)
        extra_src = " (in "+extra_info[edge.src].name+")" if extra_info != None and edge.src in extra_info else ""
        extra_tgt = " (in "+extra_info[edge.tgt].name+")" if extra_info != None and edge.tgt in extra_info else ""
        print("Call from ",edge.src.name+extra_src," to ",edge.tgt.name+extra_tgt) 
        #print("   ",type(edge.src), edge.src in extra_info)
        #if edge.src in extra_info: print("  = ", extra_info[edge.src], extra_info[edge.src].name) 
        xx = ""
        yy = ""
        if edge.src in ep: 
          #print("   + ", rpl(ep[edge.src]))
          xx = rpl(ep[edge.src])
        else:
          print(ast.dump(edge.src)) 
          print("AAAAAAAAAAAAAAAAA")
          assert False
        if edge.tgt in ep: 
          #print("   + ", rpl(ep[edge.src]))
          yy = rpl(ep[edge.tgt])
        else:
          print(ast.dump(edge.tgt)) 
          print("BBBBBBBBBBBBBBBBBB")
          assert False
        print("    >> ",xx," to ",yy) 
        #print("   ",ep[edge.src], " to ", ep[edge.tgt]) 
        #print(ast.dump(edge.tgt))
        #print(ast.unparse(edge.tgt))
        #print("\n",ast.dump(edge.src),"\n", ast.unparse(edge.src),"\n")
        #print(edge.label)
        if xx not in dd:
          dd[xx] = [yy]
        else:
          ll = dd[xx]
          ll.append(yy)
          dd[xx] = ll
        #path = "/.../pt_analysis/inferred_types/call_graph/invoke/"
        path = "/.../pt_analysis/inferred_types/call_graph/" + globals.package_name + "/"
        p_name = globals.write_pkl_name
        #print(path)
        #print(p_name)
        #assert False
        if 0:
          with open(path + p_name, 'wb') as f:
            pickle.dump(dd, f, protocol=pickle.HIGHEST_PROTOCOL)
        globals.dd_global = dd
    #print("")
  
  def getAllEdges(self):
    ret = []
    for key in self.edges.keys():
      for edge in self.edges[key]:
        ret.append(edge)
    return ret

  

  #TODO: TEST!!!
  def isDAG(self):
    for key in self.edges.keys():
       worklist = []
       closure = []
       for edge in self.edges[key]:
          if not (edge.tgt in closure):
            closure.append(edge.tgt)
            worklist.append(edge.tgt)
       while not (worklist == []):
          node = worklist.pop()
          if node in self.edges.keys():
            for edge in self.edges[key]:
              if not (edge.tgt in closure):
                closure.append(edge.tgt)
                worklist.append(edge.tgt)
       if key in closure:
         print("Call graph is NOT a DAG: ",key)
         return False 
    return True 
