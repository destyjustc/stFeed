import yagmail #https://github.com/kootenpv/yagmail#start-a-connection

yag = yagmail.SMTP('edmondsbasketball@gmail.com', 'YangYong0911')
#yag.send('michaelzhang917@gmail.com', 'test', 'test')
contents = ['Body text, and here is an embedded image:', 'http://www.sina.com.cn',
            'You can also find an audio file attached.', '/Users/yzhang/Desktop/test.PNG']
yag.send('michaelzhang917@gmail.com', contents = contents)