# git-commit-analytics

一个快速统计项目库里所有人git提交情况的脚本，方便你~~卷死其他同事~~将工作量保持在平均线以上（诚恳

## 使用方法

requirements.txt安装所需依赖后执行`analytics.py`，可用的命令行参数如下：

* `-h`              帮助
* `--contributors`  统计贡献者
* `--commit-lines`  统计各贡献者的累计提交行数
* `-path PATH`      git存储库的本地路径
* `-since SINCE`    开始日期，语义同git`--since`
* `-until UNTIL`    结束日期，语义同git`--until`
