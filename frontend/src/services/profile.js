import api from "./api";


// ------------------------- Get Profile -------------------------

export function getProfile(){

    return api.get(

        "/profile"

    );

}


// ------------------------- Update Profile -------------------------

export function updateProfile(data){

    return api.put(

        "/profile",

        data

    );

}