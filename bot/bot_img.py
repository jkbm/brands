#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from googleapiclient.discovery import build


def main(search):

  service = build("customsearch", "v1",
            developerKey="AIzaSyAFAddCugF69HZId4VzoOhT30s0IXxw7DM")

  req = service.cse().list(
      q=search,
      cx='004821443887511405250:lxd7lxcf_ow',
      searchType = 'image',
    )
  res = req.execute()

  first = res['items'][0]

  return first


if __name__ == '__main__':
  search = "CHICKEN"
  f = main(search)
  print f['title']