import pandas as pd
import pickle
'''This checks to see if the file is in top 1m. This is done manually against the top-1m.csv file.
But should rather be done against a table in the database based on the latest data from Tranco which we ingest programmatically.
Details here https://tranco-list.eu/'''




def check_in_top_1m(audit_sites_path):
    '''Takes input of path to the audit sites file and checks if the sites are in the top 1m in the world'''
    # read the top-1m.csv file into a dataframe
    top_1m_df = pd.read_csv('top-1m.csv')
    # if the dataframe has no column names
    if not top_1m_df.columns.names:
        # assign a list of column names to the dataframe
        top_1m_df.columns = ['rank', 'site']
    print (top_1m_df.head())
    # get the sample data sites
    df_sample = pd.read_excel(f"{audit_sites_path}")

    # convert the sites column to a list
    sites = df_sample['Placement'].to_list()

    # check if the sites are in the top-1m.csv file
    counts = top_1m_df['site'].isin(sites).value_counts()
    print(counts)
    counts_list = top_1m_df.loc[top_1m_df['site'].isin(sites)]['site'].to_list()

    # Dump the list of sites in top 1m to a pickle file. In the workflow this url would be marked as True for having a
    # presence in top 1m and then would be checked for its historic data. If both passes are True it would be saved to
    # the db as a safe site.

    pickle.dump(counts_list, open("sites_in_top1m.p", "wb"))

    # list the unranked sites
    to_check = [site for site in sites if site not in top_1m_df['site'].to_list()]
    # save the unranked sites to a pickle file. In the workflow this url would be passed on for further processing
    pickle.dump(to_check, open("to_check.p", "wb"))

    print ("Number of sites not in top 1m in the world")
    print (len(to_check))


if __name__ == "__main__":
    audit_sites_path = "placement_data_sites.xlsx"
    check_in_top_1m(audit_sites_path)
