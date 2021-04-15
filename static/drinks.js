const BASE_URL =  "http://127.0.0.1:5000"

function generateDrink(drink){
    let temp = "<div class='row my-3 justify-content-around container' id='new_search'>";
    for(var i = 0; i < drink.data.drinks.length;i++){
        
        temp +=  `
           <a class=" my-3 justify-content-around " href="/drinks/${drink.data.drinks[i].idDrink}">
            <div >
                <img class="img-thumbnail rounded" style="width: 18rem;" src="${drink.data.drinks[i].strDrinkThumb}" alt="">
                <h2 class="text-left">
                    ${drink.data.drinks[i].strDrink}
                </h2>
            </div>
            </a>
        `;
        
        console.log(i);
        console.log(drink.data.drinks[i]);
    }
    console.log(temp);
    temp += "</div>";
    return temp;
    
}
$("#form_name").on("submit", async function(e){
    e.preventDefault();
    $("#new_search").remove()
    let name1 = $("#search-name").val();
    
    const response = await axios.post(`${BASE_URL}/search`, {
        name1
    });
    console.log(response);
    let newDrink = $(generateDrink(response))
    $("#drink-list").append(newDrink);
})
