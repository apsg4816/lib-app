<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-darkblue">
    <img :src="require('@/assets/library.png')" style="width: 120px; height: 30x;" alt="Image Description" />
    <h4 class="navbar-brand" href="#">Librarian's Dashboard</h4>
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
            <div v-if="is_Searching == true" class="input-group-append">
              <button @click="search(keyword)" class="btn btn-danger" type="button">Cancel Search</button>
            </div>
            <div v-else class="input-group-append">
              <button @click="search(keyword)" class="btn btn-primary" type="button">Search</button>
            </div>
          </div>
        </div>

        <li class="navbar-button">
          <button type="navbar-button" class="btn btn-primary" @click="redirectToRequests">Requests</button>
        </li>

        <li class="navbar-button">
          <button type="navbar-button" class="btn btn-danger" @click="Logout">Logout</button>
        </li>
      </ul>

    </div>
  </nav>


  <!-- Start Create Section card  -->
  <div class="card">
    <div class="card-body" style="text-align: center;">
      <button type="button" style="margin-right: 20px;" class="btn btn-primary" @click='redirectToAdDashSection'>Create
        Section</button>
      <button type="button" style="margin-right: 20px;" class="btn btn-primary" @click='exportLibraryData'>Export
        Library Data</button>
      <button type="button" style="margin-right: 20px;" class="btn btn-primary" @click='LibSummary'>Books
        Summary</button>
    </div>
  </div>
  <!--  End Create Section card -->


  <!-- Card for Section and Books -->
  <div v-if="noSectionsFound">No Sections and Books found.</div>
  <div v-else>
    <div class="card" v-for="section in items_sections" :key="section.Section_Title">
      <div class="card-body">
        <h4 class="d-flex justify-content-between align-items-center"
          style="font-size: 2em; font-weight: bold; color: #4169E1;">{{ section.Section_Title }}
          <div>
            <button style="margin-right: 10px;" class="btn btn-outline-info"
              @click="redirectToEditSection(section.id)">Edit Section</button>
            <button class="btn btn-outline-danger" @click="deleteSection(section.id)">Delete Section{{ section.id
              }}</button>
          </div>
        </h4>
        <h5>Created on: {{ section.DateCreated }} &&
          Description: {{ section.Description }}
        </h5>

        <div v-if="noBooksFound">No Books found.</div>
        <div v-else>
          <div v-for="book in items_books" :key="book.Book_Title" v-show="section.Section_Title == book.ForSection"
            style="display: inline-block; margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #6A5ACD;">
            <div class="card" v-if="section.Section_Title == book.ForSection">

              <div class="card-body">
                <h5 class="show-brand" style=" text-align: center; color: #4169E1;">{{ book.Book_Title }}</h5>
                <h5 class="card-title">Author: {{ book.Author }}</h5>
                <button style="margin-right: 10px;" class="btn btn-outline-info"
                  @click="redirectToEditBook(book.id)">Edit Book</button>
                <button style="margin-right: 10px;" class="btn btn-outline-danger" @click="deleteBook(book.id)">Delete
                  Book{{ book.id }}</button>
              </div>
            </div>
          </div>
        </div>

        <div class="card-body">
          <button type="button" class="btn btn-outline-primary" @click="AddBooks(section)">Add New Book for {{
      section.Section_Title }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const router = useRouter();

const items_sections = ref([]);
const items_books = ref([]);
const noSectionsFound = ref('');
const noBooksFound = ref('');
let is_Searching = false;

const url1 = "http://127.0.0.1:5000/admin_section";
const url2 = "http://127.0.0.1:5000/admin_book";
const url3 = "http://127.0.0.1:5000/section_book_search";

let keyword = ref('');
let selectedFilter = '';


const setFilter = (filterBy) => {
  selectedFilter = filterBy;
};

function search(keyword) {
  is_Searching = !is_Searching;
  if (is_Searching == true) {
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
      const searched_sections = response.data[0].sections;
      const searched_books = response.data[1].sections;

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
    });
  } else { window.location.reload(); }
}

function redirectToAdDashSection() {
  router.push('/adDashSection')
}

function AddBooks(section) {
  store.commit('setSectionforBook', section)
  router.push('/adDashBook')
}

function redirectToRequests() {
  router.push('/adDashReq')
}
function Logout() {
  // Clear the entire local storage
  localStorage.clear();
  router.push('/loginPage')
}

function redirectToEditBook(id) {
  store.commit('setBookId', id);

  router.push(`/editBook/${id}`)
}

function LibSummary() {

  router.push(`/adDashSumm`)
}

function redirectToEditSection(id) {
  store.commit('setSectionId', id);
  // const venue_id= venue.id
  // console.log(venue.id)
  router.push(`/editSection/${id}`)
}

function deleteSection(id) {
  if (window.confirm("Do you really want to delete this Section?")) {
    const token = localStorage.getItem('token');
    const axiosInstance = axios.create({
      baseURL: 'http://127.0.0.1:5000',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    axiosInstance.delete(`${url1}/${id}`).then(() => {
      // console.log(res);
      // console.log(items_sections);
      window.location.reload();
    }).catch((err) => {
      console.log(err);
    });
  } else {
    // Do nothing if the user cancels the confirmation
  }
}

function deleteBook(id) {
  if (window.confirm("Do you really want to delete this Book?")) {
    const token = localStorage.getItem('token');
    const axiosInstance = axios.create({
      baseURL: 'http://127.0.0.1:5000',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    axiosInstance.delete(`${url2}/${id}`).then((res) => {
      console.log(res);
      console.log(items_books);
      window.location.reload();
    }).catch((err) => {
      console.log(err);
    });
  } else {
    // Do nothing if the user cancels the confirmation
  }
}

function exportLibraryData() {
  if (window.confirm("Do you really want to export books data?")) {
    const token = localStorage.getItem('token');
    const axiosInstance = axios.create({
      baseURL: 'http://127.0.0.1:5000',
      headers: { 'Authorization': `Bearer ${token}` },
      responseType: 'blob',
    });

    axiosInstance.get('/export_book_data')
      .then(response => {
        console.log(response)
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(response.data);
        downloadLink.download = 'books_available.csv';

        document.body.appendChild(downloadLink)
        downloadLink.click();
      })
      .catch(error => {
        console.log(error)

      });
  }

}

const fetchData = () => {
  const token = localStorage.getItem('token');
  const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  axiosInstance.get('http://127.0.0.1:5000/admin_section')
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
  axiosInstance.get('http://127.0.0.1:5000/admin_book')
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
    });
};

onMounted(() => {
  fetchData();
});

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