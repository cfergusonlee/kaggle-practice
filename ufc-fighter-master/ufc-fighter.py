"""
    A simple scraper to retrieve data from www.ufc.com
    in a predictable/easily machine readable format

    Copyright (c) 2016, Adrian Goris

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
    IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import codecs
import csv
import datetime
from bs4 import BeautifulSoup
import requests
import cStringIO
import pprint

class Scraper(object):

    """A collection of functions which can be used to retrieve and parse fight related data from sherdog.com"""

    # Base URL for all requests
    base_url = 'http://www.ufc.com'

    #----------------------------------+
    #  Dict object for Fighter
    #----------------------------------+
    fighter = {
        "name": "",
        "nickname": "",
        "fullname": "",
        "hometown": "",
        "location": "",
        "age": "",
        "height": "",
        "height_cm": "",
        "weight": "",
        "weight_kg": "",
        "record": "",
        "college": "",
        "degree": "",
        "summary": [],
        "strikes": {
          "attempted": 0,
          "successful": 0,
          "standing": 0,
          "clinch": 0,
          "ground": 0
          },
        "takedowns": {
          "attempted": 0,
          "successful": 0,
          "submissions": 0,
          "passes": 0,
          "sweeps": 0
        },
        "fights": []
      };


    @classmethod
    def fetch_url(self, url):

        # Fetch a url and return it's contents as a string

        uf = requests.get(url)
        return uf.text

    @classmethod
    def isNone(self, x):

        # Simple check if an object is None for use in building list comprehensions

        if x is not None:
            return False
        else:
            return True

    def name(self, soup):
        
        # Get the fighter's name from the supplied html soup
        
        try:
            name = soup.find('div', {'id' : 'fighter-details' })
            name = soup.find('h1').get_text()
        except AttributeError:
            name = None
        self.fighter["name"] = name
        return name

    def nickname(self, soup):

        # Get the fighter's nickname from the supplied html soup

        try:
            nickname = soup.find('td', {'id' : 'fighter-nickname' }).get_text()
        except AttributeError:
            nickname = None
        self.fighter["nickname"] = nickname
        return nickname

    def fullname(self, soup):

        # Get the fighter's full name from the supplied html soup

        try:
            fullname = soup.title.get_text()
            fullname = fullname.split("-")[0]
        except AttributeError:
            fullname = None
        self.fighter["fullname"] = fullname
        return fullname

    def hometown(self, soup):

        # Get the fighter's hometown from the supplied html soup
        # TODO: Remove line breaks, returns, and whitespaces

        try:
            hometown = soup.find('td', {'id' : 'fighter-from' }).get_text()
            hometown = hometown.strip()
        except AttributeError:
            hometown = None
        self.fighter["hometown"] = hometown
        return hometown

    def location(self, soup):

        # Get the fighter's listed location from the supplied html soup
        # TODO: Remove line breaks, returns, and whitespaces

        try:
            location = soup.find('td', {'id' : 'fighter-lives-in' }).get_text()
            location = location.strip()
        except AttributeError:
            location = None
        self.fighter["location"] = location
        return location

    def age(self, soup):

        # Get the fighter's age from the supplied html soup

        try:
            age = soup.find('td', {'id' : 'fighter-age' }).get_text()
            age = age.strip()
        except AttributeError:
            age = None
        self.fighter["age"] = age
        return age

    
    def height(self, soup):

        # Get the fighter's height from the supplied html soup
        # TODO: Break out into a dict for imperial and metric

        try:
            height = soup.find('td', {'id' : 'fighter-height' }).get_text()
            height = height.strip()
        except AttributeError:
            height = None
        self.fighter["height"] = height
        return height

    def weight(self, soup):

        # Get the fighter's weight from the supplied html soup
        # TODO: Break out into a dict for imperial and metric

        try:
            weight = soup.find('td', {'id' : 'fighter-weight' }).get_text()
            weight = weight.strip()
        except AttributeError:
            weight = None
        self.fighter["weight"] = weight
        return weight

    def record(self, soup):

        # Get the fighter's height from the supplied html soup
        # TODO: Break out into a dict for wins, loses, ties

        try:
            record = soup.find('td', {'id' : 'fighter-skill-record' }).get_text()
            record = record.strip()
        except AttributeError:
            record = None
        self.fighter["record"] = record
        return record

    def college(self,soup):

        # Get the fighter's college from the supplied html soup

        try:
            college = soup.find('td', {'id' : 'fighter-college' }).get_text()
            college = college.strip()
        except AttributeError:
            college = None
        self.fighter["college"] = college
        return college

    def degree(self,soup):

        # Get the fighter's height from the supplied html soup
        # TODO: Break out into a dict for wins, loses, ties

        try:
            degree = soup.find('td', {'id' : 'fighter-degree' }).get_text()
            degree = degree.strip()
        except AttributeError:
            degree = None
        self.fighter["degree"] = degree
        return degree

    def summary(self,soup):

        # Get the fighter's summary from the supplied html soup
        # TODO: Consider breaking out into a dictionary

        try:
            summary = soup.find('td', {'id' : 'fighter-skill-summary' }).get_text()
            summary = summary.strip()
        except AttributeError:
            summary = None
        self.fighter["summary"] = summary
        return summary

    def strikes(self,soup):

        # Get the fighter's strikes from the supplied html soup
        # TODO: CLEAN UP
        # TODO: Add error handleing

        fighter_striking_dict = {}

        # Striking Metrics
        fighter_strikes = soup.find('div', {'id' : 'fight-history' })
        fighter_strikes = fighter_strikes.findAll('div', {'class' : 'overall-stats' })[0]
        
        # Strikes attempted
        fighter_striking_dict["strikes_attempted"] = fighter_strikes.find('div', {'class' : 'max-number' }).get_text()
        # Strikes successfull
        fighter_striking_dict["strikes_successfull"] = fighter_strikes.find('div', {'id' : 'total-takedowns-number' }).get_text()
        
        # Strikes Type
        strikes_type = fighter_strikes.findAll('div', {'class' : 'text-bar' })
        strikes_type = [x.get_text() for x in strikes_type]
        fighter_striking_dict["strikes_standing"] = strikes_type[2]
        fighter_striking_dict["strikes_clinch"] = strikes_type[3]
        fighter_striking_dict["strikes_ground"] = strikes_type[4]

        self.fighter["strikes"] = fighter_striking_dict
        return fighter_striking_dict

    def takedowns(self,soup):

        # Get the fighter's takedowns from the supplied html soup
        # TODO: CLEAN UP
        # TODO: Add error handleing

        fighter_grapeling_dict = {}

        # Grapeling Metrics
        td_attempted = soup.findAll('div', {'class' : 'graph' })[2]
        td_successfull = soup.find('div', {'id' : 'grappling-totals-by-type-graph' })

        # Takedowns attempted
        fighter_grapeling_dict["takedowns_attempted"] = td_attempted.find('div', {'class' : 'max-number' }).get_text()
        # Takedowns successfull
        fighter_grapeling_dict["takedowns_successful"] = td_attempted.find('div', {'id' : 'total-takedowns-number' }).get_text()

        # Takedown type
        fighter_grapeling_dict["takedowns_submissions"] = td_successfull.find('div', {'id' : 'successful-submissions' }).get_text()
        fighter_grapeling_dict["successful_passes"] = td_successfull.find('div', {'id' : 'successful-passes' }).get_text()
        fighter_grapeling_dict["successful_sweeps"] = td_successfull.find('div', {'id' : 'successful-sweeps' }).get_text()

        self.fighter["takedowns"] = fighter_grapeling_dict
        return fighter_grapeling_dict

    def fights(self,soup):

        # Get the fighter's fights from the supplied html soup
        # TODO: CLEAN UP
        # TODO: Add error handleing

        fights = []

        fights_table = soup.find('table', {'id' : 'fights-table' }).findAll('tr',{'class':'fight'})

        for item in fights_table:
            fight = {}
            fighter = {}
            opponent = {}
            
            #tds have no class, or id to identify them by
            tds = item.findAll('td')

            #result
            fight['result'] = None

            #fighter_name
            fighter_name = item.find('td', {'class':'fighter'}).get_text()

            #opponent
            opponent_name = item.find('td', {'class':'fighter'}).get_text()

            #event
            event_dict = {}
            event = item.find('td', {'class':'event'}).get_text()
            event = event.strip().split('\n')
            event_name = event[0].strip()
            event_date = event[-1].strip()

            event_dict['name'] = event_name
            event_dict['date'] = event_date
            fight['event'] = event_dict

            #method
            method = item.find('td', {'class':'method'}).get_text()
            method = method.strip()
            fight['method'] = method

            #replay
            replay = item.find('td', {'class':'last'}).get_text()
            replay = replay.strip()
            fight['replay'] = replay

            #awards
            awards = item.find('td', {'class':'awards'}).get_text()
            awards = awards.strip()
            fight['awards'] = awards


            fight['fighter'] = fighter
            fight['opponent'] = opponent

            #strikes
            strikes = tds[3]    
            strikes = strikes.findAll('div')
            strikes = [x.get_text() for x in strikes]
            # fighter is 0, oppenent is 1
            fight['strikes'] = strikes
            fighter['strikes'] = strikes[0]
            opponent['strikes'] = strikes[1]


            #takedowns
            takedowns = tds[4]
            takedowns = takedowns.findAll('div')
            takedowns = [x.get_text() for x in takedowns]
            # fighter is 0, oppenent is 1
            fight['takedowns'] = takedowns
            fighter['takedowns'] = takedowns[0]
            opponent['takedowns'] = takedowns[1]


            #submissions
            submissions = tds[5]
            submissions = submissions.findAll('div')
            submissions = [x.get_text() for x in submissions]
            # fighter is 0, oppenent is 1
            fight['submissions'] = submissions
            fighter['submissions'] = submissions[0]
            opponent['submissions'] = submissions[1]


            #passes
            passes = tds[6]
            passes = passes.findAll('div')
            passes = [x.get_text() for x in passes]
            fight['passes'] = passes
            fighter['passes'] = passes[0]
            opponent['passes'] = passes[1]


            #end append to list
            fights.append(fight)

        self.fighter["fights"] = fights
        return fights


    def scrape_fighter(self, fighter_slug):

        # Retrieve and parse a fighter's details from www.ufc.com

        # fetch the required url and parse it

        url_content = self.fetch_url('%s/fighter/%s' % (self.base_url, fighter_slug))
        soup = BeautifulSoup(url_content, "html.parser")

        self.name(soup)
        self.nickname(soup)
        self.fullname(soup)
        self.hometown(soup)
        self.location(soup)
        self.age(soup)
        self.height(soup)
        self.weight(soup)
        self.record(soup)
        self.college(soup)
        self.degree(soup)
        self.summary(soup)
        self.strikes(soup)
        self.takedowns(soup)
        self.fights(soup)

        return self.fighter


class UnicodeWriter:

    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        try:
            self.writer.writerow([s.encode("utf-8") for s in row])
        except UnicodeDecodeError:
            self.writer.writerow(row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':

    # TODO: Remove Jon Jones Hard code
    # http://www.ufc.com/fighter/Jon-Jones
    
    scraper = Scraper()
    fighter = scraper.scrape_fighter("Jon-Jones")
    pprint.pprint(fighter)


