import pycountry
import requests
import time
import os
import sys
from flask import Flask, request

app = Flask(__name__)

if os.environ.get('FLAG', '').strip() == '':
	os.environ['FLAG'] = "flag{Q29uZ3JhdHMsIGdvb2QgZ2FtZSE=}"
    

country_api_addr = "https://api.country.is/"
counter_requests = 0
minimum_countries = 10
seconds_permitted = 15
country_list = []
start_time = 0
success = False


@app.route("/")
def index():
    global start_time, minimum_countries, country_list, success

    new_unique_request = ""
    response_success = "<p>Well done! You visited from these countries: " + str(
        country_list) + ". Your flag is: " + os.environ['FLAG'] + ".</p>"
    response_unique = "<p>Hello from " + new_unique_request + "! \n\n\n You have visited from these countries: " + str(
        country_list) + "</p>"
    response_non_unique = "<p>That's not unique! \n\n\n You have visited from these countries: " + str(country_list) + \
                          ", why don't you try a new one.</p>"
    response_fail = "<p>Sorry! You're out of time. You visited from: " + str(reset()) + " unique countries. " \
                                                                                        "The timer has been stopped " \
                                                                                        "and will restart on the " \
                                                                                        "next request.</p>"

    if not success:
        new_unique_request = visit()
    else:
        return response_success

    if start_time == 0:
        start_time = time.time()
        return response_unique
    elif len(country_list) >= minimum_countries:
        success = True
        return response_success
    elif round((time.time() - start_time), 2) >= 15 and not success:
        return response_fail
    else:
        if new_unique_request != "":
            return response_unique
        else:
            return response_non_unique


def reset():
    global start_time, country_list, counter_requests
    start_time = 0
    countries_visited = country_list
    country_list = []
    counter_requests = 0
    return countries_visited


# Get origin country of IP req, add to counters if unique
def visit():
    global country_list
    unique_country = ""  # Set to unique country or null if not
    request_ip = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    json_country = requests.get(country_api_addr + request_ip).json()  # Replace testing_ip/request_ip etc
    country = pycountry.countries.get(alpha_2=str(json_country["country"]))
    if country.flag not in country_list:
        country_list.append(country.flag)
        unique_country = country.name
        print(country.flag + "unique countries: " + str(len(country_list)))
    return unique_country
