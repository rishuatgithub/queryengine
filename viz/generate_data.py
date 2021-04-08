import pandas as pd 
from jinja2 import Template

nodeTemplate = Template("   \
    { key: 'PersistanceStage', isGroup: true}, \
    \n { key: 'IntermediaryLayer', isGroup: true}, \
    {% for node, group in nodelist %} \
    \n { key: '{{ node }}', group: '{{ group }}' },\
    {% endfor %} ")

baseConnectedTemplate = Template(" \
    {% for data in baseConnectedNodes %} \
    \n {from: '{{ data[0] }}', to: '{{ data[1] }}'}, \
    {% endfor %} \
")

data = pd.read_excel('../data/data.xlsx', engine='openpyxl')

nodes = [ node for node in data['Object_Name']]
node_layer = [ node for node in data['LayerName']]

nodeDict = nodeTemplate.render(nodelist=zip(nodes, node_layer))

#print(nodeDict)

connected_df = data[['Object_Name','Connected_Nodes']].dropna()
connected_node_list = [tuple(vals) for vals in connected_df.values]

baseConnectedDict = baseConnectedTemplate.render(baseConnectedNodes=connected_node_list)

parent_connected_df = data[['Object_Parent','Object_Name']].dropna()
parent_connected_node_list = [tuple(vals) for vals in parent_connected_df.values]

parent_baseConnectedDict = baseConnectedTemplate.render(baseConnectedNodes=parent_connected_node_list)

def writeToFile(filename, data):
    with open(filename,'w') as out:
        out.write(data)

writeToFile('output/nodes.txt', nodeDict)
writeToFile('output/connected_nodes.txt', baseConnectedDict)
writeToFile('output/parent_connected_nodes.txt', parent_baseConnectedDict)