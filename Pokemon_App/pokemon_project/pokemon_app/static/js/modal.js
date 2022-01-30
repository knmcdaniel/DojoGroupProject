// get elements for popup
const wrapper = document.querySelector(".popup-wrapper");
const popupbtns = document.querySelectorAll('.popupbtn');
const popup = document.querySelector('.popup');
const popupclose = document.querySelector('.popup-close');
const popupContent = document.querySelector(".popup-content");

            // popup

// get project item popup info

popupbtns.forEach(btn => btn.addEventListener('click', () => {
const popupinfo = btn.parentNode.childNodes[11];
    popupContent.querySelector(".popup-image").src = popupinfo.children[0].textContent //project image
    popup.querySelector(".popup-title").textContent = popupinfo.children[1].textContent; // project title
    popupContent.querySelector(".popup-descrip").textContent  =  popupinfo.children[2].textContent; // project description
    popupContent.querySelector(".popup-link").textContent =  popupinfo.children[3].textContent; //project link text
    popupContent.querySelector(".popup-link").href = popupinfo.children[4].textContent;

    
    wrapper.style.display = "block";
    popup.style.display = "block";
}));


// //this  block of code will continuously check if the user clicks the "X" button
//  on the popup which will mean they want to close the popup and so it will close it if they do.
popupclose.addEventListener('click', () => {
    popup.style.display = 'none';
    wrapper.style.display = "none";

});

// // this block of code continuously checks if the user clicks anywhere outside the popup box. 
// If they do, it will close the popup. This is optional. You don't have to include this feature.
popup.addEventListener('click', (e) => {
    if(e.target.className === 'popup-wrapper'){
      popup.style.display = 'none';
      wrapper.style.display = "none";
    }
});