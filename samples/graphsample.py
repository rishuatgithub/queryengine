import pygraphviz as pgv

G=pgv.AGraph()

#d={'1': {'2': None}, '2': {'1': None, '3': None}, '3': {'2': None}}
d2={'fact_AB':{'tableA':None,'tableB':None},'agg_BC':{'fact_AB':None, 'tableA':None, 'tableB':None}}
A=pgv.AGraph(d2)

print(A)

### write to a file
A.write('output/graph/file.dot')

### write to an image
A.layout()
A.layout(prog='dot')

A.graph_attr['label']='Sample pygraphviz'
#A.node_attr['shape']='square'
A.edge_attr['color']='red'

A.draw('output/graph/file.png')
A.draw('output/graph/file.ps',prog='circo')