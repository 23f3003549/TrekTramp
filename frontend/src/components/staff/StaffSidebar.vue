<template>

<div class="sidebar d-flex flex-column">

    <div class="logo-section">

        <h3 class="logo">

            🥾 TrekTramp

        </h3>

    </div>


    <ul class="nav flex-column mt-4 flex-grow-1">

        <li class="nav-item">

            <router-link
                to="/staff/dashboard"
                class="nav-link"
                active-class="active-link"
            >

                Dashboard

            </router-link>

        </li>

        <li class="nav-item">

            <router-link
                to="/staff/my-treks"
                class="nav-link"
                active-class="active-link"
            >

                My Treks

            </router-link>

        </li>

        <li class="nav-item">

            <router-link
                to="/staff/participants"
                class="nav-link"
                active-class="active-link"
            >
                Participants

            </router-link>

        </li>

    </ul>

    <div class="logout mt-auto">

            <RouterLink to="/" class="nav-link">
                <i class="bi bi-box-arrow-right me-2"></i>
                Logout
            </RouterLink>

        </div>

</div>

</template>

<script>

export default{

    name:"StaffSidebar",
    data(){

    return{

        staffName: localStorage.getItem("name")

    }

},

    methods:{

        logout(){

            localStorage.removeItem("access_token");

            localStorage.removeItem("refresh_token");

            localStorage.removeItem("role");

            this.$router.push("/login");

        }

    }

}

</script>

<style scoped>

.sidebar{

    width:260px;

    min-height:100vh;

    background:#198754;

    color:white;

    position:fixed;

    left:0;

    top:0;

    padding:20px;

    box-shadow:2px 0 12px rgba(0,0,0,.15);

}



.logo-section{

    text-align:center;

    padding-bottom:20px;

    border-bottom:1px solid rgba(255,255,255,.25);

}

.logo{

    font-weight:700;

    margin-bottom:5px;

}

.nav-link{

    color:white;

    margin-bottom:10px;

    border-radius:10px;

    padding:12px 15px;

    transition:.3s;

}

.nav-link:hover{

    background:rgba(255,255,255,.18);

    color:white;

}

.active-link{

    background:white;

    color:#198754 !important;

    font-weight:600;

}


.btn{
    color: white;
    border-radius:10px;

}
.logout{
    text-align: center;
    margin-top:auto;

    padding-top:20px;

    border-top:1px solid rgba(255,255,255,.25);

}

</style>