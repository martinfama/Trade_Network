import networkx as nx
import pandas as pd
import pycountry

def country_info(id_str=None):
    """
        args: str: the name or alpha_2 or alpha_3 code of a country
        returns: the dict returned by pycountry.countries.get()
    """
    country = None
    if len(id_str) == 2:
        country = pycountry.countries.get(alpha_2=id_str)
    elif len(id_str) == 3:
        country = pycountry.countries.get(alpha_3=id_str)
    elif len(id_str) > 3:
        country = pycountry.countries.get(name=id_str)
    else:
        raise ValueError('Invalid country name or code')
    return country

def country_exports_imports_yearly(G_Years=None, country=None):
    """
        Gets the yearly trade of a country, summing total imports and exports for all countries
        args: G_Years: a list of networkx DiGraphs
              country: the name or alpha_2 or alpha_3 code of the country
        returns: a 2D list, with the first column indicating exports, and the second column indicating imports, i.e.
                 Exports | Imports
                      ...|...
                      ...|...
    """
    # get alpha_3 code
    country = country_info(country).alpha_3
    yearly_trade = []
    for G in G_Years.values():
        country_index = list(G.nodes).index(country)
        A = nx.adjacency_matrix(G)
        yearly_trade.append([])
        yearly_trade[-1].append(A[country_index,:].sum()) #imports are sum of row
        yearly_trade[-1].append(A[:,country_index].sum()) #exports are sum of column
    return yearly_trade

def declining_imports_or_exports(G_Years=None, i_or_e='imports'):
    """
        Finds the countries which had incidents of imports/exports declining between two time intervals.
        args: G_Years: a list of networkx DiGraphs
              i_or_e: 'imports' or 'exports'
        returns: the list of countries
    """
    if i_or_e == 'imports': i_or_e = 0 
    else: i_or_e = 1
    declining_countries = []
    for country in list(G_Years.values())[0].nodes():
        # get the yearly trade
        yearly_trade = country_exports_imports_yearly(G_Years, country)
        for i in range(len(yearly_trade)-1):
            if yearly_trade[i+1][i_or_e] - yearly_trade[i][i_or_e] < 0:
                declining_countries.append(country)
                break
    return declining_countries

def get_centralities(G_Years=None, type_of_centrality='degree'):
    """
        Calculates the eigenvector centralities by year.
        args: G_Years: a list of networkx DiGraphs
        returns: a Pandas DataFrame, where rows are countries and columns are years, and entries are the eigenvector centralities
    """
    centralities = pd.DataFrame(index=list(G_Years.values())[0].nodes())
    for year in G_Years.keys():
        if type_of_centrality == 'degree':
            centralities[year] = nx.degree_centrality(G_Years[year]).values()
        elif type_of_centrality == 'eigenvector':
            centralities[year] = nx.eigenvector_centrality(G_Years[year]).values()
        elif type_of_centrality == 'betweenness':
            centralities[year] = nx.betweenness_centrality(G_Years[year]).values()
        elif type_of_centrality == 'closeness':
            centralities[year] = nx.closeness_centrality(G_Years[year]).values()
    return centralities
