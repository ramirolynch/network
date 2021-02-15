
function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }

var csrftoken = getCookie('csrftoken');
 

function post_liker(post_id) {

let liker = document.querySelector(`#liker-${post_id}`);

let likescount = parseInt(document.querySelector(`#count_likes-${post_id}`).textContent);

let addOne = likescount + 1;
let lessOne = likescount - 1;

console.log(addOne);

let likerColor = liker.getAttribute('fill');

console.log(likerColor);

// const greet = document.querySelector(`#greet`);

// const user = greet.textContent;

// let userlist = new Array(user);

// console.log(userlist)

if (likerColor === "black") {


     fetch("/api/posts/" + post_id + "/", {
          credentials: 'include',
          method: 'PUT',
          headers: {
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'X-CSRFToken': csrftoken
             },
          mode: 'same-origin',
          body: JSON.stringify({      
          liked : true,
          total_likes : addOne
      })
     })
     .then(function(response) {
          return response.json();
     })
     .then(function(data) {
          console.log("Data is ok", data);
      })
      .catch(function(ex) {
          console.log("parsing failed", ex);
      });

     liker.setAttribute('fill', 'red');
     document.querySelector(`#count_likes-${post_id}`).innerHTML = addOne;
} 

else 

{

     liker.setAttribute('fill', 'black');

     fetch("/api/posts/" + post_id + "/", {
          credentials: 'include',
          method: 'PUT',
          headers: {
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'X-CSRFToken': csrftoken
             },
          mode: 'same-origin',
          body: JSON.stringify({  
               liked : false,
               total_likes : lessOne
           })
     })
     .then(function(response) {
          return response.json();
     })
     .then(function(data) {
          console.log("Data is ok", data);
      })
      .catch(function(ex) {
          console.log("parsing failed", ex);
      });

     document.querySelector(`#count_likes-${post_id}`).innerHTML = lessOne;

   }

}


function postedit(post_id) {

const editBtn = document.querySelector(`#edit-${ post_id }`);
const saveBtn = document.querySelector(`#save-${ post_id }`);
const editForm = document.querySelector(`#edit_form-${ post_id }`);
// const postBod = document.querySelector(`#post_body-${ post.id }`);

console.log(editBtn);
console.log(editForm);
// console.log(postBod);


editForm.style.display = "block";
editBtn.style.display = "none";
saveBtn.style.display = "block";
// postBod.style.display = "none";


}


function savepost(post_id) {

const textArea = document.querySelector(`#textarea-${ post_id }`);
const textAreaContent = textArea.value;

const saveBtn = document.querySelector(`#save-${ post_id }`);

console.log(textAreaContent);

fetch("/api/posts/" + post_id + "/", {
     credentials: 'include',
     method: 'PUT',
     headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
     mode: 'same-origin',
     body: JSON.stringify({  
          body : textAreaContent
      })
})
.then(function(response) {
     return response.json();
})
.then(function(data) {
     console.log("Data is ok", data);
 })
 .catch(function(ex) {
     console.log("parsing failed", ex);
 });

const editBtn = document.querySelector(`#edit-${ post_id }`);
const editForm = document.querySelector(`#edit_form-${ post_id }`);
const postBod = document.querySelector(`#post_body-${ post_id }`);

postBod.textContent = textAreaContent;

editForm.style.display = "none";
editBtn.style.display = "block";
saveBtn.style.display = "none";

}