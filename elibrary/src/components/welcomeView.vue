<template>
  <div class="container">
    <div class="upper-half">
      <img :src="require('@/assets/library.png')" style="width: 120px; height: 30x;" alt="Image Description" />
      <img :src="require('@/assets/ebook.png')" style="width: 120px; height: 30x;" alt="Image Description" />
      <img :src="require('@/assets/close_book.png')" style="width: 120px; height: 30x;" alt="Image Description" />
      <img :src="require('@/assets/open_book.png')" style="width: 120px; height: 30x;" alt="Image Description" />
      <h1 class="title">Library Management App</h1>
      <h2 class="subtitle">Get your Books just on a click</h2>
      <div class="buttons">
        <button class="login-button" @click="goToLogin">Login</button>
        <button class="register-button" @click="goToRegister">Register</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToLogin = () => {
  router.push('/loginPage') 
};

const goToRegister = () => {
  router.push('/registerPage'); 
};
</script>

<style scoped>
.container {
  text-align: center;
  background: linear-gradient( -135deg , rgb(165, 149, 164)0, #abadb4);
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.title {
  font-size: 36px;
  font-family: 'Comic Sans MS';
  color: #4169E1;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 24px;
  font-family: 'Comic Sans MS';
  color:#4169E1

}

.buttons {
  margin-top: 20px;
}

.login-button,
.register-button {
  font-size: 24px;
  padding: 10px 50px;
  margin: 0 20px;
  margin-bottom: 20px;
  border: none;
  border-radius: 20px;
  font-family: 'Comic Sans MS';
  cursor: pointer;
  background-color: #00bfff; /* Blue color */
  color: #fff; /* White text */
}

.register-button {
  background-color: #28a745; /* Green color */
}
</style>
