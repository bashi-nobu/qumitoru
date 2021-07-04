<template>
  <div class="howtoFrame">
    <v-card>
      <v-card-title class="howtoFrame__title">
        このアプリの使い方
      </v-card-title>
    </v-card>
    <v-card class="howtoFrame__topicList">
      <ul>
        <li><a href="#topic1">アンケートの集計方法</a></li>
        <li><a href="#topic2">集計データの確認・編集方法</a></li>
      </ul>
    </v-card>
    <v-card>
      <v-card-title class="howtoFrame__title topic-title" id="topic1">
        1. アンケートの集計方法
      </v-card-title>
      <div class="howtoFrame__describe">
        <div class="howtoFrame__describe__title">
          ① サイドメニューの「
          <span class="strong-text">アンケートを読み取る</span>
          」をクリックします
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img1.png">
        </div>
        <div class="howtoFrame__describe__title">
          ② 画面中央の
          <v-icon>mdi-camera-plus-outline</v-icon>
          をクリックしてカメラを起動させます
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img2.png">
        </div>
        <div class="howtoFrame__describe__title">
          PCの場合は
          <v-icon>mdi-camera-plus-outline</v-icon>
          をクリックすると下記のようにファイル選択ボックスが表示されるのでアップロードする画像を選択してください。
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img2-2.png">
        </div>
        <div class="howtoFrame__describe__title">
          ③ アンケート用紙を撮影します<br>
          (※ アンケート用紙は<a href="/download">こちらから</a>ダウンロードしてください)
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img3.png">
        </div>
        <div class="howtoFrame__describe__title">
          ④ 撮影したら<span class="strong-text">写真を使用</span>
          をクリックします
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img4.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑤ 数秒間 Loading画面が表示されます
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img5.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑥ 読み取りに成功すると下記のような画面が表示されます
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img6.png">
        </div>
        <div class="howtoFrame__describe__title">
           読み取りに失敗した場合は下記のような画面が表示されるので、再度撮影し直してください
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img7.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑦ ⑥の画面閉じると
          <v-icon>mdi-camera-plus-outline</v-icon>
          の下に
          <span class="strong-text">読込み済みアンケートの枚数</span>
          と
          <span class="strong-text">集計開始ボタン</span>
          が表示されます(※読込み済みのアンケートが0枚の場合は表示されません)
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img8.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑧ <span class="strong-text">集計開始ボタン</span>
          をクリックして以下の画面を表示させます
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img9.png">
        </div>
        <div class="howtoFrame__describe__title">
          日付の入力欄をクリックすると下記のようにカレンダーが表示されるので
          <span class="strong-text">アンケートの実施日</span>
          を入力します
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img10.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑨ 日付を入力したら
          <span class="strong-text">集計開始ボタン</span>
          をクリックします
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img11.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑩ 下記の画面が表示されたら、集計が開始されます。数分後には
          <span class="strong-text">集計一覧画面</span>
          から集計結果を確認することができます。
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img12.png">
        </div>
      </div>
    </v-card>
    <v-card>
      <v-card-title class="howtoFrame__title topic-title" id="topic2">
        2. 集計データの確認・編集方法
      </v-card-title>
      <div class="howtoFrame__subtitle">
        ※スマホからは利用できません。
      </div>
      <div class="howtoFrame__describe">
        <div class="howtoFrame__describe__title">
          ① サイドメニューの
          <span class="strong-text">集計一覧</span>
          をクリックします。
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img13.png">
        </div>
        <div class="howtoFrame__describe__title">
          集計済みのアンケートデータが下記のように一覧表示されます
          <span class="sub-text">(画面右上の集計期間を切り替えることで表示する集計データを切り替えるとができます)</span>
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img14.png">
        </div>
        <div class="howtoFrame__describe__title">
          ② 各アンケートデータの集計数値を編集する場合は
          <span class="strong-text">撮影画像のアイコン</span>
          をクリックします。
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img15.png">
        </div>
        <div class="howtoFrame__describe__title">
          クリックすると撮影されたアンケート用紙画像と集計値が表示されます
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img16.png">
        </div>
        <div class="howtoFrame__describe__title">
          ③
          <span class="strong-text">修正ボタン</span>
          をクリックします
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img17.png">
        </div>
        <div class="howtoFrame__describe__title">
          ④ 集計済みスコアが編集できる状態になるので、修正が必要な質問項目のスコアを変更します
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img18.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑤ <span class="strong-text">登録ボタン</span>
          をクリックします
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img19.png">
        </div>
        <div class="howtoFrame__describe__title">
          ⑥ <span class="strong-text">修正が完了しました</span>
          と表示されれば、編集が完了です
        </div>
        <div class="howtoFrame__describe__content">
          <img src="../assets/howto_imgs/howto-img20.png">
        </div>
      </div>
    </v-card>
    <div class="Page-Btn" @click="scrollTop">
      <v-icon>mdi-arrow-up</v-icon>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Howto',
  methods: {
    scrollTop: function(){
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    }
  }
}
</script>
<style lang="scss">
  @import '../assets/css/howto.scss';
</style>
