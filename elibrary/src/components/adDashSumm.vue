<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-darkblue">
        <h4 class="navbar-brand" href="#">Summary of Books</h4>
        <div class="navbar" id="navbarNav">
            <ul class="navbar-nav">

                <li class="navbar-button">
                    <button type="navbar-button" class="btn btn-primary" @click="redirectToHome">Home</button>
                </li>

                <li class="navbar-button">
                    <button type="navbar-button" class="btn btn-primary" @click="Logout">Logout</button>
                </li>
            </ul>
        </div>
    </nav>
    <hr style="border: 1px solid #4169E1; ">

    <!-- Correct placement of the canvas element -->
    <div>
        <canvas ref="chart" ></canvas>
    </div>
</template>


  
  <script setup>
  import { ref, onMounted } from 'vue';
  import Chart from 'chart.js/auto';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  

  const router = useRouter();
  const chart = ref(null);
  
  onMounted(() => {
    const ctx = chart.value.getContext('2d');
  
    // Fetch data from the backend using Axios
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
  
         // Set up Axios with the token in the headers
        const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:5000', // Your API server's URL
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

        const url = "http://127.0.0.1:5000/book_request";
        const response = await axiosInstance.get(url);
        console.log(response.data.bookReq)
        renderChart(response.data.bookReq);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();
  
    const renderChart = (data) => {
      const sections = [];
      const booksPerSection = {};
  
      // Count the number of books per section
      data.forEach((book) => {
        if (!sections.includes(book.Section_Title)) {
          sections.push(book.Section_Title);
          booksPerSection[book.Section_Title] = 0;
        }
        booksPerSection[book.Section_Title]++;
      });
  
      // Create chart data
      const chartData = {
        labels: sections,
        datasets: [{
          label: 'Total Books Requested',
          data: sections.map((section) => booksPerSection[section]),
          backgroundColor: '#4169E1'
        }]
      };
  
      // Create and render the chart
      new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    };
  });
 


function redirectToHome() {
    router.push(`/adDash`)
}

function Logout() {
    localStorage.clear();
    router.push(`/loginPage/`)
}

// // onMounted(() => {
// //    chartData_func()
  
// });


</script>

<style  scoped>
.navbar {
    display: flex;
    /* Ensure items are in a row */
    justify-content: space-between;
    /* Push items to the ends of the container */
    align-items: center;
    /* Vertically center items if needed */
    text-align: center;
    padding: 10px;
    /* Add padding as needed */
    /* background-color: #333; Change background color if needed */
    color: #fff
        /*Change text color if needed */
}

.navbar-brand {
    text-align: center;
    /* Center-align the text within the navbar */
    flex-grow: 1;
    /* Allow the name to expand and take available space */
    margin: 0;
    /* Remove any default margin */
    /* font-family: 'Arial', sans-serif;  */
    font-size: 32px;
    font-weight: bold;
    color: #4169E1;
}

.navbar-button {
    margin-left: 10px;
    /* Add spacing between buttons */
    color: #166295;
    /* Additional button styles like background color, text color, etc. */
}
</style>