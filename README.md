# Command-line-trojan
Command line trojan
- 这是一个 类似反向代理的程序，已经过部分检测，3/70 的被检测的概率，因为这个的逻辑十分的简单，都是正常操作，把文本传到客户端，然后客户端本地执行传过来的命令，所以说被检测到的比较少。
![image.png](https://bytegeek.icu/static/img/11b5a694baa2bd1a0d6626af0df4206e.image.webp)
- server端用法：python3 main.py server 
- 客户端用法：直接编辑好端口打包成exe进行运行

- 拥有截图功能

![image.png](https://bytegeek.icu/static/img/a019bbcd25a2d1a4b43d1108543b4e11.image.webp)
命令在连接后有提示，可以屏幕截图和调用摄像头


![received_screenshot.jpg](https://bytegeek.icu/static/img/b4cca4ad33ea340e2e4f7daf48e45b63.received_screenshot.webp)

![1bafdea80207047e4951ab1dfbfd347.png](https://bytegeek.icu/static/img/355db9511d0d3b5cbdfb208e8ccf93ab.1bafdea80207047e4951ab1dfbfd347.webp)
