<template>
  <div id="app"
       style="top:0px;left:0px;">
    <el-menu :default-active="$route.path"
             mode="horizontal"
             v-bind:router="true"
             id="nav">
      <el-menu-item index="/"
                    id="title">ICPC SCNU</el-menu-item>
      <el-menu-item index="/">
        <i class="el-icon-star-off"></i>首页
      </el-menu-item>
      <el-menu-item index="/problem">
        <i class="el-icon-menu"></i>问题
      </el-menu-item>
      <el-menu-item index="/statue">
        <i class="el-icon-tickets"></i>状态
      </el-menu-item>
      <el-menu-item index="/contest">
        <i class="el-icon-bell"></i>竞赛
      </el-menu-item>
      <el-menu-item index="/rank">
        <i class="el-icon-star-on"></i>排名
      </el-menu-item>
      <el-menu-item index="/wiki">
        <i class="el-icon-star-off"></i>百科
      </el-menu-item>

      <el-button round
                 id="button"
                 @click="registeropen"
                 v-show="!loginshow">注册</el-button>
      <el-button round
                 id="button"
                 @click="loginopen"
                 v-show="!loginshow">登陆</el-button>

      <el-dropdown id="user"
                   v-show="loginshow"
                   @command="handleCommand"
                   :show-timeout="100"
                   :split-button="true">
        <span class="el-dropdown-link">Welcome {{name}}</span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="home">Home</el-dropdown-item>
          <el-dropdown-item command="submittion">Submittion</el-dropdown-item>
          <el-dropdown-item command="setting">Setting</el-dropdown-item>
          <el-dropdown-item command="classes" divided>Class</el-dropdown-item>
          <el-dropdown-item command="admin"
                            divided
                            v-show="isadmin">Admin</el-dropdown-item>
          <el-dropdown-item command="logout"
                            divided>Logout</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-menu>

    <register ref="registerdialog"></register>

    <login ref="logindialog"></login>

    <el-backtop :bottom="50">
      <div style="{
        height: 100%;
        width: 100%;
        background-color: #f2f5f6;
        box-shadow: 0 0 6px rgba(0,0,0, .12);
        text-align: center;
        line-height: 40px;
        color: #1989fa;
      }">UP</div>
    </el-backtop>

    <transition name="el-fade-in-linear"
                mode="out-in">
      <router-view id="route"></router-view>
    </transition>
    
    <div class="footer">
      <p>地址：广东省广州市天河区中山大道西55号<span class="pipe">|</span>邮政编码：510631</p>
      <p>华南师范大学 版权所有<span class="pipe">|</span>Copyright © 2021 South China Normal University. All Rights Reserved</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {
    "login":resolve=>require(['@/login'],resolve),
    "register":resolve=>require(['@/register'],resolve)
  },
  data () {
    return {
      activeIndex: "1",
      school: "SCNU",
      loginshow: sessionStorage.username,
      username: sessionStorage.username,
      name: sessionStorage.name,
      isadmin: false
    };
  },
  mounted () {
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;

    var sb = this.$store.state.sb
    if (sb == undefined) {
      this.$axios
        .get("/settingboard/")
        .then(res => {
          if (res.data.length > 0) this.school = res.data[0].ojname;
          else this.school = "SCNU";
          this.$store.state.sb = res.data
        });
    }
    else {
      if (sb.length > 0) this.school = sb[0].ojname;
      else this.school = "SCNU";
    }


  },
  methods: {
    loginopen () {
      this.$refs.logindialog.open();
    },
    registeropen () {
      this.$refs.registerdialog.open();
    },

    handleCommand (command) {
      if (command == "logout") {
        this.$axios
          .get("/logout/")
          .then(response => {
            this.$message({
              message: "登出成功！",
              type: "success"
            });
            sessionStorage.setItem("username", "");
            sessionStorage.setItem("name", "");
            sessionStorage.setItem("rating", "");
            sessionStorage.setItem("type", "");
            this.loginshow = 0;
            this.username = "";
            this.$router.go(0);
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      }
      if (command == "home") {
        this.$router.push({
          name: "user",
          query: { username: sessionStorage.username }
        });
      }
      if (command == "setting") {
        this.$router.push({
          name: "setting",
          params: { username: sessionStorage.username }
        });
      }
      if (command == "submittion") {
        this.$router.push({
          name: "statue",
          query: { username: sessionStorage.username }
        });
      }
      if (command == "admin") {
        this.$router.push({
          name: "admin"
        });
      }
      if (command == "classes") {
        this.$router.push({
          name: "classes"
        });
      }
    }
  }
};
</script>

<style scope>
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
#button {
  float: right;
  margin: 10px;
}
#user {
  float: right;
  margin: 10px;
}
#nav {
  background-color: #ffffff;
  position: relative;
  left: 0px;
  top: 0px;
  z-index: 5;
  width: 100%;
  /* box-shadow: 00px 0px 00px rgb(255, 255, 255),
    0px 0px 10px rgb(255, 255, 255),
     0px 0px 0px rgb(255, 255, 255),
     1px 1px 0px rgb(218, 218, 218);  */
}
#route {
  position: relative;
  top: 10px;
}
#title {
  font-size: 20px;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
.footer {
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: center;
  font-size: small;
}
</style>
