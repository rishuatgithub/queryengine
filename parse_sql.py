import os
import sql_metadata
import pygraphviz as pgv
import pandas as pd
import argparse

def get_arguments():
    '''
        Generate a parameters parser
    '''
    parser = argparse.ArgumentParser(description="Get the arguments for parse sql")

    parser.add_argument("--data_path", type=str, 
        default=''.join((os.path.realpath('.'),'/data')),
        help="Data Path for the SQL. Accepts only .sql files")

    parser.add_argument("--graph_output_file", type=str, 
        default="output/graph/sqlresultgraph.svg", 
        help="Output filename of the generated graph file")

    parser.add_argument("--graph_output_psfile", type=str, 
        default="output/graph/sqlresultgraph.ps", 
        help="Output filename of the .ps file")

    parser.add_argument("--csv_output_file", type=str, 
        default="output/file/sqlresult.csv", 
        help="Output CSV filename of the parsed sqls")

    return parser



def get_files_in_path(params):
    '''
        generate the list of files and filenames
    '''
    files_output = []
    for pathroot, pathdir, files in os.walk(params.data_path):
        for f in files:
            if '.sql' in f:
                files_output.append((os.path.join(pathroot, f),f))

    #print(files_output)
    return files_output


def generate_sql_graph(graph_nodes, params):
    '''
        generate graph for the sql generated
        @graph_node: a dict with graph dependencies
    '''
    print('Generating graph image')
    G=pgv.AGraph(graph_nodes)
    G.layout()
    G.layout(prog='dot')
    G.edge_attr['color']='red'
    
    G.draw(params.graph_output_file)
    G.draw(params.graph_output_psfile,prog='circo')
    

def generate_csv(parse_data, params):
    '''
        Generating csv from dictionary of data
    '''
    print('Generating CSV file based on the parsed data')
    dataset = {}
    source_list = []
    target_list = []
    items = parse_data.items()
    for pkey, pvalue in items:
        for ckey, cvalue in pvalue.items():
            source_list.append(pkey)
            target_list.append(ckey)
    dataset['Source'] = source_list
    dataset['Target'] = target_list

    pd_dataset = pd.DataFrame(dataset)
    
    pd_dataset.to_csv(params.csv_output_file, index=False)
        

def parse_sql(params):
    '''
        parse sql
    '''
    files = get_files_in_path(params)
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

    #print(result)
    return result

if __name__ == '__main__':

    print("Starting parsing SQL files ")
    parser = get_arguments()
    params = parser.parse_args()

    print("Parameters Passed :", params)

    ## actual execution
    graphresult = parse_sql(params)
    generate_csv(graphresult, params)
    generate_sql_graph(graphresult, params)