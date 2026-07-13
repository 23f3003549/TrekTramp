<template>

<StaffLayout
    title="Profile"
    placeholder="Search..."
>

    <ProfilePanel />

</StaffLayout>

</template>

<script>

import StaffLayout from "../../layouts/StaffLayout.vue";
import ProfilePanel from "../../components/common/ProfilePanel.vue";

export default{

    name:"Profile",

    components:{

        StaffLayout,
        ProfilePanel

    }

}

</script>