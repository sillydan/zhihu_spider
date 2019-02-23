from __future__ import print_function # 使用python3的print方法
from zhihu_oauth import ZhihuClient
import re
import os
import urllib.request

def login(username,password):
    from zhihu_oauth import ZhihuClient
    from zhihu_oauth.exception import NeedCaptchaException
    client = ZhihuClient()
    try:
        client.login(username, password)
        print(u"登陆成功!")
    except NeedCaptchaException: # 处理要验证码的情况
        # 保存验证码并提示输入，重新登录
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('please input captcha:')
        client.login(username, password, captcha)
    client.save_token('token.pkl') # 保存token
#有了token之后，下次登录就可以直接加载token文件了
# client.load_token('filename')

def crawling(id):
    #id为问题id
    client = ZhihuClient()
    # 登录
    client.load_token('token.pkl')  # 加载token文件
    question = client.question(id)
    print(u"问题:",question.title)
    print(u"回答数量:",question.answer_count)
    if not os.path.exists(question.title):
        os.mkdir(question.title)
    path = question.title
    index = 1 # 图片序号
    for i,answer in enumerate(question.answers):
        content = answer.content  # 回答内容
        anther=answer.author.name
        re_compile = re.compile(r'<img src="(https://pic\d\.zhimg\.com/.*?\.(jpg|png))".*?>')
        img_lists = re.findall(re_compile, content)
        if (img_lists):
            for img in img_lists:
                img_url = img[0]  # 图片url
                image_name=anther+'_'+str(index)+'.jpg'
                if not os.path.exists(path + '/'+ image_name):
                    urllib.request.urlretrieve(img_url, path + '/'+ image_name)
                    print(u"成功保存第%d张图片:%s,当前总进度%.2f%%" % (index,image_name,i/question.answer_count*100))
                index += 1
        print('第%d个答案爬取完成,当前总进度%.2f%%' % (i,i/question.answer_count*100))

login('cjp940502@qq.com','94c05j02p')
crawling(297715922)
#有一副令人羡慕的好身材是怎样的体验？ https://www.zhihu.com/question/297715922/answer/546342151