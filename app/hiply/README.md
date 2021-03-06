
## 緣起

* [#5 回覆: [教學] 製作 HiChannel Radio 網頁應用程式](https://www.ubuntu-tw.org/modules/newbb/viewtopic.php?post_id=357580#forumpost357580)


## 前置作業

可以參考「[這一頁](https://lazka.github.io/pgi-docs/index.html#Gtk-3.0)」，執行下面指令，安裝「[gir1.2-gtk-3.0](https://packages.ubuntu.com/xenial/gir1.2-gtk-3.0)」。

``` sh
$ sudo apt-get install gir1.2-gtk-3.0
```

可以參考「[這一頁](https://lazka.github.io/pgi-docs/index.html#Keybinder-3.0)」，執行下面指令，安裝「[gir1.2-keybinder-3.0](https://packages.ubuntu.com/xenial/gir1.2-keybinder-3.0)」。

``` sh
$ sudo apt-get install gir1.2-keybinder-3.0
```


可以參考「[這一頁](https://lazka.github.io/pgi-docs/index.html#AppIndicator3-0.1)」，執行下面指令，安裝「[ gir1.2-appindicator3-0.1](https://packages.ubuntu.com/xenial/gir1.2-appindicator3-0.1)」。

``` sh
$ sudo apt-get install gir1.2-appindicator3-0.1
```


可以參考「[這一頁](https://lazka.github.io/pgi-docs/index.html#AppIndicator3-0.1)」，執行下面指令，安裝「[gir1.2-webkit2-4.0](https://packages.ubuntu.com/xenial/gir1.2-webkit2-4.0)」。

``` sh
$ sudo apt-get install gir1.2-webkit2-4.0
```

以上合併成一個指令

``` sh
$ sudo apt-get install gir1.2-gtk-3.0 gir1.2-keybinder-3.0 gir1.2-appindicator3-0.1 gir1.2-webkit2-4.0
```


## 下載安裝

執行下面指令，下載安裝

``` sh
mkdir -p ~/bin
cd ~/bin
wget -c https://raw.githubusercontent.com/samwhelp/util-prototype/master/app/hiply/hiply.py -O hiply
chmod u+x hiply
```


## 執行啟動

執行下面指令，啟動

``` sh
$ hiply
```


## 相關專案

* [yuply](https://github.com/samwhelp/util-prototype/tree/master/app/yuply)
* [util-chewup](https://github.com/samwhelp/util-chewup/tree/master/app/usr/lib/chewup/chewup)
