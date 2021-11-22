# vn.py框架的天勤TQSDK数据服务接口-用于实盘获取初始化历史数据

## 说明

TqSdk中最多可以获取每个K线序列的最后8000根K线，无论哪个周期。即，如果提取小时线，最多可以提取最后8000根小时线，如果提取分钟线，最多可以提取最后8000根分钟线.足以用于vnpy实盘初始化策略了。

基于天勤TQSDK模块的2.8.6版本开发，支持以下中国金融市场的K线数据：

* 期货：
  * CFFEX：中国金融期货交易所
  * SHFE：上海期货交易所
  * DCE：大连商品交易所
  * CZCE：郑州商品交易所
  * INE：上海国际能源交易中心
* 股票：
  * SSE：上海证券交易所
  * SZSE：深圳证券交易所

注意：需要注册天勤账号，可以通过[该页面](https://www.shinnytech.com)。


## 安装

安装需要基于2.6.0版本以上的[VN Studio](https://www.vnpy.com)。

在vnpy_tqsdk_free目录下，在cmd中运行：

```
python setup.py install
```

## 使用

在vn.py中使用天勤TQSDK时，需要在全局配置中填写以下字段信息：

|名称|含义|必填|举例|
|---------|----|---|---|
|datafeed.name|名称|是|tqsdk_free|
|datafeed.username|用户名|是|test|
|datafeed.password|密码|是|12345678|
