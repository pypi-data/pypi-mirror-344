# anbefm

一个后台框架

- [x] manage 应用管理
- [x] handle_payload 解析请求body
- [x] jwt 保存登录信息
- [x] model 数据库连接
- [x] 请求数据校验
- [x] 排序

## 启动应用

```
python -m anbefm.manage startapp --port=9201 --app=client
```

# 如何发布python到pypi

可以参考这篇[教程](https://juejin.cn/post/6844903950550827022)

主要步骤：
- setup.py 中修改版本号
- 生成包
  - pip install --upgrade setuptools wheel twine
  - python setup.py sdist bdist_wheel
- 上传包到 PyPI
  - 注册pypi账号
  - python -m twine upload dist/*

## 如何调试python包

npm 中的`npm link`命令可以很方便的将当前项目链接到全局安装目录，python中也有类似的命令

```bash
# 将当前包安装到全局， 可以指定包所在的文件夹（setup.py所在的文件夹）
pip install -e . 

# 或
python setup.py develop
```
