<template>

<div class="container-fluid p-0 bg-light">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow">

        <a class="navbar-brand fw-bold fs-3">
            🥾 TrekTramp
        </a>

        <div class="ms-auto">

            <RouterLink
                to="/login"
                class="btn btn-outline-light me-2"
            >
                Login
            </RouterLink>

            <RouterLink
                to="/register"
                class="btn btn-success"
            >
                Register
            </RouterLink>

        </div>

    </nav>

    <section class="hero">

        <div class="container text-center">

            <h1 class="display-4 fw-bold">

                Discover Amazing Trekking Adventures

            </h1>

            <p class="lead mt-3">

                Plan, book, and manage trekking experiences with an easy-to-use
                trekking management platform.

            </p>

            <RouterLink
                to="/register"
                class="btn btn-success btn-lg mt-3 px-4"
            >
                Get Started
            </RouterLink>

        </div>

    </section>

    <section class="container py-5">

        <h2 class="text-center fw-bold mb-5">

            Why TrekTramp?

        </h2>

        <div class="row g-4">

            <div class="col-md-4">

                <div class="card h-100 shadow-sm feature-card">

                    <div class="card-body text-center">

                        <i class="bi bi-compass display-4 text-success"></i>

                        <h4 class="mt-3">

                            Browse Treks

                        </h4>

                        <p>

                            Explore trekking destinations based on location,
                            difficulty level, duration and availability.

                        </p>

                    </div>

                </div>

            </div>

            <div class="col-md-4">

                <div class="card h-100 shadow-sm feature-card">

                    <div class="card-body text-center">

                        <i class="bi bi-calendar-check display-4 text-success"></i>

                        <h4 class="mt-3">

                            Easy Booking

                        </h4>

                        <p>

                            Book treks securely, manage payments, reviews and
                            booking history in one place.

                        </p>

                    </div>

                </div>

            </div>

            <div class="col-md-4">

                <div class="card h-100 shadow-sm feature-card">

                    <div class="card-body text-center">

                        <i class="bi bi-people display-4 text-success"></i>

                        <h4 class="mt-3">

                            Efficient Management

                        </h4>

                        <p>

                            Dedicated dashboards for administrators, staff and
                            trekkers with role-based access.

                        </p>

                    </div>

                </div>

            </div>

        </div>

    </section>

    <section class="bg-success text-white py-5">

        <div class="container">

            <div class="row text-center">

                <div class="col-md-4">

                    <h2 class="fw-bold">

                        100+

                    </h2>

                    <p>

                        Treks Managed

                    </p>

                </div>

                <div class="col-md-4">

                    <h2 class="fw-bold">

                        50+

                    </h2>

                    <p>

                        Staff Members

                    </p>

                </div>

                <div class="col-md-4">

                    <h2 class="fw-bold">

                        1000+

                    </h2>

                    <p>

                        Happy Trekkers

                    </p>

                </div>

            </div>

        </div>

    </section>

    <footer class="bg-dark text-white text-center py-3">

        © 2026 TrekTramp | Trekking Management Application

    </footer>

</div>

</template>

<style scoped>

.hero{

    background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.55)),
    url("/image/treks/hero.jpg");

    background-size:cover;

    background-position:center;

    min-height:70vh;

    display:flex;

    align-items:center;

    color:white;

}

.feature-card{

    border:none;

    border-radius:15px;

    transition:.3s;

}

.feature-card:hover{

    transform:translateY(-6px);

}

footer{

    font-size:14px;

}

</style>