<template>
  <v-container class="dashboard-frame">
    <div v-if="isLoading">
      <vue-loading type="spin" color="coral" class="loading"></vue-loading>
    </div>
    <div v-else>
      <AggregationPeriod :dates="this.dates" @checkPeriod="changePeriod"></AggregationPeriod>
      <div v-if="isData">
        <v-card class="mainTitle">
          <v-card-title>平均スコア</v-card-title>
        </v-card>
        <div id="contents" style="margin-bottom: 50px;">
          <div class="row ave-score-frame">
            <ScoreBox
              categoryName="総合評価"
              :categoryScore="this.categoryAveList[0]"
              :isMainBox="true"
              :period="this.dates"
              mdiIcon="mdi-hand-heart"
            ></ScoreBox>
            <ScoreBox
              categoryName="料理満足度"
              :categoryScore="this.categoryAveList[1]"
              :period="this.dates"
              mdiIcon="mdi-food-fork-drink"
            ></ScoreBox>
            <ScoreBox
              categoryName="接客満足度"
              :categoryScore="this.categoryAveList[2]"
              :period="this.dates"
              mdiIcon="mdi-room-service-outline"
            ></ScoreBox>
            <ScoreBox
              categoryName="清潔満足度"
              :categoryScore="this.categoryAveList[3]"
              :period="this.dates"
              mdiIcon="mdi-spray-bottle"
            ></ScoreBox>
            <ScoreBox
              categoryName="雰囲気満足度"
              :categoryScore="this.categoryAveList[4]"
              :period="this.dates"
              mdiIcon="mdi-floor-lamp"
            ></ScoreBox>
            <ScoreBox
              categoryName="コスパ満足度"
              :categoryScore="this.categoryAveList[5]"
              :period="this.dates"
              mdiIcon="mdi-cash-multiple"
            ></ScoreBox>
          </div>
        </div>
        <v-card class="mainTitle">
          <v-card-title>スコア推移</v-card-title>
        </v-card>
        <div id="contents" style="margin-top: 50px;" class="line-chart-frame">
          <div class="row">
            <LineChart :dailyScoreData="this.dailyScoreData[0]" :period="this.dates"></LineChart>
            <LineChart :dailyScoreData="this.dailyScoreData[1]" :period="this.dates"></LineChart>
            <LineChart :dailyScoreData="this.dailyScoreData[2]" :period="this.dates"></LineChart>
            <LineChart :dailyScoreData="this.dailyScoreData[3]" :period="this.dates"></LineChart>
            <LineChart :dailyScoreData="this.dailyScoreData[4]" :period="this.dates"></LineChart>
            <LineChart :dailyScoreData="this.dailyScoreData[5]" :period="this.dates"></LineChart>
          </div>
        </div>
      </div>
      <div v-else>
        <span class="no-data">対象期間のデータがありません。</span>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import ScoreBox from '../components/scoreBox.vue'
import LineChart from '../components/lineChart.vue'
import AggregationPeriod from '../components/aggregationPeriod.vue'
import { VueLoading } from 'vue-loading-template'

export default {
  name: 'Dashboard',
  components: {
    VueLoading,
    ScoreBox,
    LineChart,
    AggregationPeriod
  },
  data() {
    return {
      categoryAveList: [],
      dailyScoreData: [],
      dates: [],
      isLoading: true,
      isData: false,
      chartOptions: {
        title: 'Company Performance',
        subtitle: 'Sales'
      },
      result: null,
      getDashBoardApiUrl: function() {
        let url;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/questionnaire/questionnaire/'+this.$session.get("userid")+'/make_dashboard_data/'
        }else if(process.env.NODE_ENV === 'test' || window.location.port === '8081'){ // testing
          url = 'http://172.17.0.1:33000/make_dashboard_data'
        }else if(process.env.NODE_ENV === 'production'){
          url = 'http://0.0.0.0:1337/questionnaire/questionnaire/'+this.$session.get("userid")+'/make_dashboard_data/'
        }
        return url;
      },
    };
  },
  created() {
    this.getDashboardData();
  },
  methods: {
    getDashboardData() {
      this.isLoading = true
      if(this.dates.length == 0){this.setDefaultDate()}
      let config = {
        headers: {
          'content-type': 'multipart/form-data',
          'Access-Control-Allow-Origin': 'http://localhost:8080'
        },
        params: {
          periodStart: this.dates[0],
          periodEnd: this.dates[1],
          userid: this.$session.get("userid")
        }
      };
      let url = this.getDashBoardApiUrl();
      axios.get(url, config)
      .then(function(response){
        var resData;
        if((typeof response.data) == 'string'){
          resData = JSON.parse(response.data.replace(/\bNaN\b/g, "null"))
        }else{ resData = response.data;}
        this.categoryAveList = resData.categoryAveList
        this.dailyScoreData = resData.dailyScoreData
        this.isLoading = false
        this.isData = (this.dailyScoreData.length > 0)? true:false;
      }.bind(this))
      .catch(e => {
        console.log(e);
      })
    },
    changePeriod(dates) {
      this.dates = dates
      this.getDashboardData();
    },
    setDefaultDate() {
      var dt = new Date();
      dt.setDate(dt.getDate() - 7);
      let defaultDateRangeMin = dt.toISOString().substr(0, 10);
      let defaultDateRangeMax = new Date().toISOString().substr(0, 10);
      this.dates = [defaultDateRangeMin, defaultDateRangeMax];
    }
  }
};
</script>
<style lang="scss">
.mainTitle {
  width: 200px !important;
  border-left: 5px solid coral !important;
  margin-bottom: 30px !important;
  .v-card__title {
    text-align: left !important;
    padding: 0 !important;
    padding-left: 5% !important;
    font-weight: bold !important;
    color: coral !important;
  }
}
.loading {
  width: 180px !important;
  height: 180px !important;
  margin-top: 100px !important;
}
.no-data {
  color: gray;
}
</style>
