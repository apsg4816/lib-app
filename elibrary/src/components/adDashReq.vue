<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-darkblue">
        <h4 class="navbar-brand" href="#">Requests of Users for Books</h4>
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
    <div>
        <div>
            <div>
                <div style="margin-bottom: 20px;">
                    <hr style="border: 5px solid #4169E1;">
                    <div v-for="request in sortedItemsRequestedBook" :key="request.id"
                        style="margin-bottom: 20px; display: flex; align-items: center;">
                        <h5 style="font-weight: bold; color: #4169E1; flex:1;">
                            Section: {{ request.Section_Title }} &nbsp;|&nbsp;&nbsp;&nbsp; Book: {{ request.Book_Title
                            }} &nbsp;|&nbsp;&nbsp;&nbsp; User: {{ request.user_name }} &nbsp;|&nbsp;&nbsp;&nbsp; No. of
                            Days Requested: {{ request.Ndays }}
                        </h5>
                        <div v-if="request.ReqStatus === 'Requested'">
                            <button class="btn btn-warning" style="margin-right: 10px;"
                                @click="reqApprove(request.id)">Approve</button>
                            <button class="btn btn-danger" style="margin-right: 10px;"
                                @click="reqReject(request.id)">Reject</button>
                        </div>
                        <div v-else-if="request.ReqStatus === 'Approved'">
                            <button class="btn btn-success" style="margin-right: 10px;">Approved</button>
                            <button class="btn btn-danger" style="margin-right: 10px;"
                                @click="reqReject(request.id)">Reject</button>
                        </div>
                        <div v-else-if="request.ReqStatus === 'Returned'">
                            <button class="btn btn-info" style="margin-right: 10px;">Returned</button>
                        </div>
                        <div v-else>
                            <button class="btn btn-danger" style="margin-right: 10px;">{{ request.ReqStatus }}</button>
                        </div>
                    </div>
                    <hr style="border: 1px solid #4169E1;">
                </div>

            </div>

        </div>

    </div>

</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';
// import { useStore } from 'vuex';
import { useRouter } from 'vue-router';


const router = useRouter()

const items_requested_book = ref([]);

// Define your methods and other logic here

// Define computed property to sort the items_requested_book array
const sortedItemsRequestedBook = computed(() => {
    const requested = [];
    const approved = [];

    items_requested_book.value.forEach(request => {
        if (request.ReqStatus === 'Requested') {
            requested.push(request);
        } else {
            approved.push(request);
        }
    });

    return [...requested, ...approved];
});

function reqApprove(requestId) {
    if (window.confirm("Do you really want to approve this Request ?")) {
        const url = `http://127.0.0.1:5000/book_request/${requestId}`;
        const data = { 'ReqStatus': 'Approved' };
        const token = localStorage.getItem('token');

        // Set up Axios with the token in the headers
        const axiosInstance = axios.create({
            baseURL: 'http://127.0.0.1:5000',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        try {
            axiosInstance.patch(url, data).then((res) => {
                console.log(res);
                window.location.reload();
            });
        } catch (error) {
            console.error('Error fetching Data:', error);
        }
    } else { // Do Nothing
    }
}

function reqReject(requestId) {
    if (window.confirm("Do you really want to Reject this Request ?")) {
        const url = `http://127.0.0.1:5000/book_request/${requestId}`;
        const data = { 'ReqStatus': 'Rejected' };
        const token = localStorage.getItem('token');

        // Set up Axios with the token in the headers
        const axiosInstance = axios.create({
            baseURL: 'http://127.0.0.1:5000',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        try {
            axiosInstance.patch(url, data).then((res) => {
                console.log(res);
                window.location.reload();
            });
        } catch (error) {
            console.error('Error fetching Data:', error);
        }
    } else { // Do Nothing
    }
}

function fetchRequestedData() {

    const url = `http://127.0.0.1:5000/book_request`;

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
            items_requested_book.value = res.data.bookReq
        })
    }
    catch (error) {
        console.error('Error fetching Data:', error);
    }
}

function redirectToHome() {
    router.push(`/adDash`)
}

function Logout() {
    localStorage.clear();
    router.push(`/loginPage/`)
}

onMounted(() => {
    fetchRequestedData()

});


</script>

<style scoped>
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