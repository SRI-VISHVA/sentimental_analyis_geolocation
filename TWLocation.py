from twitter import *
import csv
import time
import gmplot


def mapping(latitude_list, longitude_list, latitude, longitude):
    gmap5 = gmplot.GoogleMapPlotter(latitude,
                                    longitude, 13)

    gmap5.scatter(latitude_list, longitude_list, '# FF0000',
                  size=40, marker=False)

    # polygon method Draw a polygon with
    # the help of coordinates
    gmap5.polygon(latitude_list, longitude_list,
                  color='cornflowerblue')
    gmap5.draw("map.html")


def tweetlocation():
    try:

        consumer_key = 'RX1TfloBW5z32QGbWalCI8HXE'
        consumer_secret = 'izfNCz9LMwHVVWTtqIWwtN3PQHpdFySPV802sHKjLeypxHSRW6'
        access_token = '1198600156523847681-Foy5c01lD7Hwnt3WTteiuo6iqmLISA'
        access_token_secret = 'o3eX3XO1KOUpx2qniMcKpBzz0d5v5qlHQG5Qqnvyc4Pvi'

        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'

        latitude = float(input(bcolors.OKGREEN + 'Enter the Latitude: ' + bcolors.ENDC))
        longitude = float(input(bcolors.OKGREEN + 'Enter the Longitude: ' + bcolors.ENDC))
        max_range = float(input(bcolors.OKGREEN + 'Enter the Range: ' + bcolors.ENDC))
        num_results = input(bcolors.OKGREEN + 'Enter the Number of results: ' + bcolors.ENDC)
        outfile = "output.csv"

        # create twitter API object
        twitter = Twitter(
            auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

        # open a file to write (mode "w"), and create a CSV writer object
        csvfile = open(outfile, 'w')
        csvwriter = csv.writer(csvfile)

        # add headings to our CSV file
        row = ["Username", "Profile URL", "Latitude", "Longitude", "Google Maps", "Tweet"]
        csvwriter.writerow(row)
        result_count = 0
        last_id = None
        latitude_list = []
        longitude_list = []
        while result_count < int(num_results):

            # perform a search based on latitude and longitude
            query = twitter.search.tweets(q="", geocode="%f,%f,%dkm" % (latitude, longitude, max_range),
                                          num_results=100,
                                          max_id=last_id)
            for result in query["statuses"]:

                # only process a result if it has a geolocation
                if result["geo"]:
                    user = result["user"]["screen_name"]
                    text = result["text"]
                    text = text.encode('ascii', 'replace')
                    latitude = result["geo"]["coordinates"][0]
                    longitude = result["geo"]["coordinates"][1]
                    url = 'https://twitter.com/%s' % user
                    gurl = 'https://maps.google.com/?q=' + str(latitude) + ',' + str(longitude)
                    latitude_list.append(latitude)
                    longitude_list.append(longitude)
                    # now write this row to our CSV file
                    row = [user, url, latitude, longitude, gurl, text]
                    print('-----------------------------------------------------------------')
                    print(' ')
                    print(bcolors.OKGREEN + 'Username:    ' + bcolors.ENDC, user)
                    print(bcolors.OKGREEN + 'Profile URL: ' + bcolors.ENDC, url)
                    print(bcolors.OKGREEN + 'Latitude:    ' + bcolors.ENDC, latitude)
                    print(bcolors.OKGREEN + 'Longitude:   ' + bcolors.ENDC, longitude)
                    print(bcolors.OKGREEN + 'Google Maps: ' + bcolors.ENDC, gurl)
                    print(bcolors.OKGREEN + 'Tweet:       ' + bcolors.ENDC, text)
                    print(' ')
                    csvwriter.writerow(row)
                    result_count += 1
                    time.sleep(.35)
                last_id = result["id"]

        # let the user know where we're up to

        if result_count == 1:
            print(bcolors.WARNING + "Got %d result" % result_count + bcolors.ENDC)
            csvfile.close()
            print(bcolors.WARNING + "Saved to ", outfile + bcolors.ENDC)
        elif result_count == 0:
            print(bcolors.WARNING + "Didn't get any results try another Latitude and  Longitude" + bcolors.ENDC)
        else:
            print(bcolors.WARNING + "Got %d results" % result_count + bcolors.ENDC)
            csvfile.close()
            print(bcolors.WARNING + "Saved to ", outfile + bcolors.ENDC)
        mapping(latitude_list, longitude_list, latitude, longitude)
    # we're all finished, clean up and go home.
    except ImportError:
        print('''There was an error
    Please install the requirements:
    pip install -r requirements.txt''')

    except TwitterHTTPError:
        print("Invalid Location, Please change your Location.")
