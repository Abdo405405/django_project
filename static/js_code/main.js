// start Back To Top Button
let backUpBtn = document.querySelector(".back-btn");
function scrollChecker() {
  if (window.scrollY > 200) {
    backUpBtn.style.display = "flex";
  } else {
    backUpBtn.style.display = "none";
  }
}
function backToUp() {
  window.scrollTo({
      left:0,
      top:0,
      behavior:"smooth"
   });
}
window.addEventListener("scroll", scrollChecker);
backUpBtn.addEventListener("click" , backToUp);
// end Back To Top Button


//start products scroll
let newRaw = document.querySelector(".new-row");
let bestRaw = document.querySelector(".best-row");
let categRow = document.querySelector(".categ-row");


function prodScrollRight(myRow) {
    myRow.scrollTo({
      left: myRow.scrollLeft + 300,
      top: 0,
      behavior: "smooth"
    });
  }
function prodScrollLeft(myRow) {
    myRow.scrollTo({
      left: myRow.scrollLeft - 300,
      top: 0,
      behavior: "smooth"
    });
  }
document.addEventListener("click", function(e){
  if(e.target.classList.contains("pre-btn-new")){
    prodScrollLeft(newRaw);
  }
  else if(e.target.classList.contains("nxt-btn-new")){
    prodScrollRight(newRaw);
  }
});
document.addEventListener("click", function(e){
  if(e.target.classList.contains("pre-btn-bst")){
    prodScrollLeft(bestRaw);
  }
  else if(e.target.classList.contains("nxt-btn-bst")){
    prodScrollRight(bestRaw);
  }
});
//end products scroll

document.addEventListener("click", function(e){
  if(e.target.classList.contains("pre-catego")){
    prodScrollLeft(categRow);
  }
  else if(e.target.classList.contains("nxt-catego")){
    prodScrollRight(categRow);
  }
});

//start open and close cart

let shoppingList = document.querySelector(".cart-side");
let cartOpentBtns = document.querySelectorAll(".open-cart")
// console.log(cartOpentBtns)
cartOpentBtns.forEach((b) => {
 b.addEventListener("click",function(e){
  shoppingList.style.right = "0";
  });
});

document.addEventListener("click",function(e){
if(e.target.classList.contains("close-cart")){
  shoppingList.style.right = "-120%";
}
});
//end open and close cart 

//start open and close favorites 
let favoList = document.querySelector(".favorite-side");
let favoOpenBtns = document.querySelectorAll(".open-favo");

favoOpenBtns.forEach((b)=>{
b.addEventListener("click",function(){
  favoList.style.right = "0%";
});
});
document.addEventListener("click",function(e){
if(e.target.classList.contains("close-favorite")){
  favoList.style.right = "-120%";
}
});
//end open and close favorites 
