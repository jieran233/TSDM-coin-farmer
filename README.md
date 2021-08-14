# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工


## 结构
- `credentials.py`: 存储账户密码信息, **请不要上传**
- `farmer.py`: 主程序
- `actions.py`: 签到/打工相关函数
- `cookie.py`: cookie相关函数

credentials.py的结构: 用一个变量存储账户密码
```python
TSDM_credentials = [ ['user1', 'pswd1'],
                     ['user2', 'pswd2']
                    ]
```


## 使用

1. 在`src`文件夹新建`credentials.py`, 按照上面的格式填好需要的账号密码
2. 运行`cookies.py`中`get_multiple_cookie()`获取cookie
3. 运行`work_multiple()`进行手动签到, 或者运行`farmer.py`定时任务

