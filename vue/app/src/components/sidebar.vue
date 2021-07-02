<template>
  <v-navigation-drawer
    permanent
    expand-on-hover
    app
    class="sidemenu"
  >
    <v-list>
      <v-list-item class="px-2">
        <v-list-item-icon class="sidemenu-logo-frame">
          <div class="sidemenu-logo"><img src="../assets/qumitoru-icon.png"></div>
        </v-list-item-icon>
        <v-list-item-title class="sidemenu-logo-frame"><v-img src="../assets/qumitoru-liner.png"></v-img></v-list-item-title>
      </v-list-item>

      <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-account</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{this.username}}</v-list-item-title>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list
      nav
      dense
    >
      <v-list-item
        v-for="list in navListFilter"
        :key="list.name"
        :to="list.link"
      >
        <v-list-item-icon>
          <v-icon>{{ list.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ list.name }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link @click="logOut" class="logoutBtn">
        <v-list-item-icon>
          <v-icon>mdi-logout-variant</v-icon>
        </v-list-item-icon>
        <v-list-item-title>ログアウト</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import router from "../router";

export default {
  data() {
    return {
      username: this.$session.get('username'),
      isSmartPhoneWindowSize: false,
      spNavMenus: ['/dashboard','/upload','/howto'],
      nav_list:
        {
          lists: [
            {
              name: "ダッシュボード",
              link: "/dashboard",
              icon: "mdi-monitor-dashboard"
            },
            {
              name: "アンケートを読み取る",
              link: "/upload",
              icon: "mdi-magnify-scan"
            },
            {
              name: "集計一覧",
              link: "/list",
              icon: "mdi-clipboard-list-outline"
            },
            {
              name: "ダウンロード",
              link: "/download",
              icon: "mdi-file-download-outline"
            },
            {
              name: "使い方",
              link: "/howto",
              icon: "mdi-account-question-outline"
            },
          ],
        }
    }
  },
  methods: {
    logOut() {
      this.$session.destroy();
      this.$emit('logouted', true);
      router.push("/auth");
    },
    checkWindowSize() {
      this.isSmartPhoneWindowSize = window.innerWidth < 767 ? true: false;
    }
  },
  computed: {
    navListFilter:function() {
      let filteredList = [];
      let lists = this.nav_list.lists;
      for(let i in lists){
        if(this.isSmartPhoneWindowSize && this.spNavMenus.includes(lists[i].link)){
          filteredList.push(lists[i]);
        }else if(!this.isSmartPhoneWindowSize){
          filteredList.push(lists[i]);
        }
      }
      return filteredList;
    }
  },
  mounted() {
    this.checkWindowSize();
  }
}
</script>
<style lang="scss">
  @import "../assets/css/sidebar.scss";
</style>
