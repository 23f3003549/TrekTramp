<template>

    <div class="layout">

        <div class="d-flex">

            <Sidebar />

            <div class="main-content flex-grow-1">
                
                <header>
                    <TopNavbar /> 
                </header>

                <main class="p-4">
                    <slot>
                        
                    </slot>
                </main>

            </div>

        </div>

    </div>

</template>

<script>

import Sidebar from '../components/admin/Sidebar.vue';
import TopNavbar from '../components/admin/TopNavbar.vue';

export default {
    name: "MainLayout",
    components : {
        Sidebar,
        TopNavbar
    }
}

</script>

<style scoped>
.layout{
    width: 100%;
    min-height:100vh ;
}

.main-content{
    min-height: 100vh;
    background: #f8f9fa ;
}

</style>