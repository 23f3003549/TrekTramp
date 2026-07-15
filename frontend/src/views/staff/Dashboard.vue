<template>

<StaffLayout

    title="Dashboard"

    :searchEnabled="false"

>
    <DashboardCards />

</StaffLayout>

</template>

<script>

import StaffLayout from "../../layouts/StaffLayout.vue";

import DashboardCards from "../../components/staff/DashboardCards.vue";

export default{

    name:"StaffDashboard",

    components:{

        StaffLayout,

        DashboardCards

    }

}

</script>
<style scoped>
h2{

    color:#198754;

}
</style>