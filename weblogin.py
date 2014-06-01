# -*- coding: UTF-8 -*-

"""
 weblogin
 by Anarchintosh @ xbmcforums
 Copyleft (GNU GPL v3) 2011 onwards

 this example is configured for Fantasti.cc login
 See for the full guide please visit:
 http://forum.xbmc.org/showthread.php?p=772597#post772597


 USAGE:
 in your default.py put:

 import weblogin
 logged_in = weblogin.doLogin('a-path-to-save-the-cookie-to','the-username','the-password')

 logged_in will then be either True or False depending on whether the login was successful.
"""

import os
import re
import urllib,urllib2
import cookielib

### TESTING SETTINGS (will only be used when running this file independent of your addon)
# Remember to clear these after you are finished testing,
# so that your sensitive details are not in your source code.
# These are only used in the:  if __name__ == "__main__"   thing at the bottom of this script.

#initiate the cookielib class
cj = cookielib.LWPCookieJar()
        
#install cookielib into the url opener, so that cookies are handled
opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
    urllib2.HTTPHandler(),urllib2.HTTPSHandler(),urllib2.HTTPCookieProcessor(cj))

#the header used to pretend you are a browser
header_string = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'

#note, the cookie will be saved to the same directory as weblogin.py when testing


def check_login(source):
    
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = b'Welcome to Bayyinah TV'

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False

def check_if_logged_in(cookiepath):

#check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath = os.path.join(cookiepath,'cookies.lwp')

    if os.path.exists(cookiepath) == False:
        return False
    
    cj.load(cookiepath)
    req = urllib2.Request('http://www.bayyinah.tv/dashboard')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
    req.add_header('Connection','keep-alive')
    req.add_header('Host','www.bayyinah.tv')		
    req.add_header('User-Agent',header_string)
    response = opener.open(req)
    source = response.read()
    response.close()		

    #check the received html for a string that will tell us if the user is logged in
    #pass the username, which can be used to do this.
    login = check_login(source)

    return login


def doLogin(cookiepath,username, password):
    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath = os.path.join(cookiepath,'cookies.lwp')
        
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:

        #the url you will request to.
        login_url = 'http://www.bayyinah.tv/user_sessions'
 	
        #build the request we will make
        req = urllib2.Request('http://www.bayyinah.tv/login')
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)	
        
        response = opener.open(req)
        source = response.read()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(source)
        token = soup.find("input", { 'name': 'authenticity_token'})
		
       
        #build the form data necessary for the login
        login_data = urllib.urlencode({'authenticity_token':token['value'], 'user_session[email]':username,
                                             'user_session[password]':password, 'user_session[remember_me]':0,'x':57,'y':22})
        binary_data = login_data.encode('ascii')
		
        #build the request we will make
        req = urllib2.Request(login_url, binary_data)
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)
        	
		
        #do the login and get the response
        print('Sending login request')
        response = opener.open(req) 
        source = response.read()
        print('Login request made')

        req = urllib2.Request('http://www.bayyinah.tv/dashboard')
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)
        response = opener.open(req)
        source = response.read()
        response.close()		

        #check the received html for a string that will tell us if the user is logged in
        #pass the username, which can be used to do this.
        login = check_login(source)

        #if login suceeded, save the cookiejar to disk
        if login == True:
            cj.save(cookiepath)

        #return whether we are logged in or not
        return login
    
    else:
        return False
