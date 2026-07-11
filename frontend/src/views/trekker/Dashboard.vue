<template>

<TrekkerLayout
    title="Dashboard"
    placeholder="Search Treks..."
>

    <TrekkerStats/>

</TrekkerLayout>

</template>

<script>

import TrekkerLayout from "../../layouts/TrekkerLayout.vue";
import TrekkerStats from "../../components/trekker/TrekkerStats.vue";

export default{

    name:"Dashboard",

    components:{

        TrekkerLayout,
        TrekkerStats

    }

}

</script>