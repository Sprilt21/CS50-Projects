document.addEventListener("DOMContentLoaded", () => {
  
    document.querySelector("#cands-view").addEventListener("click", () => {
        view_candidates();
    });
  
    document.querySelector("#pm-view").addEventListener("click", () => {
        view_messages();
    });
  
    document.querySelector("#create").addEventListener("click", () => {
        create_app();
    });
  
    document.querySelector("#view-old").addEventListener("click", () => {
        view_old_cands()
    });

    document.querySelector('#home-button').addEventListener("click", () => {
        home_page();
    })

    home_page();
})

function home_page() {

    document.querySelector("#nav-buttons").style.display = "block";
    document.querySelector("#candidates").style.display = "none";
    document.querySelector("#view-pms").style.display = "none";
    document.querySelector("#create-app").style.display = "none";
    document.querySelector("#accepted").style.display = "none";
    document.querySelector("#pms").style.display = "none";

    document.querySelector("#header").textContent = "Home Page";
}

function view_candidates() {
    
    document.querySelector("#nav-buttons").style.display = "none";
    document.querySelector("#candidates").style.display = "block";
    document.querySelector("#view-pms").style.display = "none";
    document.querySelector("#create-app").style.display = "none";
    document.querySelector("#accepted").style.display = "none";

    document.querySelector("#candidates").innerHTML = "";

    document.querySelector("#header").textContent = "Candidates";
    
    fetch('/getCand', {
        method: "GET",
        headers: {
            'accept-encoding': 'none',
            'content-type': 'application/json'
          }
    })
    .then(response => response.json())
    .then(candidates => {

        if (candidates.length == 0) {
            const noElements = document.createElement("h3");
            noElements.id = "no-elements"
            noElements.textContent = "No current jobs to hire. Be the first!";

            document.querySelector("#candidates").append(noElements);
        } else {
            candidates.forEach(candidate => {

                const jobDiv = document.createElement("div");
                jobDiv.className = "job-tile";
    
                const jobUser = document.createElement("h4");
                jobUser.textContent = candidate.user;
                jobDiv.append(jobUser);
    
                const jobDesc = document.createElement("p");
                jobDesc.textContent = candidate.description;
                jobDiv.append(jobDesc);
    
                const jobPrice = document.createElement("b");
                jobPrice.textContent = "$" + candidate.price + "/hr";
                jobDiv.append(jobPrice);
    
                const jobTime = document.createElement("p");
                jobTime.textContent = "Started at: " + candidate.timestamp;
                jobDiv.append(jobTime);
    
                const hireButton = document.createElement("button");
                hireButton.textContent = "Hire them";
                hireButton.className = "postButton";
                hireButton.addEventListener('click', () => {
                    fetch('/hire/' + candidate.id, {
                        method: "POST",
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result)
                        view_candidates();
                    })
                })
                jobDiv.append(hireButton);
    
                const startDMButton = document.createElement("button");
                startDMButton.textContent = "Message " + candidate.user;
                startDMButton.className = "postButton";
                startDMButton.addEventListener('click', () => {
                    open_pm(candidate.user)
                })
                jobDiv.append(startDMButton);
    
                document.querySelector("#candidates").append(jobDiv);
            })
        }
    })
}

function view_old_cands() {

    document.querySelector("#nav-buttons").style.display = "none";
    document.querySelector("#candidates").style.display = "none";
    document.querySelector("#view-pms").style.display = "none";
    document.querySelector("#create-app").style.display = "none";
    document.querySelector("#accepted").style.display = "block";

    document.querySelector("#header").textContent = "Accepted Candidates";

    fetch('/getOlds', {
        method: "GET",
        headers: {
            'accept-encoding': 'none',
            'content-type': 'application/json'
          }
    })
    .then(response => response.json())
    .then(candidates => {
        candidates.forEach(candidate => {

            const jobDiv = document.createElement("div");
            jobDiv.className = "job-tile";
            
            const jobUser = document.createElement("h4");
            jobUser.textContent = candidate.user;
            jobDiv.append(jobUser);

            const jobDesc = document.createElement("p");
            jobDesc.textContent = candidate.description;
            jobDiv.append(jobDesc);

            const jobPrice = document.createElement("b");
            jobPrice.textContent = candidate.price + "/hr";
            jobDiv.append(jobPrice);

            const jobTime = document.createElement("p");
            jobTime.textContent = "Started at: " + candidate.timestamp;
            jobDiv.append(jobTime);

            document.querySelector("#accepted").append(jobDiv);
        })
    })
}

function view_messages() {

    document.querySelector("#nav-buttons").style.display = "none";
    document.querySelector("#candidates").style.display = "none";
    document.querySelector("#view-pms").style.display = "block";
    document.querySelector("#create-app").style.display = "none";
    document.querySelector("#accepted").style.display = "none";
    document.querySelector("#pms").style.display = "none";

    document.querySelector("#header").textContent = "Private Messages";
    
    document.querySelector("#view-pms").innerHTML = "";

    fetch("/getSenders", {

        method: "GET",
        headers: {
            'accept-encoding': 'none',
            'content-type': 'application/json'
          }
    })
    .then(response => response.json())
    .then(senders => {
        console.log(senders)
        senders.forEach(sender => {

            const contact = document.createElement("div");
            contact.className = "user-msg";
            contact.textContent = sender;
            contact.addEventListener('click', () => {
                open_pm(sender)
            })
        
            document.querySelector("#view-pms").append(contact);
        })
    })
}

function open_pm(post_user) {
    
    document.querySelector("#nav-buttons").style.display = "none";
    document.querySelector("#candidates").style.display = "none";
    document.querySelector("#create-app").style.display = "none";
    document.querySelector("#accepted").style.display = "none";
    document.querySelector("#view-pms").style.display = "none";
    document.querySelector("#pms").style.display = "block";

    document.querySelector("#text-body").value = '';
    document.querySelector("#header").textContent = "Messaging: " + post_user;
    fetch("/getPMs/" + post_user, {
        method:"GET",
        headers: {
            
            'accept-encoding': 'none',
            'content-type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(msgs => {

        console.log(post_user)
        console.log(msgs)
        
        msgs.forEach(msg => {
            msgLine = document.createElement("div");
            msgLine.className = "msgline";

            msgBlob = document.createElement("div");
            msgBlob.className = "msgs";
            msgBlob.textContent = msg.text;

            console.log(msg)
            console.log(post_user)
            console.log(msg.receiver)
            console.log(msg.receiver == post_user)
            if (msg.receiver == post_user) {
                msgBlob.id = "sent";
                console.log("1")
            } else {
                msgBlob.id = "received";
                console.log("2")
            }

            msgLine.append(msgBlob)
            msgLine.append(document.createElement("br"));
            document.querySelector("#texts").append(msgLine);
        })
    })

    document.querySelector("#send-msg").onsubmit = () => {

        fetch("/sendMsg/" + post_user, {
            method:"POST",
            body: JSON.stringify({
                text: document.querySelector("#text-body").value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            open_pm(post_user)
        })
    }
}

function create_app() {

    document.querySelector("#nav-buttons").style.display = "none";
    document.querySelector("#candidates").style.display = "none";
    document.querySelector("#view-pms").style.display = "none";
    document.querySelector("#create-app").style.display = "block";
    document.querySelector("#accepted").style.display = "none";

    document.querySelector("#header").textContent = "Create Application";

    document.querySelector("#application-form").onsubmit = () => {
        fetch("/create", {

            method: "POST",
            body: JSON.stringify({
                price: document.querySelector("#price-form").value,
                description: document.querySelector("#desc-body").value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
    }
 
}
