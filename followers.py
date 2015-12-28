import requests
import json

orgUser = {}
clientID = "092a70548af705e5aba0"
clientSecret = "ff70fa89e4e7740d097d6ba14420d5ee875259e9"
reqURL = "?client_id="+clientID+"&client_secret="+clientSecret

Orgs = {}

def clusterOrg(user):
  queue = [user]
  location = ""
  usersDone = []
  while queue:
      user = queue.pop(0)
      req = requests.get("https://api.github.com/users/"+user+reqURL)
      user = req.json()
      print user["location"], location

      if user["company"] not in Orgs:
          Orgs[user["company"]] = []
      if user["login"] not in Orgs[user["company"]]:
          Orgs[user["company"]].append(user["login"])
      if user["location"] in Orgs:
          if user["login"] not in Orgs[user["location"]]:
              Orgs[user["location"]].append(user["login"])
      r = requests.get(user["followers_url"]+reqURL)
      print user["followers_url"]+reqURL
      r = r.json()
      target = open('orgs.txt', 'w')
      target.write(str(Orgs))
      print Orgs
      for follower in r:#user["followers"]:
        # print follower
        if follower["login"] not in usersDone:
          usersDone.append(follower["login"])
          # checkFollowers(follower["login"],org,location)
          queue.append(follower["login"])


def checkFollowers(user,org, location):
  queue = [user,'arkokoley']
  usersDone = []
  while queue:
      user = queue.pop(0)
      req = requests.get("https://api.github.com/users/"+user+reqURL)
      user = req.json()
      print user["location"], location

      if user["location"]: 
          sa = set(location.replace(',','').split())
          sb = set(user["location"].replace(',','').split())
          s = sa.intersection(sb)
          if not s:
              continue
          else:
              location = ' '.join(sa.union(sb))
          if(user["location"] == org):
            orgUser[user["login"]] = True;

      if(user["company"] == org):
        orgUser[user["login"]] = True;
      r = requests.get(user["followers_url"]+reqURL)
      print user["followers_url"]+reqURL
      r = r.json()
      target = open('users.txt', 'w')
      target.write(str(orgUser))
      print orgUser
      for follower in r:#user["followers"]:
        # print follower
        if follower["login"] not in usersDone:
          usersDone.append(follower["login"])
          # checkFollowers(follower["login"],org,location)
          queue.append(follower["login"])

# usersDone.append("suprgyabhushan")
# checkFollowers("suprgyabhushan","IIIT Bangalore","Bangalore, India")
clusterOrg('suprgyabhushan')

print orgUser
