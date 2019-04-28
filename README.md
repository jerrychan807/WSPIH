

# WSPIH


![](https://github.com/jerrychan807/WSPIH/blob/master/img/logo.png)

网站个人敏感信息文件扫描器

---

# 介绍:

![](https://github.com/jerrychan807/WSPIH/blob/master/img/flow.png)

---

# 使用效果:

![](https://github.com/jerrychan807/WSPIH/blob/master/img/sc2.png)
![](https://github.com/jerrychan807/WSPIH/blob/master/img/sc1.png)

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





