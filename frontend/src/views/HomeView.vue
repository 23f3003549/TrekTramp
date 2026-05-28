<template>

    <div class="container-fluid min-vh-100 bg-light p-0">

        <!-- Navbar -->

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">

            <a class="navbar-brand fw-bold" href="#">
                TrekTramp
            </a>

            <div class="ms-auto">

                <router-link
                    to="/login"
                    class="btn btn-outline-light me-2"
                >
                    Login
                </router-link>

                <router-link
                    to="/register"
                    class="btn btn-light"
                >
                    Register
                </router-link>

            </div>

        </nav>


        <!-- Hero Section -->

        <div class="d-flex flex-column justify-content-center align-items-center text-center"
             style="height: 80vh;">

            <h1 class="display-3 fw-bold mb-3">
                Welcome To TrekTramp
            </h1>

            <p class="lead mb-4">
                Explore amazing trekking experiences across India
            </p>

            <router-link
                to="/register"
                class="btn btn-dark btn-lg"
            >
                Get Started
            </router-link>

        </div>

    </div>

</template>

<script>

export default{
    name: "HomeView"
}

</script>