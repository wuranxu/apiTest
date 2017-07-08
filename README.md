基本组成

该产品分为前端后台部分，采用了web的形式进行操作，用户可以通过浏览器来完成相应的操作，如执行用例等。

 

编程语言及框架

  前端语言包含: html, css, javascript，框架为bootstrap。

后端语言为Python  主体框架为flask。

 

使用说明
1.  配置本地mongo数据库存放测试用例，我本地端口号都在config里边
默认配置如下：

![image.png](http://upload-images.jianshu.io/upload_images/6053915-2931cbaf2480c6ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

mongo 库和collection如下：

![image.png](http://upload-images.jianshu.io/upload_images/6053915-b12b21653dbb9173.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



2. 配置本地Mysql存放注册用户信息（目前密码明文）


![image.png](http://upload-images.jianshu.io/upload_images/6053915-16a1cc17436aedd6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 修改本地config的root目录，与你的代码存放地点保持一致

![image.png](http://upload-images.jianshu.io/upload_images/6053915-ecd230ff9d3e4e95.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. 安装所需要的库如flask-sqlalchemy

5. 启动run.py运行web应用


![image.png](http://upload-images.jianshu.io/upload_images/6053915-a9ed636010572ad9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6. 打开浏览器输入地址:localhost:9000访问页面


![image.png](http://upload-images.jianshu.io/upload_images/6053915-fd4a28570283ab4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7. 注册并登陆

登陆后excel平台页面

![image.png](http://upload-images.jianshu.io/upload_images/6053915-b57ff2d2f8831a39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可视化页面


![image.png](http://upload-images.jianshu.io/upload_images/6053915-8ba67d4fdfad39d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

新增/编辑用例


![image.png](http://upload-images.jianshu.io/upload_images/6053915-7e6d42ef0a535936.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行用例

![image.png](http://upload-images.jianshu.io/upload_images/6053915-30e68404012f93fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看用例结果


![image.png](http://upload-images.jianshu.io/upload_images/6053915-191c7afae6c46686.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


查看用例详情

![image.png](http://upload-images.jianshu.io/upload_images/6053915-82997e12986ae8d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

展开（有些异常情况还有些bug待修复）

![image.png](http://upload-images.jianshu.io/upload_images/6053915-37ef6e2b2e4edf5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


大体上就这样吧， 欢迎提出整改意见！



