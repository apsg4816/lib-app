<template>
    <div v-if="book">
      <h1>{{ book.Book_Title }}</h1>
      <p><strong>Author:</strong> {{ book.Author }}</p>
      <div v-html="book.Content"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  
  // Define a ref to hold the book data
  const book = ref(null);
  
  // Get the route object using useRoute
  const route = useRoute();
  
  // Extract the book title from the route params
  const bookTitle = route.params.book_title;
  
  // Fetch the book data from the backend when the component is mounted
  onMounted(async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/user_book/${bookTitle}`);
      console.log(response)
      book.value = response.data.book;

    } catch (error) {
      console.error('Error fetching book data:', error);
    }
  });
  </script>
  