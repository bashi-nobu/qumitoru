<template>
  <div>
    <v-btn class="startAggregateBtn" text v-on:click="show">集計を開始する</v-btn>
    <modal name="aggregate-modal" class="aggregate-modal">
      <div class="modal-header">
        <h2>アンケート実施日を入力してください</h2>
      </div>
      <div class="modal-body">
        <div v-if="!isModalLoading">
          <v-menu
            ref="menu"
            v-model="menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            persistent
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="date"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                class="date-picker-field"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="date"
              :active-picker.sync="activePicker"
              :max="new Date().toISOString().substr(0, 10)"
              locale="jp-ja"
              min="2020-01-01"
              header-color="red lighten-1"
              :day-format="date => new Date(date).getDate()"
              @change="save"
            ></v-date-picker>
          </v-menu>
          <v-btn class="startAggregateConfirmBtn" text v-on:click="aggregate">集計を開始する</v-btn>
        </div>
        <div v-else>
          <vue-loading type="spin" color="coral" class="aggregate_loading"></vue-loading>
        </div>
      </div>
    </modal>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2';
import { VueLoading } from 'vue-loading-template'

export default {
  data () {
    return {
      isLoading: false,
      isModalLoading: false,
      uploadFilesCount: 0,
      activePicker: null,
      date: new Date().toISOString().substr(0, 10),
      menu: false,
      getAggregateApiUrl: function() {
        let url, currentPort = window.location.port, currentHost= window.location.host;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/uploader/v1/upload/'
        }else if(currentPort === '8081'){ // testing
          url = 'http://172.17.0.1:33000/upload'
        }else{
          url = 'http://'+currentHost+'/uploader/v1/upload/'
        }
        return url;
      }
    }
  },
  components: {
    VueLoading
  },
  methods: {
    show: function() {
      this.$modal.show('aggregate-modal');
      this.menu = false;
    },
    hide: function () {
      this.$modal.hide('aggregate-modal');
    },
    save: function () {
      this.menu = false;
    },
    aggregate() {
      this.isModalLoading = true;
      let url = this.getAggregateApiUrl();
      let formData = new FormData();
      formData.append('user_id', this.$session.get("userid"));
      formData.append('take_at', this.date);
      let config = {
        headers: {
          'content-type': 'multipart/form-data'
        }
      };
      axios.put(url, formData, config)
      .then(function(response){
        if(response.data.result == 'SUCCESS'){
          this.$emit('resetUploadFileCount', 0);
          this.isModalLoading = false;
          this.hide();
          Swal.fire({
            icon: "success",
            title: '集計を開始しました',
            text: 'アップロードされたアンケートの集計を開始しました。集計結果は数分後に集計一覧で確認できます。',
            showConfirmButton:false,
            showCloseButton:true
          })
        }else{
          this.isModalLoading = false;
          Swal.fire({
            icon: "warning",
            title: 'エラー',
            text: '集計開始ボタンを再度クリックしてください。',
            showConfirmButton:false,
            showCloseButton:true
          })
        }
      }.bind(this))
      .catch(e => {
        this.isModalLoading = false;
        Swal.fire({
          icon: "warning",
          title: 'エラー',
          text: '集計開始ボタンを再度クリックしてください。',
          showConfirmButton:false,
          showCloseButton:true
        })
        console.log(e);
      })
    }
  }
}
</script>

<style lang="scss">
  @import '../assets/css/aggregateModal.scss';
</style>
