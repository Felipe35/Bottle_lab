let slider = document.querySelector(".slider");
    let list_items = document.querySelectorAll(".navigation ul li");
    let logo_text = document.querySelector(".logo_text");

    let index_value = 0;
    let left_position = 0;


    // Animation for slider to slide on menu items or list items.

    list_items.forEach((list_item, index) => {

        // Setting initial left position and width of slider.
        slider.style.width = list_items[0].clientWidth + "px";
        slider.style.left = "0px";


        // Hover or click effect.
        list_item.onmouseover = function () {
            slider.style.width = list_item.clientWidth + "px";
            index_value = index;
            console.log(list_item.clientWidth)
            get_left_position();
            slider.style.left = left_position + "px";
            left_position = 0;
        }

    });

    function get_left_position() {
        for (let i = 0; i < index_value; i++) {
            const element = list_items[i];
            left_position += element.clientWidth;
            // console.log(left_position);
        }
    }



    // Animation for slider to slide on menu items or list items.

    list_items.forEach((list_item, index) => {

        // Setting initial left position and width of slider.
        slider.style.width = list_items[0].clientWidth + "px";
        slider.style.left = "0px";


        // Hover or click effect.
        list_item.onmouseover = function () {
            slider.style.width = list_item.clientWidth + "px";
            index_value = index;
            console.log(list_item.clientWidth)
            get_left_position();
            slider.style.left = left_position + "px";
            left_position = 0;
        }
        
        list_item.onmouseout = function () {
            slider.style.width = list_items[0].clientWidth + "px";
            slider.style.left = "0px";
        }
    });




// Animation for logo text and navigation list items on page load.
setTimeout(() => {
    logo_animation();
    menu_animation();
}, 500);

function logo_animation() {
    logo_text.style.top = "0px";
    logo_text.style.opacity = "1";
}

function menu_animation() {
    for (let m = 0; m < list_items.length; m++) {
        const element = list_items[m];
        setTimeout(() => {
            element.style.top = "0px";
            element.style.opacity = "1";
        }, m * 100);
    }
}