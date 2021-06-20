<template>
  <div class="scoreDataListFrame">
    <div v-if="isPageLoading" class="loading-frame">
      <vue-loading type="spin" color="coral" class="page-loading"></vue-loading>
    </div>
    <div v-else>
      <AggregationPeriod :dates="this.dates" @checkPeriod="changePeriod"></AggregationPeriod>
      <Questionnaire></Questionnaire>
      <v-data-table
        :headers="headers"
        :items="scoreDataList"
        :items-per-page="10"
        class="elevation-1 score-data-list"
        hide-default-footer
      >
        <template v-slot:item.img="{ item }">
          <v-chip
            class="editBtn"
            @click="openModal(item.img)"
          >
            <img :src="getImgFromS3(item.img)" class="capturedImage">
          </v-chip>
        </template>
      </v-data-table>
      <v-pagination
        v-model="page"
        :length="this.pageCount"
        circle
        color="#FF7F50"
        @input="getList"
        class="scoreDataPageNation"
      ></v-pagination>
      <ScoreEditModal
        ref="scoreEditModal"
        @updateScoreDataList='updateScoreDataList'
      >
      </ScoreEditModal>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { VueLoading } from 'vue-loading-template'
import Questionnaire from '../components/questionnaire.vue'
import AggregationPeriod from '../components/aggregationPeriod.vue'
import ScoreEditModal from '../components/scoreEditModal.vue'

export default {
  name: 'List',
  data () {
    return {
      page: 1,
      perPageItems: 10,
      dataList: null,
      pageCount: null,
      next: null,
      previous: null,
      detailImg: null,
      scoreList: null,
      isPageLoading: true,
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
      getListApiUrl: function(number) {
        let url;
        let pageNum = number ? number : 1;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/questionnaire/questionnaire/'
        }else if(process.env.NODE_ENV === 'test' || window.location.port === '8081'){ // testing
          url = 'http://172.17.0.1:33000/questionnare'+pageNum
        }else if(process.env.NODE_ENV === 'production'){
          url = 'http://0.0.0.0:1337/questionnaire/questionnaire/'
        }
        return url;
      }
    }
  },
  created () {
    this.getList();
  },
  components: {
    VueLoading,
    Questionnaire,
    AggregationPeriod,
    ScoreEditModal
  },
  methods: {
    openModal(img) {
      this.$refs.scoreEditModal.openModal(img, this.dataList)
    },
    getImgFromS3(img_path) {
      if(process.env.NODE_ENV === 'development'){
        return "https://qumitoru-dev.s3-ap-northeast-1.amazonaws.com/" + img_path
      }else{
        return "https://qumitoru-prd.s3-ap-northeast-1.amazonaws.com/" + img_path
      }
    },
    getList(number) {
      this.isPageLoading = true
      if(this.dates.length == 0){ this.setDefaultDate() }
      let pageNum = number ? number : 1;
      let config = {
        headers: {
          'content-type': 'multipart/form-data',
          'Access-Control-Allow-Origin': 'http://localhost:8080'
        },
        params: {
          periodStart: this.dates[0],
          periodEnd: this.dates[1],
        }
      };
      let url = this.getListApiUrl(number);
      axios.get(url + '?p=' + pageNum + '&userid='+this.$session.get("userid"), config)
      .then(function(response){
        this.dataList = response.data.results
        this.pageCount =  Math.ceil(response.data.count / this.perPageItems)
        this.next = response.data.next
        this.previous = response.data.previous
        this.scoreDataList = []
        for(let data of this.dataList){
          this.scoreDataList.push(
            {
              id: data.id,
              date: data.take_at,
              q1: data.q1,
              q2: data.q2,
              q3: data.q3,
              q4: data.q4,
              q5: data.q5,
              q6: data.q6,
              q7: data.q7,
              img: data.file_path,
              take_at: this.convertDateToString(data.updated_at)
            }
          )
        }
        this.isPageLoading = false
      }.bind(this))
      .catch(e => {
        console.log(e);
      })
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
            this.updateEditScoreData(this.targetId, this.scoreList, this.scoreDataList)
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
    },
    changePeriod(dates) {
      this.dates = dates
      this.getList(1);
    },
    setDefaultDate() {
      var dt = new Date();
      dt.setDate(dt.getDate() - 7);
      let defaultDateRangeMin = dt.toISOString().substr(0, 10);
      let defaultDateRangeMax = new Date().toISOString().substr(0, 10);
      this.dates = [defaultDateRangeMin, defaultDateRangeMax];
    },
    updateScoreDataList(id, scoreList) {
      for(let data of this.scoreDataList){
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
    }
  }
}
</script>

<style lang="scss">
  @import '../assets/css/list.scss';
</style>
