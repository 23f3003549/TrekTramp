import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:5000/api"
});

api.interceptors.request.use((config)=>{

    const token = localStorage.getItem("access_token");
    if(token){
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response)=>{
        return response;
    },
    async(error)=>{
        const originalRequest = error.config;
        if(
            error.response?.status===401 &&
            !originalRequest._retry
        ){

            originalRequest._retry = true;
            try{
                const refreshToken = localStorage.getItem(
                    "refresh_token"
                );
                const response = await axios.post(
                    "http://127.0.0.1:5000/api/auth/refresh",
                    {},
                    {
                        headers:{
                            Authorization:`Bearer ${refreshToken}`
                        }
                    }
                );
                const newAccessToken = response.data.access_token;

                localStorage.setItem(

                    "access_token",

                    newAccessToken

                );

                originalRequest.headers.Authorization =

                    `Bearer ${newAccessToken}`;

                return api(originalRequest);

            }

            catch(refreshError){

                localStorage.removeItem("access_token");

                localStorage.removeItem("refresh_token");

                localStorage.removeItem("role");

                localStorage.removeItem("name");

                window.location.href="/login";

                return Promise.reject(refreshError);

            }

        }

        return Promise.reject(error);

    }

);

export default api;