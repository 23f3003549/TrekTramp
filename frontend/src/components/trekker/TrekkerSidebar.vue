<template>

<div
    class=" sidebar d-flex flex-column"
    style="width: 260px;"
>


    <div
        class=" logo-section "
    >

        <h4
            class=" logo "
        >

            🥾 TrekTramp

        </h4>

    </div>

    <div class="flex-grow-1">

        <ul class="nav flex-column p-3">

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/dashboard"
                    class="nav-link"
                    active-class="active-link"
                >

                    Dashboard

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/browse"
                    class="nav-link"
                    active-class="active-link"
                >

                    Browse Treks

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/my-treks"
                    class="nav-link"
                    active-class="active-link"
                >
                    My Treks

                </RouterLink>

            </li>

        </ul>

    </div>

    <div class="logout mt-auto">

            <RouterLink to="/" class="nav-link">
                <i class="bi bi-box-arrow-right me-2"></i>
                Logout
            </RouterLink>

        </div>

</div>

</template>

<script>

export default {

    name: "TrekkerSidebar",

    methods: {

        logout() {

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

button{

    border-radius:10px;

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
.logout{
    text-align: center;
    margin-top:auto;

    padding-top:20px;

    border-top:1px solid rgba(255,255,255,.25);

}

</style>