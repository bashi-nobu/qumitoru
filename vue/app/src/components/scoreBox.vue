<template>
  <div class="col-sm-6 col-lg-3 col-12">
    <div class="v-card--material pa-3 v-card--material-stats v-card v-sheet theme--light v-card--material--has-heading">
      <div class="d-flex grow flex-wrap">
        <div class="text-start v-card--material__heading mb-n6 v-sheet theme--dark elevation-6 pa-7"
            style="max-height: 90px; width: auto;"
            v-bind:class="[isMainBox ? 'royalty-color':'other-royalty-color']">
          <i aria-hidden="true" class="v-icon notranslate mdi theme--dark" :class="this.mdiIcon"  style="font-size: 32px;"></i><!---->
        </div>
        <div class="ml-6">
          <div>
            <div class="body-3 grey--text font-weight-light">{{this.categoryName}}</div>
            <span class="ave_score"> {{this.categoryScore}} <small class="category_score_scale">/{{this.scale}}</small>
            </span>
          </div>
        </div>
      </div>
      <div class="px-0 col col-12">
        <hr role="separator" aria-orientation="horizontal" class="v-divider theme--light">
      </div>
      <i aria-hidden="true" class="v-icon notranslate ml-2 mr-1 mdi mdi-clock theme--light" style="font-size: 16px;"></i>
      <span class="caption grey--text font-weight-light">{{this.aggregatePeriod}}</span><!---->
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      aggregatePeriod: null
    }
  },
  props: {
    categoryName: {
      type: String,
      default: ''
    },
    categoryScore: {
      type: Number,
      default: 0
    },
    isMainBox: {
      type: Boolean,
      default: false
    },
    mdiIcon: {
      type: String,
      default: ''
    },
    scale: {
      type: Number,
      default: 0
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
<style lang="scss">
.v-card--material__heading {
  position: relative !important;
  top: -30px !important;
}
.royalty-color {
  color: white !important;
  background: coral !important;
  .mdi {
    color: white !important;
  }
}
.other-royalty-color {
  background: white !important;
  .mdi{
    color: coral !important;
  }
}
.category_score_scale {
  color: gray;
  font-size: 1.25rem;
}
.ave_score {
  font-size: 2.0rem !important;
}
</style>
