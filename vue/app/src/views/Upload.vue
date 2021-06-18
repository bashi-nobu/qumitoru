<template>
  <div class="upload-form">
    <v-card>
      <v-card-title class="upload-form__title">
        <v-icon>mdi-camera-plus-outline</v-icon>
        をクリックしてアンケートを撮影してください</v-card-title>
      <v-card-text class="upload-form__bth-frame">
        <v-form ref="upload_form">
          <v-file-input
            accept="*"
            v-model="uploadFile"
            capture="camera"
            hide-input
            prepend-icon="mdi-camera-plus-outline"
            @change="submit"
            v-if="!isLoading"
          ></v-file-input>
          <span v-else>
            <vue-loading type="spin" color="coral" class="loading"></vue-loading>
          </span>
        </v-form>
      </v-card-text>

      <v-divider></v-divider>
      <v-card-actions v-if="this.uploadFilesCount > 0" class="calculate-frame">
        <span class="uploadStatus">現在{{this.uploadFilesCount}}枚のアンケートがアップロードされています</span>
        <AggregateModal
          @resetUploadFileCount="resetUploadFilesCount"
        >
        </AggregateModal>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2';
import { VueLoading } from 'vue-loading-template'
import AggregateModal from '../components/aggregateModal.vue'

export default {
  name: 'Upload',
  data () {
    return {
      uploadFile: null,
      isLoading: false,
      isModalLoading: false,
      uploadFilesCount: 0,
      activePicker: null,
      date: new Date().toISOString().substr(0, 10),
      menu: false,
      getUploadedFileCountApiUrl: function() {
        let url;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/uploader/v1/upload/'
        }else if(window.location.port === '8081'){ // testing
          url = 'http://172.17.0.1:33000/uploaded_file_count'
        }else if(process.env.NODE_ENV === 'production'){
          url = 'http://127.0.0.1:8001/uploader/v1/upload/'
        }
        return url;
      },
      getUploadApiUrl: function() {
        let url;
        if(process.env.NODE_ENV === 'development'){
          url = 'http://0.0.0.0:8001/uploader/v1/upload/'
        }else if(window.location.port === '8081'){ // testing
          url = 'http://172.17.0.1:33000/upload'
        }else if(process.env.NODE_ENV === 'production'){
          url = 'http://0.0.0.0:1337/uploader/v1/upload/'
        }
        return url;
      }
    }
  },
  created () {
    this.getUploadedFileCount();
  },
  components: {
    VueLoading,
    AggregateModal
  },
  methods: {
    getUploadedFileCount (){
      let config = {
        headers: {
          'content-type': 'multipart/form-data',
          'Access-Control-Allow-Origin': 'http://localhost:8080'
        }
      };
      let url = this.getUploadedFileCountApiUrl();
      axios.get(url + '?id='+this.$session.get("userid"), config)
      .then(function(response){
        this.uploadFilesCount = response.data.count
      }.bind(this))
      .catch(e => {
        console.log(e);
      })
    },
    resetUploadFilesCount() {
      this.uploadFilesCount = 0
    },
    submit() {
      if (this.$refs.upload_form.validate()) {
        this.isLoading = true;
        let url = this.getUploadApiUrl();
        let formData = new FormData();
        formData.append('file', this.uploadFile);
        formData.append('user_id', this.$session.get("userid"));
        let config = {
          headers: {
            'content-type': 'multipart/form-data',
            'Access-Control-Allow-Origin': 'http://localhost:8080'
          }
        };
        axios.post(url, formData, config)
        .then(function(response){
            this.isLoading = false;
            if(response.data.result == 'SUCCESS'){
              this.uploadFilesCount = response.data.uploadFilesCount
              Swal.fire({
                icon: "success",
                title: '読み取り成功',
                text: 'アップロードしたアンケートの集計を開始する場合は「集計開始」ボタンをクリック後、集計日を入力してください',
                showConfirmButton:false,
                showCloseButton:true
              })
            }else{
              Swal.fire({
                icon: "warning",
                title: '読み取り失敗',
                text: 'アンケートを真上から再度撮影してください。',
                showConfirmButton:false,
                showCloseButton:true
              })
            }
        }.bind(this))
        .catch(e => {
          this.isLoading = false;
          Swal.fire({
            icon: "warning",
            title: '読み取り失敗',
            text: 'アンケートを真上から再度撮影してください。',
            showConfirmButton:false,
            showCloseButton:true
          })
          console.log(e);
        })
      }
    }
  }
}
</script>

<style lang="scss">
  @import '../assets/css/upload.scss';
</style>
