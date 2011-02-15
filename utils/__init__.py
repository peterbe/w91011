# python
import datetime
import string
import random

from render_decorator import render

from decorators import staff_required, superuser_required

def nicepass(alpha=6,numeric=2):
    """
    returns a human-readble password (say rol86din instead of
    a difficult to remember K8Yn9muL )
    """

    vowels = ['a','e','i','o','u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    digits = string.digits

    ####utility functions
    def a_part(slen):
        ret = ''
        for i in range(slen):
            if i%2 ==0:
                randid = random.randint(0,20) #number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0,4) #number of vowels
                ret += vowels[randid]
        return ret

    def n_part(slen):
        ret = ''
        for i in range(slen):
            randid = random.randint(0,9) #number of digits
            ret += digits[randid]
        return ret

    ####
    fpl = alpha/2
    if alpha % 2 :
        fpl = int(alpha/2) + 1
    lpl = alpha - fpl

    start = a_part(fpl)
    mid = n_part(numeric)
    end = a_part(lpl)

    return "%s%s%s" % (start,mid,end)


def email_to_username(email):
    return email.replace('@','').replace('.','').replace('+','')[:30]


def mobile_to_msisdn(number):
    number = number.replace(' ','').replace('-','')
    if number.startswith('0') and not number.startswith('00'):
        # UK!
        number = '44' + number[1:]
    elif number.startswith('+'):
        number = number[1:]
    return number


def niceboolean(value):
    if type(value) is bool:
        return value
    falseness = ('','no','off','false','none','0', 'f')
    return str(value).lower().strip() not in falseness


def date2datetime(date):
    return datetime.datetime(date.year, date.month, date.day)


def ordinalth(n):
    if n % 100 in (11, 12, 13): #special case
        return '%dth' % n
    t = 'th st nd rd th th th th th th'.split()
    return str(n) + t[n % 10]
