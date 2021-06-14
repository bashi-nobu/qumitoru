<template>
  <v-navigation-drawer
    permanent
    expand-on-hover
    app
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
        v-for="list in nav_list.lists"
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
    }
  }
}
</script>
<style scoped>
  .sidemenu-logo-frame {
    margin-right: 3px !important;
    max-width: 170px !important;
  }
  .sidemenu-logo {
    width: 40px;
  }
  .sidemenu-logo img {
    width: 40px;
  }
  .v-icon, .v-list-item__title{
    color: red;
  }
</style>
