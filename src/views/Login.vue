<template>
  <div>
    <div class="ui main container">

      <img class="ui centered medium image" src="../assets/Bulkbuddy_rogo.png" alt="Bulkbuddy_rogo">

      <!-- ローディング表示 -->
      <div class="ui active inverted page dimmer" v-if="isCallingApi">
        <div class="ui text loader">Loading</div>
      </div>

      <div class="ui segment">
        <!-- エラーメッセージ-->
        <p class="ui negative message" v-if="errorMsg">
          <i class="close icon" @click="clearError"></i>
          <span class="header">エラーが発生しました！</span>
          {{ errorMsg }}
        </p>

        <!-- submitイベントを拾って、preventにて規定のアクションを中止し、submitメソッドを呼び出す。-->
        <form class="ui large form" @submit.prevent="submit">
          <h3 class="ui centered header title-text">
            {{ toggledTitleText }} <br> {{ toggledSubTitleText }}
          </h3>

          <div class="field" v-if="!isLogin">
            <label>目標体重</label>
            <input v-model="user.targetWeight" type="number" min="30" placeholder="目標体重の数字を入力" />
            <!--右側にkgの表示をつけることもできるが高さの修正方法が不明-->
            <!--<div class="ui right labeled input">-->
            <!--  <input type="text" placeholder="Enter weight..">-->
            <!--  <div class="ui basic label">-->
            <!--    kg-->
            <!--  </div>-->
            <!--</div>-->
          </div>

          <div class="field">
            <label>ユーザー名(英数字を推奨)</label>
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

          <div class="field" v-if="!isLogin">
            <label>性別（正確なカロリー計算のために使用します）</label>
            <div class="fields">
              <label>
                <input type="radio" v-model="selectedOption" name="options" value="male" />
                男性
              </label>
              <label>
                <input type="radio" v-model="selectedOption" name="options" value="female" />
                女性
              </label>
            </div>
          </div>

          <div class="field" v-if="!isLogin">
            <label>生年月日</label>
            <div class="fields">
              <div class="field">
                <input v-model="user.birth_year" type="number" min="1950" max="2023" placeholder="年" />
              </div>
              <div class="field">
                <input v-model="user.birth_month" type="number" min="1" max="12" placeholder="月" />
              </div>
              <div class="field">
                <input v-model="user.birth_day" type="number" min="1" max="31" placeholder="日" />
              </div>
            </div>
          </div>

          <div class="fields" v-if="!isLogin">
            <div class="field">
              <label>身長 (cm)</label>
              <input v-model.number="user.height" type="number" min="100" max="250" placeholder="身長" />
            </div>
            <div class="field">
              <label>体重 (kg)</label>
              <input v-model.number="user.weight" type="number" min="30" placeholder="体重" />
            </div>
          </div>

          <div class="ui centered grid">
            <div class="center aligned column">
              <button class="ui button orange-button" :disabled="isButtonDisabled" type="submit">{{ submitBtnText }}</button>
            </div>
          </div>
        </form>
      </div>

      <div class="ui centered grid">
        <div class="center aligned column">
          <button @click="toggleMode" class="ui button grey-button" type="submit">{{ toggledBtnText }}</button>
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

  export default {
    name: 'Login',

    components: {
      // 読み込んだコンポーネント名をここに記述する
    },

    data() {
      // Vue.jsで使う変数はここに記述する
      return {
        isLogin: true,
        user: {
          userId: null,
          name: null,
          password: null,
          height: null,
          weight: null,
          birth_year: null,
          birth_month: null,
          birth_day: null,
          targetWeight: null,
          // targetDate: null,
          // 男性は0女性は1
          gender: null,
        },
        errorMsg: '', // 発展課題のエラーメッセージ用
        isCallingApi: false // 発展課題のローディング表示用
      };
    },

    // selectedOptionが変更される度に呼ばれるので、genderに値が入る
    watch: {
      selectedOption(newValue) {
        // selectedOptionの値に基づいてgenderを更新
        this.user.gender = newValue === 'male' ? 1 : 2;
        console.log("変更しました")
      }
    },

    computed: {
      // 計算した結果を変数として利用したいときはここに記述する

      // ボタン活性/非活性用
      isButtonDisabled() {
        const {
          userId,
          name,
          password,
          height,
          weight,
          birth_year,
          birth_month,
          birth_day,
          targetWeight,
          gender
        } = this.user;

        return this.isLogin ?
          !userId || !password :
          !userId || !name || !password || !height || !weight || !birth_year || !birth_month || !birth_day || !targetWeight || gender;
      },

      gender() {
        // selectedOptionの値に基づいて男性は1、女性は2を返す
        return this.selectedOption === 'male' ? 1 : 2;
        console.log("性別を返しました")
      },

      toggledTitleText() {
        return this.isLogin ? 'ログイン' : '目標設定には新規登録が必要です'
      },

      toggledSubTitleText() {
        return this.isLogin ? '' : 'あなたについて教えてください'
      },

      submitBtnText() {
        return this.isLogin ? 'ログイン' : '新規登録'
      },

      toggledBtnText() {
        return this.isLogin ? '新規登録はこちら' : 'ログインはこちら'
      }
    },


    methods: {
      // Vue.jsで使う関数はここで記述する

      // エラーメッセージ
      clearError() {
        this.errorMsg = ''
      },

      toggleMode() {
        this.isLogin = !this.isLogin;
      },

      async submit() {
        if (this.isCallingApi) {
          return;
        }
        this.isCallingApi = true;

        const path = this.isLogin ? '/user/login' : '/user/signup';

        const {
          userId,
          name,
          password,
          height,
          weight,
          birth_year,
          birth_month,
          birth_day,
          targetWeight,
          gender
        } = this.user;
        
        const reqBody = this.isLogin ? { userId, password } : {
          userId,
          name,
          password,
          height,
          weight,
          birth_year,
          birth_month,
          birth_day,
          targetWeight,
          gender: this.gender
        };

        console.log(reqBody)

        try {
          /* global fetch */
          const res = await fetch(baseUrl + path, {
            method: 'POST',
            body: JSON.stringify(reqBody)
          });

          const text = await res.text();
          const jsonData = text ? JSON.parse(text) : {}

          // fetchではネットワークエラー以外のエラーはthrowされないため、明示的にthrowする
          if (!res.ok) {
            const errorMessage = jsonData.message ?? 'エラーメッセージがありません';
            throw new Error(errorMessage);
          }

          window.localStorage.setItem('token', jsonData.token);
          window.localStorage.setItem('userId', this.user.userId);

          this.$router.push({ name: 'Home' });
          console.log(jsonData)
        }
        catch (e) {
          console.error(e);
          this.errorMsg = e;
        }
        finally {
          this.isCallingApi = false;
        }
      }
    },
  }
</script>

<style scoped>
  /* このコンポーネントだけに適用するCSSはここに記述する */
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
