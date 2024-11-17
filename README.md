# Konachan 下载器
[![safe049 - KonaDown](https://img.shields.io/static/v1?label=safe049&message=KonaDown&color=blue&logo=github)](https://github.com/safe049/KonaDown "Go to GitHub repo")
[![stars - KonaDown](https://img.shields.io/github/stars/safe049/KonaDown?style=social)](https://github.com/safe049/KonaDown)
[![forks - KonaDown](https://img.shields.io/github/forks/safe049/KonaDown?style=social)](https://github.com/safe049/KonaDown)

[![GitHub release](https://img.shields.io/github/release/safe049/KonaDown?include_prereleases=&sort=semver&color=blue)](https://github.com/safe049/KonaDown/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![issues - KonaDown](https://img.shields.io/github/issues/safe049/KonaDown)](https://github.com/safe049/KonaDown/issues)
欢迎使用 Konachan 下载器！这是一个基于 Python 的应用程序，允许用户通过指定标签搜索和下载壁纸。该应用程序使用 cloudscraper 库与 Konachan API 进行交互，并使用 Flet 库创建用户界面。

## 功能

- 搜索壁纸：用户可以根据输入的标签搜索壁纸。
- 分页浏览：支持分页显示搜索结果，每页显示 5 张壁纸。
- 下载功能：可以下载选中的壁纸。
- 下载控制：支持暂停、继续和取消下载操作。

## 依赖项

为了运行该应用程序，请确保安装了以下Python库：
```bash
 pip install cloudscraper flet
```
## 使用方法

1. 克隆或下载此项目到本地。
2. 在终端中导航到项目目录。
3. 运行以下命令安装应用程序：
```bash
 ./install.sh
```
4. 运行以下命令启动应用程序：
```bash
 KonaDown
 ```
4. 在出现的界面中，输入您想搜索的标签，并点击“搜索”按钮。
5. 通过“上一页”和“下一页”按钮浏览结果。
6. 选择您喜欢的壁纸，点击“下载图片”按钮进行下载。
7. 使用“暂停下载”、“继续下载”和“取消下载”按钮来控制下载进度。

## 贡献

欢迎任何贡献！如有建议或问题，请提交 Issue 或 Pull Request。

## 许可证

本项目采用 MIT 许可证，详细信息请参阅 LICENSE 文件。
