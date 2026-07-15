<template>
    <aside class="sidebar d-flex flex-column">

        <div class="logo-section">
            <h3 class="logo">🥾 TrekTramp</h3>
        </div>

        <nav class="nav flex-column mt-4 flex-grow-1 ">

            <RouterLink to="/admin" class="nav-link" active-class="active">
                Dashboard
            </RouterLink>

            <RouterLink to="/admin/treks" class="nav-link" active-class="active">
                Manage Treks
            </RouterLink>

            <RouterLink to="/admin/staff" class="nav-link" active-class="active">
                Manage Staff
            </RouterLink>

            <RouterLink to="/admin/users" class="nav-link" active-class="active">
                Users
            </RouterLink>

            <RouterLink to="/admin/bookings" class="nav-link" active-class="active">
                Bookings
            </RouterLink>

            <RouterLink to="/admin/reports" class="nav-link" active-class="active">
                Reports
            </RouterLink>

        </nav>

        <div class="logout mt-auto">

            <RouterLink to="/" class="nav-link">
                <i class="bi bi-box-arrow-right me-2"></i>
                Logout
            </RouterLink>

        </div>

    </aside>
</template>

<script>

import { RouterLink } from "vue-router"

export default {
    name: "Sidebar",
    components: {
        RouterLink
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

.nav-link.active{

    background:white;

    color:#198754 !important;

    font-weight:600;


}

.router-link-active{
    background:#2f855a;
    color:white !important;
}

.logout{
    text-align: center;
    margin-top:auto;

    padding-top:20px;

    border-top:1px solid rgba(255,255,255,.25);

}

</style>