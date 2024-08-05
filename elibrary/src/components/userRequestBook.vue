<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-darkblue">
        <h4 class="navbar-brand" href="#"> {{Book_Title}}</h4>
        <h4 class="navbar-brand" href="#">Author : {{Book_Author}}</h4>
        <div class="navbar" id="navbarNav">
          <ul class="navbar-nav">
  
            <li class="navbar-button">
              <button type="navbar-button" class="btn btn-primary" @click="redirectToHome">Home</button>
            </li>
  
            <li class="navbar-button">
              <button type="navbar-button" class="btn btn-danger" @click="Logout">Logout</button>
            </li>
          </ul>
  
        </div>
      </nav>
  <hr style="border: 3px solid #4169E1;; ">
      <head>
        <meta charset="utf-8">
        <title> Book Request by User </title>
      </head>
  
      <body>
        <div class="wrapper">
          <div class="title">
            Request Book
          </div>
          <form action="#">
      
            <div class="field">
              <input type="text" required v-model="Ndays">
              <label>Number of days</label>
            </div>
  
            <div class="field">
              <input type="requestBook"  readonly  value="Request Book" @click="requestBook">
            </div>
  
          </form>
        </div>
      </body>
  
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import { useStore } from 'vuex';
  
  const store = useStore()
  const router = useRouter();

  
  const Ndays = ref("");
  const Book_Title = ref('')
  const Book_Author = ref('')
  const email=ref(store.getters.getemail)
  const user_name = ref(store.getters.getuser_name)
  console.log(email.value)
  function requestBook() {
  
  const url = "http://127.0.0.1:5000/book_request";
  const data = {
    Ndays: Ndays.value,
    user_name: store.getters.getuser_name,
    Book_Title: Book_Title.value,
    Section_Title: store.getters.getSection_Title_user,
    BookId:store.getters.getBook_ID,
    ReqStatus:'Requested',
    email:store.getters.getemail,
  
  };
  console.log(data);
  const data_sent_config = {
    headers: {
      'Content-Type': "application/json"
    },
  }
  const token = localStorage.getItem('token');
  
    // Set up Axios with the token in the headers
    const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:5000', // Your API server's URL
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
  
    axiosInstance.post(url, data, data_sent_config).then((res) => {
    console.log(res);
    alert(res.data.message)
    router.push(`/userDash/${user_name.value}`);
  }).catch((err) => {
    console.log(err);
  })
  }
  
  function redirectToHome(){
    router.push(`/userDash/${store.getters.getuser_name}`)
  }
  
  
  function Logout(){
    // Clear the entire local storage
    localStorage.clear();
    router.push(`/loginPage/`)
  }
  
  
  function BookDetailsForRequest() {
    let BookId = store.getters.getBook_ID;
    console.log(BookId)
    const url = `http://127.0.0.1:5000/user_book/${BookId}`;

    const token = localStorage.getItem('token');
    // Set up Axios with the token in the headers
    const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:5000', // Your API server's URL
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    try {
      axiosInstance.get(url).then((res) => {
        console.log(res)
        Book_Title.value = res.data.book.Book_Title
        Book_Author.value = res.data.book.Author
        
      })
    }
    catch (error) {
      console.error('Error fetching Data:', error);
    }
  }
  
  onMounted(() => { BookDetailsForRequest()})
  
  </script>
  
<style scoped>

  @import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap');
  
  /* * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
  } */
  
  html,
  body {
    display: grid;
    height: 100%;
    width: 100%;
    place-items: center;
    background: #ffffff;
    /* background: linear-gradient(-135deg, #c850c0, #4158d0); */
  }
  
  ::selection {
    background: #4158d0;
    color: #fff;
  }
  
  .wrapper {
    width: 500px;
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
    background-color: #4169E1;;
    /* background: linear-gradient(-135deg, #c850c0, #4158d0); */
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
    align-items: center;
    flex: 1;
  }
  
  .wrapper form .field:focus,
  form .field input:valid {
    border-color: #4158d0;
  }
  
  .wrapper form .field label {
    position: absolute;
    top: 0;
    left: 20px;
    color: #4158d0;
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
    text-align: center;
  }
  
  
  
  form .field input[type="requestBook"] {
    color: #fff;
    border: none;
    padding-left: 0;
    margin-top: -10px;
    font-size: 20px;
    font-weight: 500;
    /* cursor: pointer; */
    background: linear-gradient(-135deg, #c850c0, #4158d0);
    transition: all 0.3s ease;
    text-align: center;
  }
  
  form .field input[type="requestBook"]:active {
    transform: scale(0.95);
  }
  
  form .pass-link a:hover,
  form .signup-link a:hover {
    text-decoration: underline;
  }
  .navbar {
      display: flex; /* Ensure items are in a row */
      justify-content: space-between; /* Push items to the ends of the container */
      align-items: center; /* Vertically center items if needed */
      text-align: center;
      padding: 10px; /* Add padding as needed */
      /* background-color: #333; Change background color if needed */
      color: #fff /*Change text color if needed */
    }
  .navbar-brand {
    text-align: center; /* Center-align the text within the navbar */
    flex-grow: 1; /* Allow the name to expand and take available space */
    margin: 0; /* Remove any default margin */
    /* font-family: 'Arial', sans-serif;  */
    font-size: 32px; 
    font-weight: bold;
    color: #4169E1;
  }
  .navbar-button {
    margin-left: 10px; /* Add spacing between buttons */
    color: #166295;
    /* Additional button styles like background color, text color, etc. */
  }
  </style>