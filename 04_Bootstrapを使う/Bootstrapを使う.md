# Bootstrapを使う

ここでは、Bootstrapを使用しておしゃれなブログアプリを作ってみます。

## Webアプリの基盤を作成する

### 初期設定

```startapp```コマンドでWebアプリの基盤を作成します。

```sh
$ python manage.py startapp blog
```

作成したら、```setetings.py```を編集して初期設定を行います。

まずは、作成するアプリを有効化するために、```INSTALLED_APPS```に```blog.apps.BlogConfig```を追記します。

```py
INSTALLED_APPS = [
    # PRODUCT
    'blog.apps.BlogConfig',
    # DEFAULT
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

このとき、リストに記述する順番に気をつけたほうがいいそうです。

> - INSTALLED_APPS は最初にリストされているアプリケーションのソースコードが優先される
> - INSTALLED_APPS は ローカルアプリケーション・サードパーティアプリケーション・Djangoアプリケーション という順番にしたほうがよい
>
> [DjangoのINSTALLED_APPSの順番がめちゃくちゃ重要だった話](https://jumpyoshim.hatenablog.com/entry/order-of-installed-apps-with-django-is-important)

なお、```blog.apps.BlogConfig```の実態は、自動生成された```apps.py```の中で定義されている```BlogConfig```クラスです。

```py
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

また、使用言語とタイムゾーンの初期設定は欧米のものとなっているので、日本仕様に変更します。

```py
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
```

### テンプレート

初期設定が終わったら、はじめに画面に表示するHTMLドキュメントを作成します。Djangoの世界のMTVのうち、T（Template）の要素です。ここではブログアプリを作成する予定ですが、まずは動作確認のため、以下のような簡単なファイルを作って表示してみます。

```html
<!DOCTYPE html>
<head></head>
<body>
  <h1>Top Page</h1>
</body>
```

作成したテンプレートファイルは、Webアプリのディレクトリ直下に```templates```ディレクトリを作成し、その中に保存しておきます。Webアプリのトップに表示するHTMLドキュメントとなるため、ファイル名は```index.html```とします。```templates```というディレクトリを作成した理由は、テンプレートはいくつも作成するため1つにまとめたほうが便利という点もありますが、Djangoにはビューがレンダリングする際に使用するテンプレートファイルを```templates```というディレクトリから自動で検索する機能があるからです。

### ビュー

次に、画面に表示する内容を生成するビューを作成します。Djangoの世界のMTVのうち、V（View）の要素です。Djangoのビューの作り方は、関数ベースビューとクラスベースビューの2通りあります。ここでは、メリットの多いクラスベースビューに絞って学習します。

クラスベースビューは、予め用意された様々なビルドインクラスビューから目的似合ったクラスを1つ選択し、それを継承したサブクラスを作ることで、独自のビューを定義します。ビルドインクラスビューはリファレンスにある通りです。

[https://docs.djangoproject.com/ja/3.2/ref/class-based-views/](https://docs.djangoproject.com/ja/3.2/ref/class-based-views/)

多くのビルドインクラスが実装されていることがわかりますが、よく使うクラスはいくつかに絞られます。以下に、汎用的なクラスを示します。

|クラス|用途|
|:--|:--|
|TemplateView|テンプレートを読み込んでHTMLドキュメントをレンダリングする|
|RedirectView|別のビューにリダイレクトする|
|ListView|モデルのデータを一覧表示する|
|DetailView|モデルのデータの詳細を表示する|
|CreateView|モデルのデータを作成する|
|UpdateView|モデルのデータを更新する|
|DeleteView|モデルのデータを削除する|
|FormView|フォームと連動した処理を行う|

今回はHTMLドキュメントをレンダリングするだけなので、```TemplateView```を継承した```IndexView```を作成してみます。```blog```ディレクトリの中の```veiws.py```を開くとインポート文しか記述されていないはずなので、その下に```IndexView```クラスを実装していきます。

```py
from django.shortcuts import render
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    
    template_name = 'index.html'
```

```template_name```は```TemaplateView```クラスのクラス変数であり、描画するテンプレートファイルを指定するものです。今回は```index.html```を描画したいので、この変数をオーバーライドしておきます。先程説明したとおり、Djangoは```temapltes```ディレクトリの中から自動的に検索するため、```templates/index.html```とする必要はありません。

### ルーティング

次に、ルーティングの設定を行います。今回は、[http://127.0.0.1:8000](http://127.0.0.1:8000)にアクセスしたらブログアプリに直接アクセスできるようなルーティングを設定します。

ルーティング（URLconf）は、プロジェクトの```urls.py```に設定する内容ですが、一つのプロジェクトに多数のWebアプリを開発すると、その量は膨大になります。そこで、各Webアプリのディレクトリにも```urls.py```を作り、その中でルーティングを管理したほうが便利です。こうすると、プロジェクトの```urls.py```には、各Webアプリの```urls.py```を参照すること！という1行をWebアプリごとに記述するだけで済みます。

まずはブログアプリのルーティングから設定します。```blog/urls.py```というファイルを新規作成し、以下のように設定します。プロジェクトの```urls.py```をコピーして編集したほうが、インポート文を書く手間が少し減ります。

```py
from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]
```

同じディレクトリにあるviews.pyをインポートし、```views.IndexView```が継承しているクラスの```as_view```関数を呼び出します。

一方、プロジェクトのルーティングには作成した```blog/urls.py```を参照したいので、以下のように設定します。

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'))
]
```

```include```は引数のURLconfにリダイレクトさせる関数です。これで、ブログアプリへのルーティングが完成しました。

### 動作確認

開発サーバを起動して、[http://127.0.0.1:8000/](http://127.0.0.1:8000/)に接続してみます。Top Pageと表示されるだけの簡素なページが表示されることが確認できたと思います。これで、ルーティング→ビュー→テンプレートの一連の流れができることが確認できました。

## Bootstrapを使用する

ここからは、先程作成したTop Pageと表示されるだけのページをブログのような見た目にしていきます。あくまでも見た目だけの話で、データベース連携などは次章以降に実施します。

ここでは、[Start Bootstrap](https://startbootstrap.com/)のサイトから、[Clean Blog](https://startbootstrap.com/theme/clean-blog)というテンプレートをダウンロードして使っていこうと思います。サイトから「Free Download」をクリックしてZIPファイルをダウンロードしてください。

ダウンロードしたZIPファイルを展開すると、次のようなディレクトリ構成となっていると思います。

```sh
startbootstrap-clean-blog-gh-pages
│  about.html
│  contact.html
│  index.html
│  post.html
│
├─assets
│  │  favicon.ico
│  │
│  └─img
│          about-bg.jpg
│          contact-bg.jpg
│          home-bg.jpg
│          post-bg.jpg
│          post-sample-image.jpg
│
├─css
│      styles.css
│
└─js
        scripts.js
```

まずは、、先程作成したTop Pageを表示するだけのhtmlドキュメントを、Bootstrapの```index.html```で上書きしてください。開発サーバを起動すると、htmlの内容が更新されていることがわかりますが、まだCSSやJavaScript、画像などを適用していないため、テキストだけの簡素なページとなっていると思います。

次に、```sset```、```css```、```js```ディレクトリをBlogアプリのディレクトリにコピーします。これらのファイルは静的ファイルと呼ばれており、Djangoでは静的ファイルを```static```ディレクトリに配置する決まりとなっています。正確には、プロジェクトの```settings.py```の以下で設定されているディレクトリに配置することになります。

```py
STATIC_URL = '/static/'
```

```blog/static/```ディレクトリを作成し、その中に先程の3つのディレクトリをコピーすれば、静的ファイルの配置は完了です。

最後に、Djangoが静的ファイルを参照できるような仕組みを実装します。Djangoではテンプレートを使って動的なHTMLドキュメントを生成するための仕組みとしてテンプレートタグがあります。テンプレートタグは、

```html
{%    %}
```
のように、波括弧と%で囲った範囲で記述することができます。テンプレートタグでstaticディレクトリをロードするためには、まずテンプレートタグ```load```で```static```タグをロードします。これを```index.html```の先頭に記述してください。

```html
{% load static %}
```

次に、```static```タグを使用して、<link>タグなどで静的ファイルを参照するURLを動的生成します。具体的には、次の部分になります。

```html
9行目       <link rel="icon" type="image/x-icon" href={% static 'assets/favicon.ico' %} />
16行目      <link href={% static 'css/styles.css' %} rel="stylesheet" />
38行目      <header class="masthead" style="background-image: url({% static 'assets/img/home-bg.jpg' %})">
151行目     <script src="{% static 'js/scripts.js' %}"></script>
```

上から順番に、ファビコンの画像、CSSファイル、背景画像ファイル、JavaScriptのURLが動的に生成されるようになります。

最後に、画面上部にトップページへ遷移するリンク「Start Bootstrap」「HOME」があるので、遷移先のURL（http://127.0.0.1:8000）を自動生成します。URLを生成するためには```url```タグを使用します。

```html
22行目      <a class="navbar-brand" href={% url 'blog:index' %}>Start Bootstrap</a>
29行目      <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href={% url 'blog:index' %}>Home</a></li>
```

ここで、```{% url 'blog:index'}```のうち```blog```は```blog/urls.py```で指定した```app_name```を、```index```は同じく```blog/urls.py```の```path('', views.IndexView.as_view(), name='index')```の```name```属性で指定した値です。このように```app_name```や```name```を設定しておくと、URLが逆引きできるため便利です。

index.html全体は以下になります。正しく設定できていれば、[Start Bootstrap](https://startbootstrap.com/theme/clean-blog)のサンプルにあるようなページが表示されるはずです。

[index.html](https://github.com/JuvenileTalk9/Django/blob/main/sampleproject/blog/templates/index.html)

[目次へ戻る](https://github.com/JuvenileTalk9/Django)
