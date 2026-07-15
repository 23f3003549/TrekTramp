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

export function getUserDetails(userId){

    return api.get(

        `/admin/user/${userId}/details`

    );

}

export function updateUserStatus(userId, data){

    return api.put(

        `/admin/user/${userId}/status`,

        data

    );

}

export function getAllUsers(search=""){

    return api.get(

        "/admin/users", {
            params:{
                search
            }
        }

    );

}

export function getUser(userId){

    return api.get(

        `/admin/user/${userId}`

    );

}

export function getAllBookings(search=""){

    return api.get(

        "/admin/bookings", {
            params:{
                search
            }
        }

    );

}


export function getBookingDetails(bookingId){

    return api.get(

        `/admin/booking/${bookingId}`

    );

}


export function updateBooking(bookingId,data){

    return api.put(

        `/admin/booking/${bookingId}`,

        data

    );

}


export function getReports(){

    return api.get(

        "/admin/reports"

    );

}


export function exportUsersReport(){

    return api.get(

        "/admin/reports/users",

        {

            responseType:"blob"

        }

    );

}

export function exportStaffReport(){

    return api.get(

        "/admin/reports/staff",

        {

            responseType:"blob"

        }

    );

}


export function exportBookingReport(){

    return api.get(

        "/admin/reports/bookings",

        {

            responseType:"blob"

        }

    );

}


export function exportTrekReport(){

    return api.get(

        "/admin/reports/treks",

        {

            responseType:"blob"

        }

    );

}

export function getAdminProfile(){

    return api.get(

        "/admin/profile"

    );

}

export function updateAdminProfile(data){

    return api.put(

        "/admin/profile",

        data

    );

}

export function changeAdminPassword(data){

    return api.put(

        "/admin/change-password",

        data

    );

}