<template>
  <div>
    <div class="ui main container">
      <img class="ui small image" src="../assets/Bulkbuddy_rogo.png" alt="Bulkbuddy_rogo">
      
      <!--有料プラン案内-->
      <div class="ui segment">
        <ul class="ui comments divided article-list">
          <h3>有料会員登録</h3>
          <p>月額324円のお支払いで、Bulkbuddyを利用している他のユーザーと交流が可能なコミュニティ機能を無制限でお使いいただけます。増量仲間をつくりモチベーションを共有しましょう！</p>
          <button>支払う</button>
        </ul>
      </div>
      
      <!--投稿機能-->
      <div class="ui segment">
        <form class="ui form" @submit.prevent="postArticle">
          <div class="field">
            <div class="ui input">
            <textarea
              v-model="post.text"
              placeholder="増量について発信してみましょう！"
            />
            </div>
          </div>
          <div class="field">
            <label>カテゴリー</label>
            <select v-model="post.category">
              <option value="">指定なし</option>
              <option value="食事">食事</option>
              <option value="トレーニング">トレーニング</option>
              <option value="コラム">コラム</option>
            </select>
          </div>
          <div class="right-align">
            <button
              class="ui green button"
              v-bind:disabled="isPostButtonDisabled"
              type="submit"
            >
              投稿
            </button>
          </div>
        </form>
      </div>
      
      <!--投稿一覧-->
      <h3 class="ui dividing header">投稿一覧</h3>
      <div class="ui segment">
        <ul class="ui comments divided article-list">
          <li class="comment" v-for="(article, index) in articles" :key="index">
            <div class="content">
              <span class="author">{{ article.userId }}</span>
              <span class="name">{{ article.name }}</span>
              <div class="metadata">
                <span class="date">{{ convertToLocaleString(article.timestamp) }}</span>
              </div>
              
              <p class="text">{{ article.text }}</p>
              <span v-if="article.category !== 0" class="ui green label">{{ (article.category) }}</span>
              <button
                class="ui mini button right floated"
                :class="{ 'positive': article.likepost === 1 }"
                @click="toggleLike(article)"
              >
                いいね {{ article.likepost === 1 ? '済み' : '' }}
              </button>
              <div class="ui divider"></div>
            </div>
          </li>
        </ul>
      </div>
      
    </div>
  </div>
</template>

<script>
import { baseUrl } from "@/assets/config.js";

const headers = { Authorization: "mtiToken" };

export default {
  name: "Home",

  components: {
    // 読み込んだコンポーネント名をここに記述する
  },

  data() {
    // Vue.jsで使う変数はここに記述する
    return {
      post: {
        text: null,
        category: null,
      },
      articles: [],
    };
  },

  created: async function () {
    // Vue.jsの読み込みが完了したときに実行する処理はここに記述する

    if (
      window.localStorage.getItem("userId") &&
      window.localStorage.getItem("token")
    ) {
      this.iam = window.localStorage.getItem("userId");
      await this.getArticles();
    } else {
      window.localStorage.clear();
      this.$router.push({ name: "Login" });
    }
  },

  methods: {
    
    isMyArticle(id) {
      return this.iam === id;
    },
    isMyArticle(name) {
      return this.name === name;
    },
    
    async postArticle() {
      if (this.isCallingApi) {
        return;
      }
      this.isCallingApi = true;

      const reqBody = {
        userId: this.iam,            
        name: this.name,                
        text: this.post.text,         
        category: this.post.category,
      };
      try {
        /* global fetch */
        const res = await fetch(baseUrl + "/article", {
          method: "POST",
          body: JSON.stringify(reqBody),
          headers,
        });

        const text = await res.text();
        const jsonData = text ? JSON.parse(text) : {};

        // fetchではネットワークエラー以外のエラーはthrowされないため、明示的にthrowする
        if (!res.ok) {
          const errorMessage =
            jsonData.message ?? "エラーメッセージがありません";
          throw new Error(errorMessage);
        }
        
        console.log("投稿成功:", jsonData);
        this.post.text = "";
        this.post.category = "";
        console.log(jsonData);
      } catch (e) {
        console.log("error");
      }
    },
    
    async getArticles() {
      this.isCallingApi = true;

      try {
        /* global fetch */
        const res = await fetch(baseUrl + "/article", {
          method: "GET",
          // mode: 'cors',
          // credentials: true,
          headers,
        });

        const jsonData = await res.json();

        if (!res.ok) {
          const errorMessage = jsonData.message ?? "エラーメッセージがありません";
          throw new Error(errorMessage);
        }

        this.articles = jsonData.articles ?? [];
      } catch (e) {
        console.error(e);
        this.errorMsg = `記事一覧取得時にエラーが発生しました: ${e}`;
      } finally {
        this.isCallingApi = false;
      }
    },

    async toggleLike(article) {
      article.likepost = article.likepost === 1 ? 0 : 1;

      try {
        const res = await fetch(`${baseUrl}/like`, {
          method: "POST",
          body: JSON.stringify({ userId: this.iam, articleId: article.id, like: article.likepost === 1 }),
          headers,
        });

        // 成功時の処理をここに書く
      } catch (e) {
        console.error(e);
      }
    },

    convertToLocaleString(timestamp) {
      return new Date(timestamp).toLocaleString();
    },

    // 他のメソッドや計算プロパティはここに記述する
  },
};
</script>