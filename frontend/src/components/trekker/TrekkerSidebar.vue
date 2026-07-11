<template>

<div
    class="d-flex flex-column bg-white border-end shadow-sm vh-100"
    style="width: 260px;"
>

    <!-- Logo -->

    <div
        class="text-center py-4 border-bottom"
    >

        <h4
            class="fw-bold text-success mb-0"
        >

            TrekTramp

        </h4>

    </div>

    <!-- Navigation -->

    <div class="flex-grow-1">

        <ul class="nav flex-column p-3">

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/dashboard"
                    class="nav-link"
                    active-class="active-link"
                >

                    <i class="bi bi-speedometer2 me-2"></i>

                    Dashboard

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/browse"
                    class="nav-link"
                    active-class="active-link"
                >

                    <i class="bi bi-compass me-2"></i>

                    Browse Treks

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/bookings"
                    class="nav-link"
                    active-class="active-link"
                >

                    <i class="bi bi-calendar-check me-2"></i>

                    My Bookings

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/history"
                    class="nav-link"
                    active-class="active-link"
                >

                    <i class="bi bi-clock-history me-2"></i>

                    History

                </RouterLink>

            </li>

            <li class="nav-item mb-2">

                <RouterLink
                    to="/trekker/profile"
                    class="nav-link"
                    active-class="active-link"
                >

                    <i class="bi bi-person me-2"></i>

                    Profile

                </RouterLink>

            </li>

        </ul>

    </div>

    <!-- Logout -->

    <div
        class="border-top p-3"
    >

        <button
            class="btn btn-outline-danger w-100"
            @click="logout"
        >

            <i class="bi bi-box-arrow-right me-2"></i>

            Logout

        </button>

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

.nav-link{

    color:#495057;

    border-radius:10px;

    padding:12px 16px;

    transition:0.3s;

    font-weight:500;

}

.nav-link:hover{

    background:#e8f5e9;

    color:#198754;

}

.active-link{

    background:#198754;

    color:white !important;

}

button{

    border-radius:10px;

}

</style>