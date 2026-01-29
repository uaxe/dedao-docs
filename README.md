## 得到听书文档

## clone问题
`error: invalid path 'docs/历史/《<山海经>的世界》- 裴鹏程解读.md'`
进入该目录：cd D:\GitHub\dedao-docs  

开启转义支持并强制恢复：
``` bash
git config core.protectNTFS false
git checkout -f HEAD
```

得到听书 markdown 文档

----

###  markdown 在线文档

 * [github](https://uaxe.github.io/dedao-docs/)
 * [netlify](https://dedao.netlify.app/)

### 本地部署

#### docker方式
```shell
docker run -d -p 8092:8092 --restart always  --name dedao-docs  zkep/dedao-docs
```
浏览器访问：<http://127.0.0.1:8092/>


#### 源码方式
```shell
git clone https://github.com/uaxe/dedao-docs.git  --depth 1

pip install mkdocs-material

cd dedao-docs

mkdocs serve
```

浏览器访问：<http://127.0.0.1:8000/>
