<template>

<TrekkerLayout
    title="Profile"
    placeholder="Search..."
>

    <ProfilePanel />

</TrekkerLayout>

</template>

<script>

import TrekkerLayout from "../../layouts/TrekkerLayout.vue";
import ProfilePanel from "../../components/common/ProfilePanel.vue";

export default{

    name:"Profile",

    components:{

        TrekkerLayout,
        ProfilePanel

    }

}

</script>