import requests
import logging
import sys

DpCsvFileName = 'data/diamond.csv'
# Notes
# Split the long link Just for visibility
DpTmpLinkPart1 = 'https://raw.githubusercontent.com/Chinmayrane16'
DpTmpLinkPart2 = '/Diamonds-In-Depth-Analysis/master/diamonds.csv'
DpLink = DpTmpLinkPart1 + DpTmpLinkPart2


def DpFetchDB(fileName=DpCsvFileName):
    # For Debug
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    try:
        DpTmpResponse = requests.get(DpLink)
        # ToDo:
        # Insert timeout variabl to the get() function.
        # Make it RESTfull api.
        # _____
        # Notes:
        # Code down here in the block will only run only
        # if the request is successful.
        DpDiamondUrlContent = DpTmpResponse.content
        DpTextDiamondCSV = open(fileName, 'wb')
        DpTextDiamondCSV.write(DpDiamondUrlContent)
        DpTextDiamondCSV.close()
        # ToDo
        # Chack if the files can be opened and written to the container.
        # Save diffrent version with time stamp to DB

    except requests.exceptions.HTTPError as errh:
        print(errh)

    except requests.exceptions.ConnectionError as errc:
        print(errc)

    except requests.exceptions.Timeout as errt:
        print(errt)

    except requests.exceptions.RequestException as err:
        print(err)

    logging.debug('response status code is %d', DpTmpResponse.status_code)
    if (DpTmpResponse.status_code > 200):
        return -1
