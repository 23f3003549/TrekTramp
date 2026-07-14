
import api from "./api";

export function getAllTreks(search=""){
    return api.get("treks", {
        params:{
            search
        }
    });
}

export function createTrek(data){

    return api.post("/treks",data);

}
export function deleteTrek(id){

    return api.delete(`/treks/${id}`);

}

export function updateTrek(id, data){

    return api.put(`/treks/${id}`, data);

}

export function getTrek(id){
    return api.get(`/treks/${id}`);
}

