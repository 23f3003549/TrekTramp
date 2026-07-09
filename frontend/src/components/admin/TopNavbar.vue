<template>

    <header class="top-navbar">

        <button class="btn btn-outline-success">
            ☰

        </button>
        <div class="admin-profile">
            Admin ▼

        </div>

    </header>

</template>

<script>

export default{
    name: "TopNavbar"
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

.admin-profile{
    font-weight:600;
}

</style>