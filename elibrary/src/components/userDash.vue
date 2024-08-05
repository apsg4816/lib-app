<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-darkblue">
      <img :src="require('@/assets/open_book.png')" style="width: 120px; height: 30x;" alt="Image Description" />
      <h4 class="navbar-brand" href="#">{{ First_Name }}'s Dashboard</h4>
      <div class="navbar" id="navbarNav">
        <ul class="navbar-nav">
          <div class="input-group mb-3">
            <!-- Dropdown -->
  
            <div class="input-group-prepend">
              <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-haspopup="true" aria-expanded="false">
                Filter
              </button>
              <div class="dropdown-menu">
                <a class="dropdown-item" @click="setFilter('Section')" href="#">Section</a>
                <a class="dropdown-item" @click="setFilter('Book')" href="#">Book</a>
  
              </div>
            </div>
  
            <!-- Input Field -->
            <input type="text" v-model="keyword" class="form-control" placeholder="Search..." aria-label="Search input"
              aria-describedby="basic-addon2">
  
            <!-- Search Button -->
            <div>
              <div v-if="is_Searching==true" class="input-group-append">
                <button @click="search(keyword)" class="btn btn-danger" type="button">Cancel Search</button>
              </div>
              <div v-else class="input-group-append">
                <button @click="search(keyword)" class="btn btn-primary" type="button">Search</button>
              </div>
            </div>
          </div>
  
          <li class="navbar-button">
            <button type="navbar-button" class="btn btn-info" @click="MyBooks">MyBooks</button>
          </li>
  
          <li class="navbar-button">
            <button type="navbar-button" class="btn btn-danger" @click="Logout">Logout</button>
          </li>
        </ul>
  
      </div>
    </nav>
  
  
    <!-- Card for Section and Books -->
    <div v-if="noSectionsFound">No sections found.</div>
    <div v-else>
      <div class="card" v-for="section in items_sections" :key="section.Section_Title">
        <div class="card-body">
          <h4 class="d-flex justify-content-between align-items-center"
            style="font-size: 2em; font-weight: bold; color: #4169E1;">{{ section.Section_Title}}</h4>
          <h5>Created on: {{ section.DateCreated}} ||
            Description: {{ section.Description }}
          </h5>
  
          <div v-if="noBooksFound">No Books found.</div>
          <div v-else>
            <div v-for="book in items_books" :key="book.Book_Title" v-show="section.Section_Title == book.ForSection"
              style="display: inline-block; margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #6A5ACD;">
              <div class="card" v-if="section.Section_Title == book.ForSection">
                <div class="card-body" >
                  <h5 class="show-brand" style="text-align: center; color: #4169E1;">{{ book.Book_Title }}</h5>
                  <h5 class="card-title">Author: {{ book.Author }}</h5>
  
                  <div v-if= "haveStatus(book.id)" >
                    <button style="margin-right: 10px;" class="btn btn-primary">{{ getStatus(book.id) }}</button>
                  </div>
                  <div v-else-if="userRequestedBook < 5">
                    <button style="margin-right: 10px;" class="btn btn-info"
                      @click="RequestBook(book.id, book.ForSection)">Request Book</button>
                  </div>
                  <div v-else>
                    <button style="margin-right: 10px;" class="btn btn-info"
                      >Maxm. Request Exceeded</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
        </div>
      </div>
    </div>
  </template>
      
    <script setup>
    import { useRouter } from 'vue-router';
    import axios from 'axios';
    import { ref, onMounted,computed } from 'vue';
    import { useStore } from 'vuex';
    
    const store = useStore();
    const router = useRouter();
    
    const items_sections = ref([]);
    const items_books= ref([]);
    const noSectionsFound= ref('');
    const noBooksFound= ref('');
    let is_Searching= false;
    // const user_name = ref(store.getters.getuser_name)
    const First_Name = ref('')
    // const buttonNotShown= ref(true)
  
    const url1 = "http://127.0.0.1:5000/admin_section";
    const url2 = "http://127.0.0.1:5000/admin_book";
    const url3 = "http://127.0.0.1:5000/section_book_search";
  
    let keyword = ref('');
    let selectedFilter = '';
  
  
    const setFilter = (filterBy) => {
    selectedFilter = filterBy;
  };
  
  
  function haveStatus(bookId){
      const requested = sortedItemsRequestedBook.value.find(request => request.BookId == bookId && (request.ReqStatus === "Requested" || request.ReqStatus === "Approved"));
    
      return requested ?1:0 ;
    
  }
  
  function getStatus(bookId)  {
    
      const requested=sortedItemsRequestedBook.value.find(request => request.BookId == bookId);
      return requested ? requested.ReqStatus : 'RequestBook';  
  }
  
  function search(keyword){
      is_Searching=!is_Searching;
      if(is_Searching== true){
          const token = localStorage.getItem('token');
          const axiosInstance = axios.create({
          baseURL: 'http://127.0.0.1:5000',
          headers: {
              'Authorization': `Bearer ${token}`
          }
          });
          axiosInstance.get(`${url3}/${keyword}`).then(response => {
              console.log(keyword)
              console.log(selectedFilter)
              console.log(response.data[0].sections)
              console.log(response.data[1].books)
              const searched_sections=response.data[0].sections;
              const searched_books=response.data[1].sections;
  
          if (selectedFilter === 'Section') {
          items_sections.value = response.data[0].sections;
          if (searched_sections.length === 0) {
              // Update flag variable to indicate no sections found
              noSectionsFound.value = true;
          } else {
              noSectionsFound.value = false;
          }
          } else if (selectedFilter === 'Book') {
          items_books.value = response.data[1].books;
          if (searched_books.length === 0) {
              // Update flag variable to indicate no books found
              noBooksFound.value = true;
          } else {
              noBooksFound.value = false;
          }
          } else {
          // When no filter is selected, update both items_sections and items_books
          items_sections.value = response.data[0].sections;
          items_books.value = response.data[1].books;
          }
      }).catch(error => {
          console.error(error);
      });}else {window.location.reload();
  }
  }
  
  function MyBooks() {
      router.push('/userMyBooks')
  }
  function Logout() {
      // Clear the entire local storage
      localStorage.clear();
      router.push('/loginPage')
  }
  function RequestBook(id,section){
    store.commit('setforBookID', id);
    store.commit('setforSection_Title', section);
    router.push('/userReqBook')
  }
   
  function bookStatus(){
    const url = `http://127.0.0.1:5000/book_request`;
  
  const token = localStorage.getItem('token');
  // Set up Axios with the token in the headers
  const axiosInstance = axios.create({
      baseURL: 'http://127.0.0.1:5000',
      headers: {
          'Authorization': `Bearer ${token}`
      }
  });
  try {
    axiosInstance.get(url).then((res) => {
      console.log(res.data.bookReq)
      items_requested_book.value=res.data.bookReq
      console.log(items_requested_book.value)
    })
  }
  catch (error) {
    console.error('Error fetching Data:', error);
  }
  }
  
  const user_name = ref('')
  
  const items_requested_book = ref([]);
  
  
  // computed property to sort the items_requested_book array
  const sortedItemsRequestedBook = computed(() => {
      const requested = [];
      const approved = [];
      const returned= [];
      const rejected = [];
      
      items_requested_book.value.forEach(request => {
          if (request.user_name === user_name.value) {
              if (request.ReqStatus === 'Requested') {
                  requested.push(request);
              } else if(request.ReqStatus === 'Approved') {
                  approved.push(request);
              } else if(request.ReqStatus === 'Rejected') {
                  rejected.push(request);
              } else if(request.ReqStatus === 'Returned') {
                  returned.push(request);
              }
          }
      });
        
      return [...requested, ...approved, ...rejected, ...returned];
  });
  
  
  const userRequestedBook = computed(() => {
      const requested = [];
  
      items_requested_book.value.forEach(request => {
          if (request.user_name === user_name.value && request.ReqStatus === 'Requested') {
              requested.push(request);
          }
      });
  
      return requested.length;
  });
  
    const fetchData = () => {
      // For first name from local storage
      const storedData1 = localStorage.getItem('First_Name');
      if (storedData1) {
          First_Name.value = JSON.parse(storedData1);
      }
      else{ router.push('/loginPage')}
       // For user name from local storage
      const storedData2 = localStorage.getItem('user_name');
      if (storedData2) {
          user_name.value = JSON.parse(storedData2);
      }else{ router.push('/loginPage')}
  
      const token = localStorage.getItem('token');
      const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:5000',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
        axiosInstance.get(url1)
        .then(response => {
          
          items_sections.value = response.data.sections;
          if (response.data.sections.length === 0) {
          // Update flag variable to indicate no sections found
          noSectionsFound.value = true;
        } else {
          noSectionsFound.value = false;
        }
        })
        .catch(error => {
          console.log(error);
        });
  
        axiosInstance.get(url2)
        .then(response => {
          items_books.value = response.data.books;
          if (response.data.books.length === 0) {
          // Update flag variable to indicate no books found
          noBooksFound.value = true;
        } else {
          noBooksFound.value = false;
        }
        })
        .catch(error => {
          console.log(error);
          router.push('/loginPage');
        });
    };
  
    onMounted(() => {fetchData(),bookStatus(),console.log(sortedItemsRequestedBook.value)});
    
    </script>
    
  
  

    <style scoped>
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 10px;
      color: #fff;
    }
    .navbar-brand {
      text-align: center;
      flex-grow: 1;
      margin: 0;
      font-size: 36px;
      font-weight: bold;
      color: #4169E1;
    }
    .navbar-button {
      margin-left: 10px;
      color: #166295;
    }
    .show-style {
      display: inline-block;
      margin: 10px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      background-color: #f9f9f9;
    }
    </style>
    