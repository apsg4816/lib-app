<template>
    <div>
      <html lang="en" dir="ltr">
  
      <head>
        <meta charset="utf-8">
        <title>Add Book </title>
      </head>
  
      <body>
        <div class="wrapper">
          <div class="title">
            Book Entry
          </div>
          <form action="#">
            <div class="field">
              <input type="text" required v-model="Book_Title">
              <label>Book Tittle</label>
            </div>
  
            <div class="field">
              <input type="text" required v-model="Author">
              <label>Author</label>
            </div>
  
            <div class="field">
              <input type="text" required v-model="Content">
              <label>Content</label>
            </div>
  
            <div class="field">
              <input type="addbook" readonly value="Add Book" @click="addBook">
            </div>
  
  
          </form>
        </div>
      </body>
  
      </html>
  
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { ref } from 'vue';
  import axios from 'axios';
  import { useStore } from 'vuex';
  
  const router = useRouter();
  const store = useStore();
  
  const ForSection = store.getters.getSectionforBook;
  console.log(ForSection)
  const Book_Title = ref("");
  const Author = ref('');
  const Content = ref("");
  
  
  function addBook() {
  
    const data = {
      ForSection: ForSection,
      Book_Title: Book_Title.value,
      Author: Author.value,
      Content:Content.value
  
    };
  
    const data_sent_config = {
      headers: {
        'Content-Type': "application/json"
      },
    }
  
    const token = localStorage.getItem('token');
  
      // Set up Axios with the token in the headers
      const axiosInstance = axios.create({
          baseURL: 'http://127.0.0.1:5000',
          headers: {
              'Authorization': `Bearer ${token}`
          }
      });
  
      // Use axiosInstance for making requests
      axiosInstance.post('/admin_book',data, data_sent_config)
          .then(response => {
              alert(response.data.message)
              console.log(response)
              router.push('/adDash');
          })
          .catch(error => {
              console.log(error)
              alert(error.response.data.message)
          });
  }


</script>
  <style scoped>
  @import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap');
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
  }
  
  html,
  body {
    display: grid;
    height: 100%;
    width: 100%;
    place-items: center;
    background: #f2f2f2;
    /* background: linear-gradient(-135deg, #c850c0, #4158d0); */
  }
  
  ::selection {
    background: #4158d0;
    color: #fff;
  }
  
  .wrapper {
    width: 380px;
    background: #fff;
    border-radius: 15px;
    box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.1);
  }
  
  .wrapper .title {
    font-size: 35px;
    font-weight: 600;
    text-align: center;
    line-height: 100px;
    color: #fff;
    user-select: none;
    border-radius: 15px 15px 0 0;
    background: linear-gradient(-135deg, #c850c0, #4158d0);
  }
  
  .wrapper form {
    padding: 10px 30px 50px 30px;
  }
  
  .wrapper form .field {
    height: 50px;
    width: 100%;
    margin-top: 20px;
    position: relative;
  }
  
  .wrapper form .field input {
    height: 100%;
    width: 100%;
    outline: none;
    font-size: 17px;
    padding-left: 20px;
    border: 1px solid lightgrey;
    border-radius: 25px;
    transition: all 0.3s ease;
  }
  
  .wrapper form .field input:focus,
  form .field input:valid {
    border-color: #4158d0;
  }
  
  .wrapper form .field label {
    position: absolute;
    top: 50%;
    left: 20px;
    color: #999999;
    font-weight: 400;
    font-size: 17px;
    pointer-events: none;
    transform: translateY(-50%);
    transition: all 0.3s ease;
  }
  
  form .field input:focus~label,
  form .field input:valid~label {
    top: 0%;
    font-size: 16px;
    color: #4158d0;
    background: #fff;
    transform: translateY(-50%);
  }
  
  form .content {
    display: flex;
    width: 100%;
    height: 50px;
    font-size: 16px;
    align-items: center;
    justify-content: space-around;
  }
  
  form .content .checkbox {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  form .content input {
    width: 15px;
    height: 15px;
    background: red;
  }
  
  form .content label {
    color: #262626;
    user-select: none;
    padding-left: 5px;
  }
  
  form .content .pass-link {
    color: "";
  }
  
  form .field input[type="addBook"] {
    color: #fff;
    border: none;
    padding-left: 0;
    margin-top: -10px;
    font-size: 20px;
    font-weight: 500;
    cursor: pointer;
    background: linear-gradient(-135deg, #c850c0, #4158d0);
    transition: all 0.3s ease;
    text-align: center;
  }
  
  form .field input[type="addBook"]:active {
    transform: scale(0.95);
  }
  
  form .signup-link {
    color: #262626;
    margin-top: 20px;
    text-align: center;
  }
  
  form .pass-link a,
  form .signup-link a {
    color: #4158d0;
    text-decoration: none;
  }
  
  form .pass-link a:hover,
  form .signup-link a:hover {
    text-decoration: underline;
  }</style>