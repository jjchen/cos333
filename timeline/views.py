# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
import sys, os, cgi, urllib, re
#from polls.models import Poll


form = cgi.FieldStorage()

class CASClient:
   def __init__(self, request, url='https://fed.princeton.edu/cas/'):
      self.request = request
      self.cas_url = url

   def Authenticate(self):
      # If the request contains a login ticket, try to validate it
      if form.has_key('ticket'):
         netid = self.Validate(form['ticket'].value)
         if netid != None:
            return netid
      # No valid ticket; redirect the browser to the login page to get one
      login_url = self.cas_url + 'login' \
         + '?service=' + urllib.quote(self.ServiceURL())
      print 'Location: ' + login_url
      print 'Status-line: HTTP/1.1 307 Temporary Redirect'
      print ""
#      return login_url
      sys.exit(0)

   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?service=' + urllib.quote(self.ServiceURL()) + \
         '&ticket=' + urllib.quote(ticket)
      #val_url = self.cas_url + "serviceValidate" + \
      #   '?service=' + urllib.quote(self.ServiceURL()) + \
      #   '&ticket=' + urllib.quote(ticket)  # new
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return r[1].strip()
      return None

   def ServiceURL(self):
      return "bobcats"
#      if os.environ.has_key('REQUEST_URI'):
      if self.request != None:
#         ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
         ret = self.request.build_absolute_uri()
         ret = re.sub(r'ticket=[^&]*&?', '', ret)
         ret = re.sub(r'\?&?$|&$', '', ret)
         return ret
         #$url = preg_replace('/ticket=[^&]*&?/', '', $url);
         #return preg_replace('/?&?$|&$/', '', $url);
      return "something is badly wrong"

# https://fed.princeton.edu/cas/
#  validate?ticket=ST-3555-McPZ4NKfx6S0EhnCEkHc
#  &service=https://www.applyweb.com/proto/auth/cas/princeton

def main():
  print "CASClient does not run standalone"

if __name__ == '__main__':
  main()

def index(request):
    client = CASClient(request)
    login_url = client.Authenticate()
#    return render_to_response(login_url)
    print login_url
#    login_url="oc_app"
    return HttpResponseRedirect(login_url)
    return render_to_response('timeline/fancytimeline.html')
