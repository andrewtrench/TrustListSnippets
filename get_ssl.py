import ssl
import socket
import pickle
import concurrent.futures
'''Check if a site in the list has an SSL certificate or if it is still connectable'''

def check_ssl_certificate(hostname):
    '''Check if a site in the list has an SSL certificate or if it is still connectable'''
    context = ssl.create_default_context()
    s = context.wrap_socket(socket.socket(), server_hostname=hostname)
    s.connect((hostname, 443))
    certificate = s.getpeercert()
    if certificate:
        return True
    else:
        return False

if __name__ == "__main__":
    # this loads URLS to check from a pickle file but obviously would be handled by database or other source in production
    # Replace with data source of your choice
    urls_to_check = pickle.load(open("to_check.p", "rb"))
    urls_left = len(urls_to_check)
    bad_certs = []
    # this uses the concurrent.futures module to run the checks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Sets up a dictionary of futures to URLs so we can track which URL generated which exception
        executor.map(check_ssl_certificate, urls_to_check)
        future_to_url = {executor.submit(check_ssl_certificate, url): url for url in urls_to_check}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            urls_left -= 1
            print (f"{urls_left} left")
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
                bad_certs.append(url)
            else:
                if not data:
                    bad_certs.append(url)
    print (f"Bad certs: {len(bad_certs)}")
    # saved the urls with bad certiciactes to a pickle file but this would write to a db table in production
    pickle.dump(bad_certs, open("bad_certs.p", "wb"))
