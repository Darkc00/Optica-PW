let cart = [];
divCarrito = document.getElementById('carrito-items')



function Item(name, price,  product_id, img) {
    this.name = name;
    this.img = img;
    this.price = price;
    this.product_id = product_id;
}

function saveCart() {
    sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
}

function loadCart() {
    divCarrito.innerHTML=''
    cart = JSON.parse(sessionStorage.getItem('shoppingCart'));
    cart.forEach(element => {
        addtoDiv(element)
    });
}

function addtoDiv(product){
    console.log(product)
    divCarrito.innerHTML += `
        <div class="cart-item" id="${product.product_id}">
            <span class="fas fa-times" onclick="removeItemFromCart('${product.product_id}')"></span>
            <img src="${product.img}" alt="">
            <div class="content">
                <h3>${product.name}</h3>
                <div class="price">$${product.price}/-</div>
            </div>
        </div>
        `
}

function  addItemToCart(name, price,  product_id, img)   {
    let item = new Item(name, price,  product_id, img);
    cart.push(item);
    addtoDiv(item)
    saveCart();
}

function removeItemFromCart  (product_id) {

    for (let item in cart) {

         if (cart[item].product_id === product_id) {
  
            document.getElementById(product_id).remove()
            cart.splice(item, 1);
            break;
         }
    }
    saveCart();
}

function loadProducts(cat){
    const div = document.querySelector('.box-container')
    fetch('/productos/cat/'+cat)
    .then(data => data.json())
    .then(data => {
        
        div.innerHTML = ''
        data.producto.forEach(element => {
            div.innerHTML += `
        <div class="box">
            <div class="image">
                <img src="${element.image}" alt="">
            </div>
            <div class="content">
                <p style='font-size: 2.5rem;line-height: 1.5;color: #fff;'>${element.nombre}</h3>
                <p style='font-size: 1.6rem;line-height: 1.8;color: #ccc;padding: 1rem 0;'>${element.descripcion}</p>
                <div class="price" style="color: #fff;font-size: 2.5rem;padding: .5rem 0;">$${element.precioVenta}</div>
                <a class="btn add-to-cart" 
                onclick="showCarrito('${element.idProducto}','${element.nombre}','${element.precioVenta}','${element.image}')">
                Agregar a carrito
                </a>
            </div>
        </div>
        `
        });
        
    })
}
function showCarrito(id,name,price, img){
    let price2 = Number(price);
    addItemToCart(name, price2, id, img);

    cartItem.classList.toggle('active');
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
}


function comprar(){
    let cantidad = 0;
    let precio = 0;
    cart.forEach(element => {
        cantidad++
        precio+=element.price
    });
    
    fetch("/pedidos",{
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body:JSON.stringify({total:precio,cantidad:cantidad})})
        .then(result => result.json())
        .then(result =>{
            if( result.exito === true){
                alert('pedido registrado.')
                sessionStorage.removeItem('shoppingCart');
                location.reload();
            }else{
                alert("Ha ocurrido un error")
            }

        })

}

if (sessionStorage.getItem("shoppingCart") != null) {
    loadCart();
}
