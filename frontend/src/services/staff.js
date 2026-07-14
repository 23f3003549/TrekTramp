import api from "./api";

export function createStaff(data){

    return api.post("/admin/staff", data);

}

export function getAllStaff(search=""){

    return api.get("/admin/staff",{
        params:{
            search
        }
    });

}

export function getStaff(id){

    return api.get(`/admin/staff/${id}`);

}

export function updateStaff(id,data){

    return api.put(`/admin/staff/${id}`,data);

}

export function changeStaffStatus(id,status){

    return api.put(`/admin/staff/${id}/status`,
        {

            status

        }

    );

}

export function getAvailableStaff(){

    return api.get("/admin/available-staff");

}

export function assignStaff(data){

    return api.post("/admin/staff-assignment", data);

}


// ----------------staff apis-------------------

export function getMyProfile(){

    return api.get("/staff/profile");

}

export function completeProfile(data){

    return api.put( "/staff/profile", data);

}

export function getDashboardStatistics(){

    return api.get("/staff/dashboard");

}

export function getMyTreks(search=""){

    return api.get("/staff/my-treks",{params:{search}
        });

}

export function updateTrekCapacity(id,data){

    return api.put(`/staff/treks/${id}/capacity`,data);

}

export function updateTrekStatus(id,data){

    return api.put(`/staff/treks/${id}/status`,data);

}

export function getParticipants(){

    return api.get("/staff/participants");

}

export function getAllAssignedParticipants(search=""){

    return api.get(

        "/staff/participants",
        {

            params:{

                search: search

            }

        }

    );

}

export function getParticipantDetails(bookingId){

    return api.get(

        `/staff/participants/${bookingId}`

    );

}

export function updateParticipant(bookingId, data){

    return api.patch(

        `/staff/participants/${bookingId}`,

        data

    );

}



