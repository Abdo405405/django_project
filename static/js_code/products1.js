//declaretion
let myNewProducts = document.querySelector(".new-row");
let myBestProducts = document.querySelector(".best-row");
let listCartHTML = document.querySelector('.shop-list');
let myDataObject;
let myArray = [];
let afterCart = [];
let prodArray = [];

// start get products from JSON
let xhr = new XMLHttpRequest();
xhr.open("GET","{% static 'js_code/products.json'}");
xhr.send();
xhr.onreadystatechange = function (){
  if(xhr.readyState === 4 && xhr.status === 200)
   {
      myDataObject = JSON.parse(this.responseText);
      prodArray = myDataObject.products;
      
      //add products to cart
      document.addEventListener("click",function(e){
      if(e.target.classList.contains("addCart")){
          createCart(e.target.dataset.id,prodArray);
       }
      });
      //set New products 
      setNewItemsHome();
      //set best products 
      setBestItemsHome();
   };
};
// end get products from JSON

//start set products functions
function setNewItemsHome () {
     // load list product
     myNewProducts.innerHTML = "";
     prodArray.forEach(product => {
         let newProduct = document.createElement('div');
         newProduct.classList.add('box');
         newProduct.innerHTML = `
         <img src="${product.image}">
        <div class="content">
         <h3>${product.name}</h3>
         <p class="description">${product.description}</p>
         <p class="price">price: ${product.price}$ <span class="old-price" delete> 120$</span></p>
          </div>
         <div class="process">
            <a class="nav-btn" href="">Buy</a>
            <a class="nav-btn addCart" data-id = "${product.id}">Add To Cart</a>
          </div>
          <div class="hover-btns">
            <a class="favorite" href=""><i class="fas fa-heart"></i></a>
            <a class="view" href=""><i class="fas fa-eye"></i></a>
            </div>
            <a class="new-mark">New</a>`;
          myNewProducts.prepend(newProduct);
    });
}
function setBestItemsHome () {
     // load list product
     myBestProducts.innerHTML = "";
     prodArray.forEach(product => {
         let newProduct = document.createElement('div');
         newProduct.classList.add('box');
         newProduct.innerHTML = `
         <img src="${product.image}">
        <div class="content">
         <h3>${product.name}</h3>
         <p class="description">${product.description}</p>
         <p class="price">price: ${product.price}$ <span class="old-price" delete> 120$</span></p>
          </div>
         <div class="process">
            <a class="nav-btn" href="">Buy</a>
            <a class="nav-btn addCart" data-id = "${product.id}">Add To Cart</a>
          </div>
          <div class="hover-btns">
            <a class="favorite" href=""><i class="fas fa-heart"></i></a>
            <a class="view" href=""><i class="fas fa-eye"></i></a>
            </div>
           `;
          myBestProducts.prepend(newProduct);
    });
}
//end set products functions


//start creating cart 
function createCart (idValue,prodcuts) {
   prodcuts.forEach(e => {
     if(idValue == e.id){
       myArray.push({
          pid : e.id,
          pname : e.name,
          price : e.price,
          pimg : e.image,
          quantity : 1
       });
     }
   });
   
   //console.log(myArray)
  // addElementsToCart(myArray);
}
function addElementsToCart(array){
   array.forEach(e => {
      let cartProduct = document.createElement("div");
      cartProduct.classList.add("item");
      cartProduct.innerHTML = `
            <div class="context">
            <div class="cart-image">
            <img src="${e.pimg}">
            </div>
            <div class="product-name">
               ${e.pname}
            </div>
              
            </div>
            <div class="item-functions">
             <div class="total-p-item">
               ${e.price}$
             </div>
             <div class="quantity">
               <button class="decr-btn">-</button>
               <input type="number" value="${e.quantity}">
               <button class="incr-btn">+</button>
             </div>
             <button class="del-cart"><i class="fa-solid fa-trash"></i></button>
            </div>
          </div>
      `;
      listCartHTML.appendChild(cartProduct);
   });
}
function filterCartArray(array){
  array.forEach(e => {
    let totalQuantity = 0;
  })
}
//end creating cart 
