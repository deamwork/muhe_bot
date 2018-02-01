#!/usr/bin/python
#-*- coding:utf-8 -*-
# File Name: SearchCVE.py
# Author: o0xmuhe
# Mail: o0xmuhe@gmail.com
# Created Time: 2018-01-31 19:20:29

import requests
import json

BASE_URL = "http://cve.circl.lu/api"
LASTEST_CVE_URL = "http://cve.circl.lu/api/last"

def emptyJson():
    return json.loads("{}")


def getJSONData(url):
    try:
        r = requests.get(url)
        return json.loads(r.text)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return emptyJson()
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return emptyJson()
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return emptyJson()
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        return emptyJson()


def getAllVendors():
    '''
        Get all vendors.
        Return a vendors list.
    '''
    try:
        url = BASE_URL + '/browse'
        return getJSONData(url)['vendor']
    except Exception as e:
        # error
        return "None"


def getProductsByVendor(target):
    '''
        Get target's vendor.
        Return all products of vendor.
    '''
    try:
        url = BASE_URL + '/browse/{0}'.format(target)
        return getJSONData(url)['product']
    except Exception as e:
        # no such a vendor
        return "None"


def getLastCVEs():
    '''
        Get the last cve info.
    '''
    url = LASTEST_CVE_URL
    return getJSONData(url)


def searchVendorProduct(vendor,product):
    '''
        Get product info.
        Return CVE data of this product with json format.
    '''
    url = BASE_URL + '/search/{0}/{1}'.format(vendor,product)
    return getJSONData(url)


def searchCVEDetails(cve):
    '''
        Get CVE info by cve id.
        format:
                cve-xxxx-xxxx
        Return CVE info with json data.
    '''
    url = BASE_URL + '/cve/{0}'.format(cve)
    return getJSONData(url)


def main():
    # print getAllVendors()
    # raw_input('$')
    # print getProductsByVendor('adobe')
    # raw_input('$')
    # data = getLastCVEs()
    # print data[0]
    # raw_input('$')
    # print searchVendorProduct('microsoft','office')
    # raw_input('$')
    # data = searchCVEDetails('cve-2010-3333')
    # print data
    pass



if __name__ == '__main__':
    main()
