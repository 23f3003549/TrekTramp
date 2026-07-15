<template>

    <div class="container-fluid d-flex min-vh-100 bg-dark justify-content-center align-items-center">

        <div class="card shadow p-4" style = "width:400px">


            <div class="d-flex justify-content-between align-items-center mb-4">

                <h2 class="fw-bold mb-0" style="color: black;">
                    Register
                </h2>
            
                <RouterLink
                    to="/"
                    class="btn btn-outline-dark btn-sm"
                >
                    Home
                </RouterLink>

            </div>

            <form @submit.prevent="register">

                <div class="mb-3">
                   <label for="name" class="form-label">Name</label>
                   <input type="text" id= "name" class="form-control" placeholder="Enter your name" v-model="name" required>
                </div>

            <div class=" mb-3 ">
                <label for="email" class="form-label">Email</label>
                <input type="email" id= "email" class="form-control" placeholder="Enter your email" v-model="email" required>
            </div>

            <div class=" mb-3 ">
                <label for="password" class="form-label">Password</label>
                <input type="password" id= "password" class="form-control" placeholder="Enter password", v-model="password" required>
            </div>

            <div v-if="errormessage" class="alert alert-danger">
                {{ errormessage }}
            </div>
                <button
                    type="submit"
                    class="btn btn-dark w-100 mt-2"
                >
                    Register
                </button>
                
                <div class="text-center mt-4">
                
                    <small class="text-muted">
                        Already have an account?
                    </small>
                
                    <br>
                
                    <RouterLink
                        to="/login"
                        class="text-decoration-none fw-semibold"
                    >
                        Login here
                    </RouterLink>
                
                </div>

            
            </form>



        </div>

    </div>

</template>

<script>

import axios from "axios"

export default {
    name: "RegisterView",
    data(){
        return {
            "name": "",
            "email": "",
            "password": "",
            "errormessage":""
        }
    },
    methods: {
        async register(){

            try{
                const response = await axios.post(
                "http://127.0.0.1:5000/api/auth/user/registration" ,
                {
                    name : this.name,
                    email : this.email,
                    password : this.password

                }
            )

            console.log(response.data)

            alert("User registered successfully")
            this.$router.push("/login")

            }
            catch(error){
                console.log(error)
                this.errormessage = error.response.data.message
            }

        }
    }

}
</script>
<style scoped>
.card{

    border-radius:8px;

}

.form-control{

    border-radius:10px;

}

.btn{

    border-radius:10px;

}
</style>