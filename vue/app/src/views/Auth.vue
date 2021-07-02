<template>
  <v-container grid-list-md justify-content-center class="auth-frame">
    <v-layout row wrap align-center justify-center fill-height>
      <v-flex xs12 sm8 lg4 md5>
        <v-card class="login-card">
          <v-card-title>
            <img class="img" src="../assets/qumitoru-top-logo.png" width="100%">
          </v-card-title>

          <v-spacer/>

          <v-card-text>

          <v-layout
            row
            fill-height
            justify-center
            align-center
            v-if="loading"
          >
            <v-progress-circular
              :size="50"
              color="primary"
              indeterminate
            />
          </v-layout>

          <v-form v-else ref="form" class="login-form" v-model="valid" lazy-validation>
            <v-container>

            <v-text-field
              v-model="credentials.username"
              :counter="20"
              label="ユーザー名"
              :rules="rules.username"
              maxlength="20"
              autocomplete="off"
              id="input_username"
              required
            />

            <v-text-field
              type="password"
              v-model="credentials.password"
              :counter="20"
              label="パスワード"
              :rules="rules.password"
              maxlength="20"
              autocomplete="off"
              name="password"
              required
            />

            </v-container>
            <v-btn class="pink white--text login-btn" :disabled="!valid" @click="login">Login</v-btn>
          </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import router from '../router';

export default {
  name: 'Auth',
  data: () => ({
    credentials: {},
    valid:true,
    loading:false,
    rules: {
      username: [
          v => !!v || "ユーザー名は必須です",
          v => (v && v.length > 4) || "ユーザー名は5文字以上でなければなりません",
          v => /^[a-z0-9_]+$/.test(v) || "許可されていない文字が入力されています"
      ],
      password: [
          v => !!v || "パスワードは必須です",
          v => (v && v.length > 4) || "パスワードは5文字以上でなければなりません"
      ]
    },
    getApiUrl: function() {
      let url, currentPort = window.location.port, currentHort= window.location.host;
      if(process.env.NODE_ENV === 'development'){
        url = 'http://0.0.0.0:8001/auth/'
      }else if(currentPort === '8081'){ // testing
        url = 'http://172.17.0.1:33000/auth'
      }else{
        url = 'http://'+currentHort+'/auth/'
      }
      return url;
    }
  }),
  methods: {
    login() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        let url = this.getApiUrl();
        axios.post(url, this.credentials).then(res => {
          this.$session.start();
          this.$session.set('token', res.data.token);
          this.$session.set('userid', res.data.userid);
          this.$session.set('username', res.data.username);
          this.$emit('logined', true);
          router.push('/dashboard');
        // eslint-disable-next-line
        }).catch(e => {
          this.loading = false;
          Swal.fire({
            icon: "warning",
            title: 'エラー',
            text: 'ユーザー名もしくはパスワード、または両方が間違っています',
            showConfirmButton:false,
            showCloseButton:false,
            timer:3000
          })
        })
      }
    }
  }
}
</script>

<style lang="scss">
  @import "../assets/css/auth.scss";
</style>
