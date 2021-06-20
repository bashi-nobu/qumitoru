<template>
  <v-main class="selectPeriodFrame">
    <v-menu
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      min-width="auto"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          label="集計期間"
          v-model="dateRangeText"
          prepend-icon="mdi-calendar"
          readonly
          v-bind="attrs"
          v-on="on"
          class="date-picker-field"
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="submitPeriod"
        :max="new Date().toISOString().substr(0, 10)"
        locale="jp-ja"
        min="2020-01-01"
        :day-format="date => new Date(date).getDate()"

        range
      ></v-date-picker>
    </v-menu>
  </v-main>
</template>

<script>
  export default {
    props: {
      dates: {
        type: Array,
        required: true
      }
    },
    computed: {
      dateRangeText () {
        return this.dates.join(' ~ ')
      },
      submitPeriod: {
        get() {
          return this.dates;
        },
        set(newVal) {
          if(newVal[0] > newVal[1]){
            newVal = [newVal[1], newVal[0]]
          }
          this.$emit('checkPeriod', newVal);
        }
      }
    }
  }
</script>

<style lang="scss">
  @import "../assets/css/aggregatePeriod.scss";
</style>
