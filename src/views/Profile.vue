<template>
  <div>
    <div class="ui main container">

      <!--ロゴとウェルカムメッセージ-->
      <div class="ui grid">
        <div class="row">
          <div class="column">
            <div class="ui items">
              <div class="item">
                <img class="ui small image" src="../assets/Bulkbuddy_rogo.png" alt="Bulkbuddy_rogo">
                <div class="content vertical-align-parent">
                  <p class="vertical-align-child">{{ this.user.name }}さん、こんにちは！</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ローディング表示 -->
      <div class="ui active inverted page dimmer" v-if="isCallingApi">
        <div class="ui text loader">Loading</div>
      </div>

      <div class="ui segment">
        <!-- エラーメッセージ-->
        <p class="ui negative message" v-if="errorMsg">
          <i class="close icon" @click="clearMsg('error')"></i>
          <span class="header">エラーが発生しました！</span>
          {{ errorMsg }}
        </p>

        <!-- 成功メッセージ-->
        <p class="ui positive message" v-if="successMsg">
          <i class="close icon" @click="clearMsg"></i>
          <span class="header">完了しました！</span>
          {{ successMsg }}
        </p>

        <!-- 更新情報入力フォーム -->
        <form class="ui large form" @submit.prevent="submit">
          <h3 class="ui centered header title-text">
            ユーザー情報の編集
          </h3>

          <div class="field">
            <label>目標体重</label>
            <input v-model="user.targetWeight" type="number" min="30" placeholder="目標体重の数字を入力" />
          </div>

          <div class="field">
            <label>ユーザー名(英数字)</label>
            <input v-model="user.userId" type="text" placeholder="ユーザー名を入力" />
          </div>

          <div class="field" v-if="!isLogin">
            <label>ニックネーム</label>
            <input v-model="user.name" type="text" placeholder="ニックネームを入力" />
          </div>

          <div class="field">
            <label>パスワード</label>
            <input v-model="user.password" type="password" placeholder="パスワードを入力" />
          </div>

          <div class="field">
            <label>身長 (cm)</label>
            <input v-model.number="user.height" type="number" min="100" max="250" placeholder="身長" />
          </div>

          <!--<div class="field">-->
          <!--  <div class="ui left icon input">-->
          <!--    <i class="calendar icon"></i>-->
          <!--    <input v-model.number="user.age" type="number" min="0" placeholder="Age" />-->
          <!--  </div>-->
          <!--</div>-->
          
          <div class="ui centered grid">
            <div class="center aligned column">
              <button class="ui button orange-button"  v-bind:disabled="isButtonDisabled" type="submit">更新</button>
            </div>
          </div>
        </form>
      </div>
      
      <div class="ui centered grid">
        <div class="center aligned column">
          <button @click="deleteUser" class="ui button grey-button" type="submit">退会</button>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
  // 必要なものはここでインポートする
  // @は/srcの同じ意味です
  // import something from '@/components/something.vue';
  import { baseUrl } from '@/assets/config.js';

  const headers = { 'Authorization': 'mtiToken' };

  export default {
    name: 'Profile',

    components: {
      // 読み込んだコンポーネント名をここに記述する
    },

    data() {
      // Vue.jsで使う変数はここに記述する
      return {
        user: {
          userId: window.localStorage.userId,
          targetWeight: null,
          name: null,
          password: null,
          height: null,
        },
        errorMsg: '', // 発展課題のエラーメッセージ用
        successMsg: '', //発展課題の成功メッセージ用
        isCallingApi: false // 発展課題のローディング表示用
      };
    },

    computed: {
      // 計算した結果を変数として利用したいときはここに記述する
      isButtonDisabled() {
        const { 
          userId,
          targetWeight,
          name,
          password,
          height,
          } = this.user;
        return !userId || !targetWeight || !name || !password || !height;
      },
    },

    methods: {
      // Vue.jsで使う関数はここで記述する
      // エラー・成功メッセージ
      clearMsg(target) {
        if (target === 'error') {
          this.errorMsg = '';
        }
        else {
          this.successMsg = '';
        }
      },

      async submit() {
        if (this.isCallingApi) {
          return;
        }
        this.isCallingApi = true;

        const {
          userId,
          targetWeight,
          name,
          password,
          height,
        } = this.user;
        
        const reqBody = {
          userId,
          targetWeight,
          name,
          password,
          height,
        };

        try {
          /* global fetch */
          const res = await fetch(baseUrl + '/user', {
            method: 'PUT',
            body: JSON.stringify(reqBody),
            headers
          });

          const text = await res.text();
          const jsonData = text ? JSON.parse(text) : {}

          // fetchではネットワークエラー以外のエラーはthrowされないため、明示的にthrowする
          if (!res.ok) {
            const errorMessage = jsonData.message ?? 'エラーメッセージがありません';
            throw new Error(errorMessage);
          }

          this.successMsg = 'ユーザー更新処理が完了しました'
          
        }
        catch (e) {
          this.errorMsg = `ユーザー更新時にエラーが発生しました: ${e}`;
        }
        finally {
          this.isCallingApi = false;
        }
      },

      async deleteUser() {
        if (this.isCallingApi) {
          return;
        }
        this.isCallingApi = true;

        try {
          /* global fetch */
          const res = await fetch(`${baseUrl}/user?userId=${this.user.userId}`, {
            method: 'DELETE',
            headers
          });

          const text = await res.text();
          const jsonData = text ? JSON.parse(text) : {}

          // fetchではネットワークエラー以外のエラーはthrowされないため、明示的にthrowする
          if (!res.ok) {
            const errorMessage = jsonData.message ?? 'エラーメッセージがありません';
            throw new Error(errorMessage);
          }

          // アカウント自体が消えるので、ログイン情報も破棄する
          window.localStorage.clear();
          this.$router.push({ name: 'Login' });
        }
        catch (e) {
          this.errorMsg = `ユーザー削除時にエラーが発生しました: ${e}`;
        }
        finally {
          this.isCallingApi = false;
        }
      }
    },

    created: async function() {
      this.isCallingApi = true;

      try {
        /* global fetch */
        const res = await fetch(baseUrl + `/user?userId=${this.user.userId}`, {
          method: 'GET',
          headers
        });

        const text = await res.text();
        const jsonData = text ? JSON.parse(text) : {}

        // fetchではネットワークエラー以外のエラーはthrowされないため、明示的にthrowする
        if (!res.ok) {
          const errorMessage = jsonData.message ?? 'エラーメッセージがありません';
          throw new Error(errorMessage);
        }

        console.log(jsonData)
        this.user.targetWeight = jsonData.targetWeight;
        this.user.userId = jsonData.userId;
        this.user.name = jsonData.name;
        this.user.height = jsonData.height;
      }
      catch (e) {
        this.errorMsg = `ユーザー情報取得時にエラーが発生しました: ${e}`;
      }
      finally {
        this.isCallingApi = false;
      }
    }
  }
</script>

<style scoped>
  /* このコンポーネントだけに適用するCSSはここに記述する */
  .vertical-align-parent {
    position: relative;
  }

  .vertical-align-child {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  
  .orange-button {
    background-color: #F68712;
    color: white;
    width: 25%;
    margin: 20px;
  }

  .grey-button {
    background-color: #333;
    color: white;
    width: 24%;
    margin: 20px;
  }

  .title-text {
    padding: 20px;
  }
</style>
