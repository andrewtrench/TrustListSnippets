import whois
import pickle
import datetime

'''Gets the whois data using the whois package and checks if the site is older than a year.'''


def check_whois(site):
    # Check for sites that are younger than a year
    try:
        w = whois.whois(site)
        # check date is older than one year
        print (w.creation_date)
        #print (f"This is the creation date {w.creation_date[0]}")
        try:
            created_date = w.creation_date[0]


        except Exception as e:
            created_date = w.creation_date
        if created_date > datetime.datetime.now() - datetime.timedelta(days=365):
            return True
        else:
            return False

    except Exception as e:
        print (f"Error {e} for {site}")
        return True


if __name__ == "__main__":
    # loads urls from pickle file but in production would be from db table
    # replace with data source as desired
    sites_to_check = pickle.load(open("to_check.p", "rb"))
    to_check_after_whois = []
    for site in sites_to_check:
        if check_whois(site):
            to_check_after_whois.append(site)

    # saves the urls that are younger than a year to a pickle file but in production would be to a db table
    pickle.dump(to_check_after_whois, open("to_check_after_whois.p", "wb"))
    print (f"Sites younger than a year{len(to_check_after_whois)}")