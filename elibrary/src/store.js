import { createStore } from 'vuex';

export default createStore({
  state: {
    Venue_id: 0,
    Show_id: 0,
    venue4show: '',
    bookForVenue: '',
    bookForShow: '',
    ven_name: '',
    Sprice: 0,
    Venue_capacity:0,
    TotalBooked:0,
    message:'',
    access_token:'',
    id:'',
    user_name:'',
    First_Name:'',
    Last_Name:'',
    favGenre:'',
    email:'',
    Vcapacity:'',
    AllShows:'',
    chartData1:'',

    Section_Title:'',
    Book_id:'',
    Book_ID:'',
    Section_id:'',
    Section_Title_user:'',
    isAuthenticated:false,
    bookid:'',
  },
  mutations: {
    setSectionId(state, id) {
      state.Section_id = id;
    },
    setBookId(state, id) {
      state.Book_id = id;
    },
    setSectionforBook(state, section) {
      state.Section_Title = section.Section_Title;
    },
    setforSection_Title(state, Section_Title) {
      state.Section_Title_user = Section_Title;
    },

    setforBookId_feed(state,bookid){
      state.bookid = bookid;
    },



    setBookforVenue_Name(state, v_name) {
      state.ven_name = v_name;
    },
    setBookforShow(state, s_id) {
      state.bookForShow = s_id;
    },
    setforBookID(state, id){
      state.Book_ID = id;
    },
    setVenue_capacity(state,Venue_capacity){
      state.Venue_capacity=Venue_capacity;
    },
    setTotalBooked(state,TotalBooked){
      state.TotalBooked=TotalBooked
    },
    setUserData(state,user_data){
      state.message=user_data.message;
      state.access_token=user_data.access_token,
      state.id=user_data.id,
      state.user_name=user_data.user_name,
      state.First_Name=user_data.First_Name,
      state.Last_Name=user_data.Last_Name,
      state.favGenre=user_data.favGenre,
      state.email=user_data.email
    },
    setAllShows(state,AllShows){
      state.AllShows=AllShows;
    },
    setchartdata(state,chartData1){
      state.chartData1=chartData1;
    },
    setisAuthenticated(state,isAuthenticated){
      state.isAuthenticated=isAuthenticated;
    },
  },

  getters: {
    getSection_id: (state) => state.Section_id,
    getBook_id: (state) => state.Book_id,
    getBook_ID: (state) => state.Book_ID,
    getSectionforBook: (state) => state.Section_Title,
    getSection_Title_user: (state) => state.Section_Title_user,
    getforBookId_feed:(state)=> state.bookid,
    
    getBookForShow: (state) => state.bookForShow,
    getV_name: (state) => state.ven_name,
    getBookID: (state) => state.Book,
    getVenue_capacity:(state)=> state.Venue_capacity,
    getTotalBooked:(state)=> state.TotalBooked,
    getemail:(state)=> state.email,
    getuser_name:(state)=>state.user_name,
    getid:(state)=>state.id,
    getFirst_Name:(state)=>state.First_Name,
    getLast_Name:(state)=>state.Last_Name,
    getfavGenre:(state)=>state.favGenre,
    getaccesstoken:(state)=>state.access_token,
    getVcapacity:(state)=>state.Vcapacity,
    getAllShows:(state)=>state.AllShows,
    getchartdata:(state)=> state.chartData1,
    getisAuthenticated:(state)=>state.isAuthenticated
  },
});

