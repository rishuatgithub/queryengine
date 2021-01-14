import os
import sql_metadata
import pygraphviz as pgv

DATA_PATH='/Users/rishushrivastava/Document/GitHub/queryengine/data/'
GRAPH_OUTPUT_FILE='output/graph/sqlresultgraph.png'
GRAPH_OUTPUT_PSFILE='output/graph/sqlresultgraph.ps'

def get_files_in_path():
    '''
        generate the list of files and filenames
    '''
    files = [DATA_PATH+x for x in os.listdir(DATA_PATH)]
    #print(files)
    files_output = []
    for f in files:
        basefile = os.path.basename(f)
        files_output.append((f,basefile))

    return files_output


def generate_sql_graph(graph_nodes):
    '''
        generate graph for the sql generated
        @graph_node: a dict with graph dependencies
    '''
    print('Generating graph image')
    G=pgv.AGraph(graph_nodes)
    G.layout()
    G.layout(prog='dot')
    G.edge_attr['color']='red'
    
    G.draw(GRAPH_OUTPUT_FILE)
    G.draw(GRAPH_OUTPUT_PSFILE,prog='circo')
    

def parse_sql():
    '''
        parse sql
    '''
    files = get_files_in_path()
    result = {}
    for filepath, filename in files:
        with open(filepath,'r') as f:
            sql_data = f.read()

        get_tables = sql_metadata.get_query_tables(sql_data)
        source_table = filename.replace('.sql','')
        
        local_depends = {}
        
        for table in get_tables:
            if '.' in table:
                table_name = table.split('.')[1]
            else:
               table_name = table
            
            local_depends[table_name]=None
        
        result[source_table] = local_depends

    print(result)
    return result

if __name__ == '__main__':
    print("Starting parsing SQL files ")
    graphresult = parse_sql()
    generate_sql_graph(graphresult)