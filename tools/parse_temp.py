# -*-coding: utf-8 -*-
path = 'C:/Users/Administrator/Desktop/MyProject/post_url_v1.0'
file = open('%s/url/cache/temp_url.txt' % path, 'r+')
result = open('%s/url/cache/result.txt' % path, 'w+')
for line in file:
    url = line.split(' ', 2)[0]
    print(url)
    result.write(url + '\n')
result.close()
file.close()