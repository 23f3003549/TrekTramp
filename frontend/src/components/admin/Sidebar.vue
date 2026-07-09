<template>
    <aside class="sidebar">

        <div class="logo">
            <h3>TrekTramp</h3>
        </div>

        <nav class="nav flex-column">

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
    width:250px;
    height:100vh;
    background:#1f2937;
    color:white;
    display:flex;
    flex-direction:column;
    padding:20px;
}

.logo{
    margin-bottom:30px;
}

.logo h3{
    font-weight:bold;
}

.nav-link{
    color:white;
    margin-bottom:10px;
    border-radius:8px;
    padding:10px;
    text-decoration:none;
}

.nav-link:hover{
    background:#2f855a;
    color:white;
}

.nav-link.active{

    background:#198754;

    color:white;

    border-radius:8px;

}

.router-link-active{
    background:#2f855a;
    color:white !important;
}

.logout{
    margin-top:auto;
}

</style>