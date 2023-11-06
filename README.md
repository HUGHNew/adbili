# adbili

adb copier for bilibili songs/audios

TODO:
- [ ] dist/package
- [ ] use case

## usage

```bash
python3 main.py --app com.bilibili.app.in # 只处理 Play 版本的下载内容
```

## introduction

appId:
- tv.danmaku.bili : 国内版本
- com.bilibili.app.in : Play Version

根路径: `/Android/data/`

目录结构

App
- cache
- download
  - <avid>
    - <cid>
      - <video_quality>
        - audio.m4s
        - index.json
        - video.m4s
      - danmaku.xml
      - entry.json
- files

> 版本不同 entry.json 里面的字段有差异

已测试版本
- tv.danmaku.bili : 6.40.0
- com.bilibili.app.in : 3.16.0
已测试系统
- MIUI 14.0.\*
