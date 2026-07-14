<template>

    <div class="layout">

            <Sidebar />

            <div class="main-content ">
                
                <header>
                    <TopNavbar

                        :placeholder="placeholder"
                    
                        :searchEnabled="searchEnabled"
                    
                        @search="handleSearch"

                    />
                </header>

                <main class="p-4">
                    <slot>
                        
                    </slot>
                </main>

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
    },
    props:{

        placeholder:{

            type:String,

            default:"Search..."

        },

        searchEnabled:{

            type:Boolean,

            default:true

        }

    },
    emits:[
        "search"
    ],
    methods:{
        handleSearch(keyword){
            this.$emit(
                "search", keyword
            );
        }
    }
}

</script>
<style>

.layout{

    min-height:100vh;

}

.main-content{

    margin-left:260px;

    min-height:100vh;

    background:#f8f9fa;

}

.sidebar{

    position:fixed;

    top:0;

    left:0;

    width:260px;

    height:100vh;

    overflow-y:auto;

    background:#fff;

    z-index:1000;

}
</style>