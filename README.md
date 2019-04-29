

# WSPIH


![](https://github.com/jerrychan807/WSPIH/blob/master/img/logo.png)

网站个人敏感信息文件扫描器

---

# 介绍:

![](https://github.com/jerrychan807/WSPIH/blob/master/img/flow.png)

[开发记录](https://jerrychan807.github.io/2019/04/25/WPSIH-%E7%BD%91%E7%AB%99%E4%B8%AA%E4%BA%BA%E6%95%8F%E6%84%9F%E4%BF%A1%E6%81%AF%E6%96%87%E4%BB%B6%E6%89%AB%E6%8F%8F%E5%99%A8-%E5%BC%80%E5%8F%91%E8%AE%B0%E5%BD%95/)

---

# 使用效果:

![](https://github.com/jerrychan807/WSPIH/blob/master/img/sc2.png)
![](https://github.com/jerrychan807/WSPIH/blob/master/img/sc1.png)

---

# 数据统计:

![](https://github.com/jerrychan807/WSPIH/blob/1e06930910ec3cd615c5762840d0b7d71c6133cf/img/data1.png)

![](https://github.com/jerrychan807/WSPIH/blob/1e06930910ec3cd615c5762840d0b7d71c6133cf/img/data2.png)

---

# 使用步骤:

## 初始化:

```bash
# 下载
git clone https://github.com/jerrychan807/WSPIH.git

# 进入项目目录
cd WSPIH

# 安装依赖模块
pip3 install -r requirements.txt

# 修改配置文件(若不修改,则使用默认配置)
vi config.py
```

## 开始扫描:

```bash
# 使用
python3 SensitivesHunter.py 目标文件 结果文件夹

# 示例
python3 SensitivesHunter.py targets/http-src-1-100.txt src
```


## 查看结果:

如果有扫出敏感文件...

### 单个结果:

- 每个目标的结果会保存在 结果文件夹/对应域名 下.
- 会保留有问题的敏感文件
- 文件链接`file_links.json`、敏感结果`result.json`


### 汇总结果:

```bash
# 输出最终汇总的结果
python3 CombineResult.py 结果文件夹

# 示例
python3 CombineResult.py src
```

- 查看最终合并的结果:`all_result.txt `

---

# Ps:

- 本项目仅供学习,交流使用.勿用于非法用途。
- 如果目标是学校网站,麻烦把漏洞提交到[教育行业漏洞报告平台](https://src.edu-info.edu.cn),谢谢.


---

# Contributors:

- JackChan1024





