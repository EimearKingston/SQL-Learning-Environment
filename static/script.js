document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".menu-btn"); 
    const closeButton = document.querySelector(".close-btn");
    const sidebar = document.querySelector(".sidebar"); 
    let submit = document.getElementById("submit");

    menuButton.addEventListener("click", function () {
        sidebar.classList.toggle("active");
    }); 
    closeButton.addEventListener("click", function () {
        sidebar.classList.remove("active"); 
    }); 

    submitButton.addEventListener("click", function () { 
        submit.disabled = true; 
        let text = "Executing"; 
        let dot = "."; 
        for (let i = 1; i < 4; i++){ 
            if (i==3){ 
                submit.innerHTML == "Executing"; 
                i = 0
            }  
            submit.innerHTML = text + dot*i; 
            
        } 

    }

    );
});