from html.parser import HTMLParser
import urllib.request as urllib2

fields = {"creator": "",
          "title": "",
          "text": "",
          "dollarsPledged": "",
          "dollarsGoal": "",
          "numBackers": "",
          "daysToGo": "",
          "allOrNothing": False}

def reset_fields():
    fields["creator"] = ""
    fields["title"] = ""
    fields["text"] = ""
    fields["dollarsPledged"] = ""
    fields["dollarsGoal"] = ""
    fields["numBackers"] = ""
    fields["daysToGo"] = ""
    fields["allOrNothing"] = False

def fix_currency(data):
    return data.replace("\\xe2\\x82\\xac", "€").replace("\\xc2\\xa", "£")

class MyHTMLParser(HTMLParser):
    # Initializing lists
    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()
    lookingFor = ""
    gotBackers = False

    def handle_starttag(self, startTag, attrs):
        if startTag == "meta":
            if attrs[0][1] == "og:title":
                fields["title"] = attrs[1][1]
        if startTag == "span" and len(attrs) == 1:
            if attrs[0][1] == "ksr-green-500":
                if fields["dollarsPledged"] == "":
                    self.lookingFor = "dollarsPledged"
            if attrs[0][0] == "class" and attrs[0][1] == "money":
                if fields["dollarsGoal"] == "":
                    self.lookingFor = "dollarsGoal"
        if startTag == "div" and len(attrs) == 1:
            if attrs[0][1] == "type-14 bold":
                if fields["creator"] == "":
                    self.lookingFor = "creator"
            if attrs[0][1] == "ml5 ml0-lg mb4-lg":
                if fields["numBackers"] == "":
                    self.lookingFor = "backers"
            elif attrs[0][1] == "ml5 ml0-lg":
                if fields["daysToGo"] == "":
                    self.lookingFor = "daysToGo"

    def handle_data(self, data):
        if data == "All or nothing.":
            fields["allOrNothing"] = True
            return

        if self.lookingFor == "dollarsPledged":
            fields["dollarsPledged"] = fix_currency(data)
        elif self.lookingFor == "dollarsGoal":
            fields["dollarsGoal"] = fix_currency(data)
        elif self.lookingFor == "backers":
            fields["numBackers"] = data
        elif self.lookingFor == "creator":
            fields["creator"] = data
        elif self.lookingFor == "daysToGo":
            fields["daysToGo"] = data
        self.lookingFor = ""


def crawlPage(url):
    reset_fields()
    parser = MyHTMLParser()
    html_page = urllib2.urlopen(url)
    parser.feed(str(html_page.read()))
    return fields
