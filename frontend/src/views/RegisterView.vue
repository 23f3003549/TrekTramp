<template>

    <div class="container-fluid d-flex min-vh-100 bg-dark justify-content-center align-items-center">

        <div class="card shadow p-4" style = "width:400px">


            <div class="text-center mb-4">
                <h1>Register</h1>
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

            <!-- <div class=" mb-3 ">
                <label for="age" class="form-label">Age</label>
                <input type="number" id= "age" class="form-control" placeholder="Enter your age" v-model="age" required>
            </div>

            <div class=" mb-3  ">
                <label for="gender" class="form-label">Gender</label>

                <select class="form-select" id="gender" v-model="gender">
                    <option disabled selected value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
                
                
            </div>

            <div class=" mb-3 ">
                <label for="phone" class="form-label">Phone</label>
                <input type="tel" id= "phone" class="form-control" placeholder="Enter your number", v-model="phone">
            </div> -->

            <div class=" mb-3 ">
                <label for="password" class="form-label">Password</label>
                <input type="password" id= "password" class="form-control" placeholder="Enter password", v-model="password" required>
            </div>

            <div v-if="errormessage" class="alert alert-danger">
                {{ errormessage }}
            </div>

            <button type="submit" class="btn btn-dark">
                Register
            </button>
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
            // "age": "",
            // "gender": "",
            // "phone":"",
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
                    // age : this.age,
                    // gender : this.gender,
                    // phone : this.phone,
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