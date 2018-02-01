# muhe_bot

muhe's tg bot


#### 1. 配置文件

在项目当前目录下，文件名`conf.json`，只有token的配置，格式如下：

```json
{"Token":your_tg_bot_token}
```


#### 2. 支持的命令

/vendors : get all vendors.

/search [vendor] : get vendor's all product.

/search [vendor] [product] [count] : get all cve's about product of vendor.

/cves : get lastest cves.

/cve [cve-xxxx-xxxx] : get info of cve-xxxx-xxxx.


#### TODO
```
/sentry start : Begin early waring

/sentry stop  : Stop early waring
```


