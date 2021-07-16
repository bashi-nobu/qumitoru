<template>
  <v-app>
    <sidebar v-show="isLogin"  @logouted="hideSidebar" id="sidebar"></sidebar>

    <v-main app>
      <router-view
        @logined="showSidebar"
      />
    </v-main>

    <v-footer app>
    </v-footer>
  </v-app>
</template>

<script>
import router from "./router";
import sidebar from './components/sidebar.vue'

export default {
  components: { sidebar },
  name: 'App',
  data: () => ({
    isLogin: false
  }),
  mounted() {
		this.checkLoggedIn();
	},
	methods: {
    checkLoggedIn() {
      this.$session.start();
      if(this.$route.path === '/howto'){
        router.push("/howto").catch(()=>{});
      }else if (!this.$session.has("token")) {
        if(this.$route.path !== '/auth'){router.push("/auth").catch(()=>{});}
      }else{
        this.isLogin = true;
        if(this.$route.path === '/auth'){router.push("/").catch(()=>{});}
      }
    },
    showSidebar() {
      this.isLogin = true;
    },
    hideSidebar() {
      this.isLogin = false;
    }
	}
}
</script>

<style scoped>
@import "./assets/css/main.scss";
@import "./assets/css/modal.scss";

</style>
