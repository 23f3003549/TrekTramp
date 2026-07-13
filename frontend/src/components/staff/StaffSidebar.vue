<template>

<div class="sidebar d-flex flex-column">

    <!-- Logo -->
     <h6 class="mt-2 mb-0">

    {{ staffName }}

</h6>

<small class="text-light">

    Trek Staff

</small>

    <div class="logo-section">

        <h3 class="logo">

            🥾 TrekTramp

        </h3>

        <small class="text-light">

            Staff Panel

        </small>

    </div>

    <!-- Navigation -->

    <ul class="nav flex-column mt-4 flex-grow-1">

        <li class="nav-item">

            <router-link
                to="/staff/dashboard"
                class="nav-link"
                active-class="active-link"
            >

                <i class="bi bi-grid-fill me-2"></i>

                Dashboard

            </router-link>

        </li>

        <li class="nav-item">

            <router-link
                to="/staff/my-treks"
                class="nav-link"
                active-class="active-link"
            >

                <i class="bi bi-map-fill me-2"></i>

                My Treks

            </router-link>

        </li>

        <li class="nav-item">

            <router-link
                to="/staff/participants"
                class="nav-link"
                active-class="active-link"
            >

                <i class="bi bi-people-fill me-2"></i>

                Participants

            </router-link>

        </li>

        <!-- <li class="nav-item">

            <router-link
                to="/staff/profile"
                class="nav-link"
                active-class="active-link"
            >

                <i class="bi bi-person-circle me-2"></i>

                Profile

            </router-link>

        </li> -->

    </ul>

    <!-- Logout -->

    <div class="logout-section">

        <button
            class="btn btn-danger w-100"
            @click="logout"
        >

            <i class="bi bi-box-arrow-right me-2"></i>

            Logout

        </button>

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

.logout-section{

    margin-top:auto;

    padding-top:20px;

    border-top:1px solid rgba(255,255,255,.25);

}

.btn{

    border-radius:10px;

}

</style>