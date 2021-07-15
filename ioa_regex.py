import re


class findIoA():

    def _init_(sentence):
        self.sentence = sentence

    def cve(self):
        if len(self.sentence) > 0:
            return re.findall(r"CVE-\d{4}-\d{4,7}", self.sentence)
        else:
            print("Invalid Sentence")

    def md5(self):
        if len(self.sentence) > 0:
            return re.findall(r"([a-fA-F\d]{32})", self.sentence)
        else:
            print("Invalid Sentence")

    def url(self):
        if len(self.sentence) > 0:
            return re.findall(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", self.sentence)
        else:
            print("Invalid Sentence")

    def reg_keys(self):
        if len(self.sentence) > 0:
            return re.findall(r"((?:[HK][A-Z\_]+|[A-Z]+)\+\s+(?:.*)\+[a-zA-Z]+)", self.sentence)
        else:
            print("Invalid Sentence")

    def ip(self):
        if len(self.sentence) > 0:
            return re.findall(r"(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))", self.sentence)
        else:
            print("Invalid Sentence")

    def email(self):
        if len(self.sentence) > 0:
            return re.findall(r"((?:[a-zA-Z0-9.]+)@(?:[a-z]+.)(?:[a-z]{2,62}.[a-z]{2}|[a-z]{2,62}))", self.sentence)

    def find_ioc(self):
        iocs = {}
        iocs['cve'] = self.cve()
        iocs['md5'] = self.md5()
        iocs['url'] = self.url()
        iocs['reg'] = self.reg_keys()
        iocs['ip'] = self.ip()
        iocs['email'] = self.email()
        return iocs


def main():
    """Example of usage"""
    test_sentence = "CVE-2018-19360, CVE-2018-19360, FasterXML jackson-databind 2.x before 2.9.8 might allow attackers to have unspecified impact by leveraging failure to block the axis2-transport-jms class from polymorphic deserialization.  http://bit.ly/2R3qxQo"
    a = findIoA()
    a.sentence = test_sentence
    print(a.find_ioc())

if __name__ == "__main__":
    main()
