import concurrent
import pandas as pd
import pickle
import pandas as pd
import requests


def check_ads_text(url):
    response = requests.get(f"https://{url}/ads.txt", timeout=5)
    # print(response.text)
    if response.status_code == 200:
        print("ads.txt file found")
        found = True
        response.close()
    else:
        print("ads.txt file not found")
        found = False
        response.close()
    return found

if __name__ == "__main__":
    result_dict = {}
    # read in the list of urls from an excel file to do them in bulk and in a threaded manner for speed
    urls_to_check = pd.read_excel("global_news_sites.xlsx")['url'].to_list()
    #print(len(urls_to_check))
    no_of_urls = len(urls_to_check)
    # check each url for the ads.txt file. If it exists, return True, else return False
    # this is done in a threaded manner for speed
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(check_ads_text, url): url for url in urls_to_check}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            no_of_urls -= 1
            #print(f"{no_of_urls}: {url}")
            try:
                result_dict[url] = future.result()
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                result_dict[url] = "Connection Error"
            except requests.exceptions.ReadTimeout:
                print("Read Timeout")
                result_dict[url] = "Read Timeout"
    # create a pandas dataframe from the dictionary and save it to an excel file.
    # This of course could be saved direct to a database
    df = pd.DataFrame.from_dict(result_dict, orient='index', columns=['ads.txt'])
    df.to_excel("ads_txt.xlsx")
    print (df['ads.txt'].value_counts()) # this is just to show the results
