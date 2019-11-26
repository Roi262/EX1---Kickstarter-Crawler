from html.parser import HTMLParser
import urllib.request as urllib2


class Reward:
    def __init__(self):
        self.text = ""
        self.price = ""
        self.numBackers = ""
        self.totalPossibleBackers = "unlimited"

    def __str__(self):
        return "Text: " + self.text + " Price: " + self.price + " numBackers: " + self.numBackers \
                + " totalPossibleBackers: " + self.totalPossibleBackers

    def get_dict(self):
        return {"text": self.text, "price": self.price,
                "numBackers": self.numBackers, "totalPossibleBackers": self.totalPossibleBackers}

fields = {"ID": "",
          "creator": "",
          "title": "",
          "text": "",
          "dollarsPledged": "",
          "dollarsGoal": "",
          "numBackers": "",
          "daysToGo": "",
          "allOrNothing": False,
          "rewards": []}


def getCurrentReward():
    return fields["rewards"][-1]


def reset_fields(ID):
    fields["ID"] = str(ID)
    fields["creator"] = ""
    fields["title"] = ""
    fields["text"] = ""
    fields["dollarsPledged"] = ""
    fields["dollarsGoal"] = ""
    fields["numBackers"] = ""
    fields["daysToGo"] = ""
    fields["allOrNothing"] = False
    fields["rewards"] = []


def fix_currency(data):
    return data.replace("\\xe2\\x82\\xac", "Euro ").replace("\\xc2\\xa3", "GBP ")

class MyHTMLParser(HTMLParser):
    # Initializing lists
    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()
    lookingFor = ""
    lookingForRewards = False

    def handle_starttag(self, startTag, attrs):
        if startTag == "meta":
            if attrs[0][1] == "og:title":
                fields["title"] = attrs[1][1]
        if startTag == "span" and len(attrs) == 1:
            if attrs[0][1] == "ksr-green-500":
                if fields["dollarsPledged"] == "":
                    self.lookingFor = "dollarsPledged"
            if attrs[0][0] == "class" and attrs[0][1] == "money":
                if self.lookingForRewards:
                    self.lookingFor = "rewardData_price"
                elif fields["dollarsGoal"] == "":
                    self.lookingFor = "dollarsGoal"
            if attrs[0][0] == "class" and (attrs[0][1] == "pledge__backer-count"
                                           or attrs[0][1] == "block pledge__backer-count"):
                self.lookingFor = "rewardData_numBackers"
            if attrs[0][0] == "class" and attrs[0][1] == "pledge__limit":
                self.lookingFor = "rewardData_totalPossibleBackers"
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
            elif attrs[0][1] == "pledge__reward-description pledge__reward-description--expanded":
                self.lookingFor = "rewardData_text"
        if startTag == "h2" and attrs[0][1] == "pledge__amount":
            self.lookingForRewards = True

    def handle_data(self, data):
        data = fix_currency(data)
        if data == "All or nothing.":
            fields["allOrNothing"] = True
            return

        elif self.lookingFor.startswith("rewardData"):
            if data == "Make a pledge without a reward":
                self.lookingForRewards = False
                return
            if self.lookingFor == "rewardData_price":
                fields["rewards"].append(Reward())
                getCurrentReward().price = data
            elif self.lookingFor == "rewardData_numBackers":
                getCurrentReward().numBackers = data.replace(" backers", "").replace("\\n", "")
                self.lookingForRewards = False
            elif self.lookingFor == "rewardData_totalPossibleBackers":
                getCurrentReward().totalPossibleBackers = data.replace("\\n", "").split(" ")[-1][:-1]
            elif self.lookingFor == "rewardData_text":
                if data.endswith("% off") or data.endswith("% off\\n"):
                    return
                if data == "\\n":
                    return
                getCurrentReward().text = data

        elif self.lookingFor == "dollarsPledged":
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


def crawlPage(url, ID):
    reset_fields(ID)
    parser = MyHTMLParser()
    html_page = urllib2.urlopen(url)
    parser.feed(str(html_page.read()))
    fields["rewards"] = [r.get_dict() for r in fields["rewards"]]
    return fields


