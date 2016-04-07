#coding=utf8
__author__ = 'DixonShen'

import random
import base64
from settings import USER_AGENTS

class RandomUserAgent(object):
  """Randomly rotate user agents based on a list of predefined ones"""
  def __init__(self, agents):
    self.agents = agents
  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings.getlist('USER_AGENTS'))
  def process_request(self, request, spider):
    #print "**************************" + random.choice(self.agents)
    request.headers.setdefault('User-Agent', random.choice(self.agents))