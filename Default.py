import os,urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,weblogin,cookielib

#Bayyinah TV - Code Crimson Inc

__addonname__ = 'plugin.video.bayyinahtv'
__addon__ = xbmcaddon.Addon()
__datapath__ = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode("utf-8")
__icon__ = __addon__.getAddonInfo('icon')
__cookiepath__ = os.path.join(__datapath__,'cookies.lwp')
__username__ = ''
__password__ = ''

#the header used to pretend you are a browser
header_string = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'

#initiate the cookielib class
cj = cookielib.LWPCookieJar()

def AUTHCHECK():
        logged_in = weblogin.check_if_logged_in(__datapath__)
        if logged_in == False:
                logged_in = weblogin.doLogin(__cookiepath__,__username__,__password__)
            
        if logged_in == True:
                cj.load(__cookiepath__)
      
def CATEGORIES():                
        addDir('COURSES','http://www.bayyinah.tv/categories/137959',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/137959/small/4_Series.jpg?1372522400')
        addDir('RAMADAN','http://www.bayyinah.tv/categories/137658',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/137658/small/bonus.png?1372357554')
        addDir('EXTRAS','http://www.bayyinah.tv/categories/138762',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/138762/small/icon-universe.png?1372890269')
                       
def INDEX(url):
        AUTHCHECK()        
        req = urllib2.Request(url)
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(),urllib2.HTTPSHandler(),urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        source = response.read()
        response.close()
        match=re.compile(b'src="(.+?)" width="64" />\n  </div>\n\t<div class="list-details">\n\t\t<div class="list-title"><a href="(.+?)">(.+?)</a> </div>').findall(source)                
        print(match)
        for thumbnail,url,name in match:
                addDir(name,'http://www.bayyinah.tv'+url,2,thumbnail)

def INDEX2(url):
        AUTHCHECK()        
        req = urllib2.Request(url)
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(),urllib2.HTTPSHandler(),urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        source = response.read()
        response.close()
        match=re.compile(b'src="(.+?)" width="64" />\n  </div>\n\t<div class="list-details">\n\t\t<div class="list-title"><a href="(.+?)">(.+?)</a> </div>').findall(source)                
        print(match)
        for thumbnail,url,name in match:
                addDir(name,'http://www.bayyinah.tv'+url,3,thumbnail)

def VIDEOLINKS(url,name):
        AUTHCHECK()        
        req = urllib2.Request(url)
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language','en-GB,en-US;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','www.bayyinah.tv')		
        req.add_header('User-Agent',header_string)
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(),urllib2.HTTPSHandler(),urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        source = response.read()
        response.close()
        match=re.compile(b'<div class="list-thumb">\n        <a href="(.+?)">\n          <span style="display:block;width:122px;height:74px;"><img alt="" src="(.+?)" /></span>\n        </a>\n      </div>\n      <div class="list-details">\n        <div class="list-title">\n          <a href="(.+?)">(.+?)</a>').findall(source)
        for title,thumbnail,url,name in match:
                addLink(name,'http://www.bayyinah.tv'+url,thumbnail)
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def Notify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def LOGIN(username,password):
        uc = username[0].upper() + username[1:]
        lc = username.lower()

        logged_in = weblogin.check_if_logged_in(__datapath__)
        if logged_in == False:
            logged_in = weblogin.doLogin(__datapath__,username,password)
            
        if logged_in == True:
                cookiepath = os.path.join(__datapath__,'cookies.lwp')
                cj.load(cookiepath)
                
                Notify('Welcome back','Successfully logged into Bayyinah.tv','4000',__icon__)

                addDir('COURSES','http://www.bayyinah.tv/categories/137959',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/137959/small/4_Series.jpg?1372522400')
                addDir('RAMADAN','http://www.bayyinah.tv/categories/137658',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/137658/small/bonus.png?1372357554')
                addDir('EXTRAS','http://www.bayyinah.tv/categories/138762',1,'http://s3.amazonaws.com/kajabi-media/assets/category_images/138762/small/icon-universe.png?1372890269')
        elif logged_in == False:
                Notify('Login Failure',' could not login','4000',__icon__)

def STARTUP_ROUTINES():
        #deal with bug that happens if the datapath doesn't exist
        if not os.path.exists(__datapath__):
          os.makedirs(__datapath__)

        usrsettings = xbmcaddon.Addon(id=__addonname__)

        #get username and password and do login with them
        #also get whether to hid successful login notification
        __username__ = usrsettings.getSetting('username')
        __password__ = usrsettings.getSetting('password')

        LOGIN(__username__,__password__) 
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))

if mode==None or url==None or len(url)<1:
        print ("")
        STARTUP_ROUTINES()
        #CATEGORIES()
       
elif mode==1:
        print (""+url)
        INDEX(url)
        
elif mode==2:
        print (""+url)
        INDEX2(url)
        
elif mode==3:
        print (""+url)
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
