# android-auto-helper
基于Python3开发的、开源的、跨平台的安卓自动化脚本开发工具
# 项目应用
- [安卓脚本应用开发脚手架]()
- [安卓截图图色助手]()
- [介绍及应用教学视频]()
# 项目优缺点
## 优点
- 面向对象：每一个安卓设备都可以初始化为一个设备对象进行操作
- 跨平台：支持windows/mac/linux，只需选择对应系统的adb初始化，不需要修改源码
- 自动兼容设备分辨率：对于不同分辨率的设备，可以自动进行兼容，无需修改坐标数据
## 缺点
- 本项目在Mac平台开发，Windows/Linux平台暂未测试
- 由于adb调试桥的事件操作命令最高只支持到安卓7.0（api24），如果安卓系统版本过高，可能得不到预期的效果
# 开发环境
- 操作系统：mac系统（M1 Pro）
- Python：python 3.9
- 安卓设备：安卓模拟器（Android Studio Virtual Device）
- 安卓系统：Android 7.0 (api24、arm64)
# 项目依赖
可以通过命令`pip install -r requirements.txt`来安装以下依赖
- easyocr==1.6.2
- imutils==0.5.4
- numpy==1.23.3
- opencv_python_headless==4.5.4.60
- Pillow==9.2.0
# 跨平台实现
**本项目与安卓设备的交互主要通过adb实现，只需要在初始化安卓对象时选择对应系统的adb文件即可**
adb文件存在目录`tools/platform-tools-*`下，也可以自行到官网下载->[传送门](https://developer.android.com/studio/command-line/adb)
- platform-tools-linux
- platform-tools-mac
- platform-tools-windows

**如果使用的是第三方的安卓模拟器，建议复制其模拟器源文件目录下的adb文件来调用**