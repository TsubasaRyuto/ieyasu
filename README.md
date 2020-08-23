# Ieyasukun
## 概要
`ieyasu`を自動登録できるツールです。

月末に基本時間で登録する方は、このツールを利用することで簡単に登録することができるようになります。

## 環境
```
mac os
python 3.8
```

## 使い方
基本的にターミナル上での実行となります。

### chrome driverのインストール
```
brew tap homebrew/cask
brew cask install chromedriver
```

### moduleのインストール
* リポジトリーはclone済みとする
* ディレクトリは移動済みとする
```
pipenv install 
```

### config/settingsのコピー
```
cp config/settings.py.sample config/settings.py
```
### settingsの修正
```
login_id →　自分のieyasuのuser id
login_pass →　自分のieyasuのpassword
only_9_oclock →　False （開発チームは基本False）
> 「全て9時出社、18時退社」としたい場合Trueに変更
```

### 実行
shellの起動
```
pipenv shell
```

プログラム実行
```
python execution.py
```

処理が終了したらshellから抜ける
```
exit
```

