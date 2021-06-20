<template>
  <modal name="detail-modal">
    <div class="img-frame">
      <div class="img-frame__title"><v-icon>mdi-clipboard-outline</v-icon> 読み込んだアンケート</div>
      <v-divider></v-divider>
      <v-chip class="img-frame__chip">
        <img :src="getImgFromS3(this.detailImg)">
      </v-chip>
    </div>
    <div class="ocr-result-frame">
      <div class="ocr-result-frame__title"><v-icon>mdi-magnify-scan</v-icon> 認識結果</div>
      <v-divider></v-divider>
      <div v-if="!isEditting">
        <div v-if="!isEditting" class="ocr-result-frame__list">
          <div
            class="score-frame"
            v-for="(score, index) in this.scoreList"
            :key="index"
          >
            <span class="score-label">Q{{index + 1}}:</span>
            <span class="score-val">{{score}}</span>
          </div>
        </div>
        <div class="edit-btn-frame">
          <v-btn @click="openScoreEditFrame" class="editStartBtn">修正する</v-btn>
        </div>
      </div>
      <div v-else>
        <div class="edit-select-frame">
          <v-row align="center">
            <v-col
              class="d-flex"
            >
              <v-select :items="tenScales" label="Q1" v-model="scoreList[0]"></v-select>
              <v-select :items="tenScales" label="Q2" v-model="scoreList[1]"></v-select>
              <v-select :items="fiveScales" label="Q3" v-model="scoreList[2]"></v-select>
              <v-select :items="fiveScales" label="Q4" v-model="scoreList[3]"></v-select>
              <v-select :items="fiveScales" label="Q5" v-model="scoreList[4]"></v-select>
              <v-select :items="fiveScales" label="Q6" v-model="scoreList[5]"></v-select>
              <v-select :items="fiveScales" label="Q7" v-model="scoreList[6]"></v-select>
            </v-col>
          </v-row>
        </div>
        <div class="edit-btn-frame" v-if="!isLoading">
          <span v-if="isEdited" class="updateResult">{{this.updateResult}}</span>
          <v-btn @click="submit" class="submitBtn">登録する</v-btn>
          <v-btn @click="closeScoreEditFrame">キャンセル</v-btn>
        </div>
        <div v-else>
          <vue-loading type="spin" color="coral" class="loading"></vue-loading>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import axios from 'axios'
import { VueLoading } from 'vue-loading-template'

export default {
  data () {
    return {
      dataList: null,
      detailImg: null,
      scoreList: null,
      isEditting: false,
      isLoading: false,
      isEdited: false,
      targetId: null,
      updateResult: null,
      tenScales: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, ''],
      fiveScales: [5, 4, 3, 2, 1, ''],
      dates: [],
      headers: [
        {
          text: "実施日",
          align: 'start',
          value: 'date',
        },
        { text: 'Q1', value: 'q1' },
        { text: 'Q2', value: 'q2' },
        { text: 'Q3', value: 'q3' },
        { text: 'Q4', value: 'q4' },
        { text: 'Q5', value: 'q5' },
        { text: 'Q6', value: 'q6' },
        { text: 'Q7', value: 'q7' },
        { text: '撮影画像', value: 'img' },
        { text: '処理時刻', value: 'take_at' }
      ],
      scoreDataList: [
      ],
      convertDateToString: function(dateString) {
        var date = new Date(dateString);
        return date.toLocaleString();
      },
      getQuestionnareUpdateApiUrl: function() {
        let url;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/questionnaire/questionnaire/'+ this.$session.get("userid") +'/score_update/'
        }else if(window.location.port === '8081'){ // testing
          url = 'http://172.17.0.1:33000/score_update'
        }else if(process.env.NODE_ENV === 'production'){
          url = 'http://0.0.0.0:1337/questionnaire/questionnaire/'+ this.$session.get("userid") +'/score_update/'
        }
        return url;
      }
    }
  },
  components: {
    VueLoading,
  },
  methods: {
    openModal(img, dataList) {
      this.detailImg = img
      this.dataList = dataList
      this.$modal.show('detail-modal');
      this.isEditting = false;
      this.updateResult = null;
      this.currentScoreData();
    },
    openScoreEditFrame() {
      this.currentScoreData();
      this.isEditting = true;
    },
    closeScoreEditFrame() {
      this.currentScoreData();
      this.isEditting = false;
      this.updateResult = null;
    },
    currentScoreData() {
      for(let data of this.dataList){
        if(data.file_path == this.detailImg){
          this.targetId = data.id;
          this.scoreList = [
            data.q1,
            data.q2,
            data.q3,
            data.q4,
            data.q5,
            data.q6,
            data.q7
            ]
        }
      }
    },
    updateEditScoreData(id, scoreList, dataList) {
      for(let data of dataList){
        if(data.id == id){
          data.q1 = scoreList[0],
          data.q2 = scoreList[1],
          data.q3 = scoreList[2],
          data.q4 = scoreList[3],
          data.q5 = scoreList[4],
          data.q6 = scoreList[5],
          data.q7 = scoreList[6]
        }
      }
    },
    getImgFromS3(img_path) {
      if(process.env.NODE_ENV === 'development'){
        return "https://qumitoru-dev.s3-ap-northeast-1.amazonaws.com/" + img_path
      }else{
        return "https://qumitoru-prd.s3-ap-northeast-1.amazonaws.com/" + img_path
      }
    },
    submit() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('scoreList', this.scoreList);
      formData.append('target_id', this.targetId);
      let config = {
        headers: {
          'content-type': 'multipart/form-data',
          'Access-Control-Allow-Origin': 'http://localhost:8080'
        }
      };
      let url = this.getQuestionnareUpdateApiUrl();
      axios.post(url, formData, config)
      .then(function(response){
          this.isEdited = true;
          this.isLoading = false;
          if(response.data.result == 'SUCCESS'){
            this.updateEditScoreData(this.targetId, this.scoreList, this.dataList);
            // this.updateEditScoreData(this.targetId, this.scoreList, this.scoreDataList)
            this.$emit('updateScoreDataList', this.targetId, this.scoreList);
            this.updateResult = '更新が完了しました。'
          }else{
            this.updateResult = '通信エラーにより更新できませんでした。'
          }
          this.isLoading = false;
      }.bind(this))
      .catch(e => {
        this.isEdited = false;
        this.updateResult = '通信エラーにより更新できませんでした。'
        this.isLoading = false;
        console.log(e);
      })
    }
  }
}
</script>

<style lang="scss">
  @import "../assets/css/scoreEditModal.scss";
</style>
