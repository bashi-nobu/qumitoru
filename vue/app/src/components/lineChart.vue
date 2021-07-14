<template>
  <div class="col-lg-4 col-12">
    <div class="v-card--material pa-3 v-card--material-chart v-card v-sheet theme--light v-card--material--has-heading" hover-reveal="">
      <div class="d-flex grow flex-wrap">
        <div class="text-start v-card--material__heading mb-n6 v-sheet theme--dark elevation-6 pa-7" style="width: 100%; background-color: white; border-color: rgb(233, 30, 99);">
          <div class="ct-square">
            <GChart
              type="LineChart"
              :data="dailyScoreData"
              :options="{title: dailyScoreData[0][1]}"
            />
          </div>
        </div>
      </div>
      <h4 class="card-title font-weight-light mt-2 ml-2"> {{this.dailyScoreData[0][1]}} </h4>
      <hr role="separator" aria-orientation="horizontal" class="mt-2 v-divider theme--light">
      <div class="v-card__actions pb-0">
        <i aria-hidden="true" class="v-icon notranslate mr-1 mdi mdi-clock-outline theme--light" style="font-size: 16px;"></i>
        <span class="caption grey--text font-weight-light">{{this.period[0]}} ~ {{this.period[1]}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts';

export default {
  data() {
    return {
      aggregatePeriod: null
    }
  },
  components: {
    GChart
  },
  props: {
    dailyScoreData: {
      type: Array
    },
    period: {
      type: Array
    }
  },
  created() {
    this.makeAggregatePeriodStr();
  },
  methods: {
    makeAggregatePeriodStr() {
      if(this.period[1]){
        this.aggregatePeriod = this.period[0] +' ~ '+this.period[1]
      }else{
        this.aggregatePeriod = this.period[0]
      }
    }
  }
}
</script>
<style scoped>
.v-card--material__heading {
  position: relative !important;
  top: -30px !important;
}
.card-title {
  color: gray;
}
</style>
