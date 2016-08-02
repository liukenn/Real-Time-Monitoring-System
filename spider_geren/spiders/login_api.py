# _*_coding: utf-8 _*_
try:
    import os
    import sys
    import urllib
    import urllib2
    import cookielib
    import base64
    import re
    import hashlib
    import json
    import rsa
    import binascii
except ImportError:
    print >> sys.stderr, "%s" % (sys.exc_info(), )
    sys.exit(1)


def get_su(user_name):
    username_ = urllib.quote(user_name)  # html字符转义
    username = base64.encodestring(username_)[:-1]
    return username


def get_sp_rsa(passwd, servertime, nonce):
    # 这个值可以在prelogin得到,因为是固定值,所以写死在这里
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    weibo_rsa_e = 65537  # 10001对应的10进制
    message = str(servertime) + '\t' + str(nonce) + '\n' + passwd
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    encropy_pwd = rsa.encrypt(message, key)
    return binascii.b2a_hex(encropy_pwd)


def get_prelogin_status(user_name):
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' \
                   + get_su(user_name) + \
                   '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)'
    data = urllib2.urlopen(prelogin_url).read()
    print 'step1: Load prelogin url'
    p = re.compile('\((.*)\)')

    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = data['rsakv']
        return servertime, nonce, rsakv
    except:
        print 'Getting prelogin status met error!'
        return None


def do_login(user_name, passwd, cookie_file):
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': '',     
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    cookie_jar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener2 = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
        servertime, nonce, rsakv = get_prelogin_status(user_name)
    except:
        return
    login_data['su'] = get_su(user_name)
    login_data['sp'] = get_sp_rsa(passwd, servertime, nonce)
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['rsakv'] = rsakv
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req = urllib2.Request(login_url, data=login_data, headers=http_headers)
    response = urllib2.urlopen(req)
    text = response.read()
    print 'step2: Signin with post_data'
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    try:
        login_url2 = p.search(text).group(1)  # http://passport.weibo.com/wbsso/login/.../
        data = urllib2.urlopen(login_url2).read()
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar.save(cookie_file, ignore_discard=True, ignore_expires=True)
            print 'step3: Save cookies after login succeeded'
            #添加手机端m.weibo.cn的验证cookie
            SUB_data = open(cookie_file,'rb').read( )
            SUB_num = re.findall('SUB="(.+?)";',SUB_data)
            SUB = 'Set-Cookie3: SUB="'+ str(SUB_num[0]) +'"; path="/"; domain="m.weibo.cn"; path_spec; domain_dot; discard; httponly=None; version=0'
            f = open(cookie_file,'a+')
            f.writelines(SUB)
            #
            return 1
        else:
            return 0
    except:
        return 0


def get_login_cookie(url):
    import settings

    cookie_file = settings.COOKIE_FILE
    if not os.path.exists(cookie_file):
        user_name = settings.USER_NAME
        passwd = settings.PASSWORD
        do_login(user_name, passwd, cookie_file)

    try:
        cookie_jar = cookielib.LWPCookieJar(cookie_file)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        print 'Load cookie succeeded'
    except cookielib.LoadError:
        return None
    else:
        cookie_d = {}
        for cookie in cookie_jar:
            domain = cookie.domain
            if url.find(domain) > 0:
                cookie_d[cookie.name] = cookie.value
        return cookie_d


def load_cookie(cookie_file):
    try:
        cookie_jar = cookielib.LWPCookieJar(cookie_file)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        print 'Load cookie succeeded'
        return 1
    except cookielib.LoadError:
        return 0


def login(user_name, passwd, cookie_file):
    if os.path.exists(cookie_file) and load_cookie(cookie_file):
        return 1
    else:
        return do_login(user_name, passwd, cookie_file)


def test_with_mayun():
    test_url = 'http://weibo.com/mayun'
    response = urllib2.urlopen(test_url).read()
    print response
    p = re.compile(r'\$CONFIG\[\'uid\'\]')
    # print re.search(p, response)
    if not p.search(response):
        print 'Please Login'
    else:
        print 'Already Login'


if __name__ == '__main__':
    import settings
    test_with_mayun()
    print settings.USER_NAME,settings.PASSWORD
    if login(settings.USER_NAME, settings.PASSWORD, settings.COOKIE_FILE):
        print 'Login Weibo succeeded'
        # test_with_mayun()
    else:
        print 'Login Weibo failed'