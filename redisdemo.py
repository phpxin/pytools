# -*- coding: utf-8 -*-
import redis

redisdb = redis.Redis('SpiderDb')

# 集合操作

# 添加
redisdb.delete('urls')

redisdb.sadd('urls', 'localhost')
redisdb.sadd('urls', 'lalalala')

# 获取所有成员，返回一个集合
test = redisdb.smembers('urls')

print test  # set(['lalalala', 'localhost'])

# 测试是否为该集合成员
is_member = redisdb.sismember('urls', 'localhost')

if is_member :
    print 'is member'
else:
    print 'not member'