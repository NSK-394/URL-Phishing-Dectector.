import re
from urllib.parse import urlparse
import ipaddress

shorteners = ("bit.ly", "t.co", "tinyurl.com", "goo.gl", "ow.ly", "buff.ly", "is.gd", "tiny.cc")

weights={
    "ip_in_host": 30,
    "at_symbol": 25,
    "long_url": 10,
    "many_dashes": 10,
    "multiple_double_slash": 10,
    "shortener": 20,
    "punycode": 20,
    "no_https": 5,
}

def normalize_url(url):
    if not re.match(r'^^[a-zA-Z]+://', url):
        url="http://"+url
    parsed = urlparse(url)
    host=parsed.netloc
    if '@'in host:
        host=host.split('@')[-1]
        
    host=host.split(':')[0]
    return url,parsed,host
def is_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False
def detech_phishing(url):
    url,parsed,host=normalize_url(url)
    flage=[]
    score=0
    
    if is_ip(host):
        flage.append("Uses RAW IP address in URL")
        score+=weights["ip_in_host"]
        
    if '@' in url:
        flage.append("Contains '@' symbol")
        score+=weights["at_symbol"]
    if len(url)>75:
        flage.append("URL is too long")
        score+=weights["long_url"]
    if url.count('-')>5:
        flage.append("Contains many '-' in URL")
        score+=weights["many_dashes"]
    if url.count('//')>2:
        flage.append("Contains multiple '//' in URL")
        score+=weights["multiple_double_slash"]
    if host in shorteners:
        flage.append("Uses URL shortener")
        score+=weights["shortener"] 
    if 'xn--' in host:
        flage.append("Uses punycode in URL")
        score+=weights["punycode"]  
    if parsed.scheme!='https':
        flage.append("Doesn't use HTTPS")
        score+=weights["no_https"]  
        
    if score>=50:
        verdit="High Risk"
    if 20<=score<50:
        verdit="Medium Risk"
    if score<20:
        verdit="Low Risk"
           
    return {
        "url": url,
        "host": host,
        "score": score,
        "flags": flage,
        "verdict": verdit
    }
if __name__=="__main__":
    url=input("Enter URL: ")
    result=detech_phishing(url)
    print("\nURL:",result["url"])
    print("Host:",result["host"])
    print("Score:",result["score"])
    print("Verdict:",result["verdict"])
    print("Flags:")
    for flag in result["flags"]:
        print("-",flag)

    
    