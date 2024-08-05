import { createRouter, createWebHistory } from 'vue-router';
import loginPage from './components/login_page.vue';
import registerPage from './components/register_page.vue';
import adDash from './components/adDash.vue';
import adDashSection from './components/admCrtSection.vue';
import adDashBook from './components/admCrtBook.vue';
import adDashReq from './components/adDashReq.vue';
import userDash from './components/userDash.vue';
import userReqBook from './components/userRequestBook.vue';
import editBook from './components/admEditBook.vue';
import editSection from './components/admEditSection.vue';
import welcomeView from './components/welcomeView.vue';
import userMyBooks from './components/userMyBooks.vue';
import userviewContent from './components/viewContent.vue';
import adDashSumm from './components/adDashSumm.vue';
import userFeedback from './components/userFeedback.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: welcomeView,
        },
        {
            path: '/loginPage',
            component: loginPage,
        },
        {
            path: '/RegisterPage',
            component: registerPage,
        },
        {
            path: '/adDash',
            component: adDash,
            meta:{requiresAuth:true},
        },
        {
            path: '/adDashSection',
            component: adDashSection,
        },
        {
            path: '/adDashBook',
            component: adDashBook,
        },
        {
            path: '/adDashReq',
            component: adDashReq,
        },
        {
            path: '/adDashSumm',
            component: adDashSumm,
        },
        {
            path: '/userDash',
            component: userDash,
            meta:{requiresAuth:true},
        },
        {
            path: '/userDash/:user_name',
            component: userDash,
            meta:{requiresAuth:true},
        },

        {
            path: '/userReqBook/',
            component: userReqBook,
        },
        {
            path: '/editBook',
            component: editBook,
        },
        {
            path: '/editSection',
            component: editSection,
        },
        
        {
            path: '/editSection/:venue_id',
            component: editSection,
          
        },
        {
            path: '/editBook/:show_id',
            component:editBook,
          
        },
        {
            path: '/userMyBooks',
            component:userMyBooks,
          
        },
        {
            path: '/viewContent/:book_title',
            component:userviewContent,
          
        },
        {
            path: '/userFeedback',
            component:userFeedback,
          
        },
        
    ],
});

export default router;