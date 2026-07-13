import api from "./api";

export function getDashboardStats() {
    return api.get("/admin/dashboard");
}

export function getStaffDetails(staffId){

    return api.get(

        `/admin/staff/${staffId}/details`

    );

}

export function updateStaffStatus(staffId, data){

    return api.put(

        `/admin/staff/${staffId}/status`,

        data

    );

}

// ---------------------- Get User Details ----------------------

export function getUserDetails(userId){

    return api.get(

        `/admin/user/${userId}/details`

    );

}


// ---------------------- Update User Status ----------------------

export function updateUserStatus(userId, data){

    return api.put(

        `/admin/user/${userId}/status`,

        data

    );

}

//---------------------- Get All Users ----------------------

export function getAllUsers(){

    return api.get(

        "/admin/users"

    );

}


//---------------------- Get Single User ----------------------

export function getUser(userId){

    return api.get(

        `/admin/user/${userId}`

    );

}