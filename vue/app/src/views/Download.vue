<template>
  <v-container>
    <v-card class="downloadFrame">
      <v-card-title>
        下記のボタンをクリックして
        <br/>
        アンケート用紙をダウンロードしてください。
      </v-card-title>
      <v-card-text>
        <v-btn href="/pdf/questionare.pdf" class="x-small post-link align-center py-1 px-2 downloadBtn" download>アンケート用紙をダウンロード</v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script>

</script>
<style lang="scss">
  .downloadFrame {
    width: 80%;
    margin: 0 auto;
    margin-top: 20%;
    text-align: center !important;
    .v-card__title {
      display: block;
    }
    .downloadBtn {
      background: coral !important;
      color: white !important;
      font-weight: bold;
    }
  }
  @media (max-width: 767px) {
    .downloadFrame {
      display: none !important;
    }
  }
</style>
