<template>

    <header class="top-navbar">
        <div>

            <h4 class="mb-0 fw-bold" style="color: grey;">
                Hello Admin
            </h4>

        </div>


        <div class="search-box">

            <i class="bi bi-search search-icon"
               @click="searchData"></i>

            <input
                type="text"
                class="form-control"
                :placeholder="placeholder"
                :disabled="!searchEnabled"
                v-model="search"
                @input="debouncedSearch"
            />

        </div>
        <div
            class="profile-avatar"
            @click="showProfile=true"
        >

            {{ initials }}

        </div>

        <AdminProfilePanel

            v-if="showProfile"

            @close="showProfile=false"

        />

    </header>

</template>

<script>

import AdminProfilePanel from "./AdminProfilePanel.vue";

import{

    getAdminProfile

}from "../../services/admin";

export default{

    name:"TopNavbar",

    components:{

        AdminProfilePanel

    },

    data(){

        return{
            search:"",

            searchTimer:null,

            showProfile:false,

            admin:{

                name:"",

                email:"",

                role:""

            }

        }

    },

    props:{

        placeholder:{
    
            type:String,
    
            default:"Search..."
    
        },
    
        searchEnabled:{
    
            type:Boolean,
    
            default:true
    
        }

    },

    computed:{

        initials(){

            if(!this.admin.name){

                return "A";

            }

            return this.admin.name

                .split(" ")

                .map(

                    word=>word.charAt(0)

                )

                .join("")

                .substring(0,2)

                .toUpperCase();

        }

    },

    methods:{

        async loadProfile(){

            try{

                const response = await getAdminProfile();

                this.admin = response.data.admin;

            }

            catch(error){

                console.error(error);

                alert(

                    error.response?.data?.message ||

                    "Unable to load admin profile."

                );

            }

        },
        debouncedSearch(){

            clearTimeout(this.searchTimer);
    
            this.searchTimer = setTimeout(()=>{
    
                this.searchData();
    
            },300);

        },
        searchData(){

            this.$emit(
        
                "search",
        
                this.search.trim()
        
            );
        
        },        

        logout(){

            localStorage.clear();

            this.$router.push("/login");

        }

    },

    mounted(){

        this.loadProfile();

    }

}

</script>

<style scoped>

.top-navbar{

    height:70px;

    background:white;

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:0 25px;

    border-bottom:1px solid #dee2e6;

}

h4{

    color:#212529;

    font-weight:700;

    margin:0;

}
.search-box{

    width:420px;

    position:relative;

}

.search-box input{

    border-radius:30px;

    padding-left:45px;

    height:42px;

    border:1px solid #ced4da;

}

.search-box input:focus{

    border-color:#198754;

    box-shadow:0 0 0 .15rem rgba(25,135,84,.2);

}

.search-icon{

    position:absolute;

    top:13px;

    left:18px;

    color:#6c757d;

    font-size:15px;
    cursor:pointer;

}
.profile-avatar{

    width:46px;

    height:46px;

    border-radius:50%;

    background:#198754;

    color:white;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:18px;

    font-weight:700;

    cursor:pointer;

    user-select:none;

    transition:.25s;

}

.profile-avatar:hover{

    background:#157347;

    transform:scale(1.05);

    box-shadow:0 4px 12px rgba(25,135,84,.3);

}

@media(max-width:992px){

    .search-box{

        width:280px;

    }

}

@media(max-width:768px){

    .top-navbar{

        padding:0 15px;

    }

    .search-box{

        display:none;

    }

}

</style>